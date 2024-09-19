# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Script used to generate the messages files."""

from __future__ import annotations

import os
from collections import defaultdict
from enum import Enum
from inspect import getmodule
from itertools import chain, groupby
from pathlib import Path
from typing import NamedTuple

from sphinx.application import Sphinx

from pylint.checkers import initialize as initialize_checkers
from pylint.constants import MSG_TYPES
from pylint.extensions import initialize as initialize_extensions
from pylint.lint import PyLinter
from pylint.message import MessageDefinition
from pylint.utils import get_rst_title

PYLINT_BASE_PATH = Path(__file__).resolve().parent.parent.parent
"""Base path to the project folder."""

PYLINT_MESSAGES_PATH = PYLINT_BASE_PATH / "doc/user_guide/messages"
"""Path to the messages documentation folder."""

PYLINT_MESSAGES_DATA_PATH = PYLINT_BASE_PATH / "doc" / "data" / "messages"
"""Path to the folder with data for the messages documentation."""

MSG_TYPES_DOC = {k: v if v != "info" else "information" for k, v in MSG_TYPES.items()}

MESSAGES_WITHOUT_EXAMPLES = {
    "astroid-error",  # internal
    "bad-configuration-section",  # configuration
    "bad-plugin-value",  # internal
    "c-extension-no-member",  # not easy to implement in the current doc framework
    "config-parse-error",  # configuration
    "fatal",  # internal
    "import-self",  # not easy to implement in the current doc framework
    "invalid-character-nul",  # not easy to implement in the current doc framework
    "invalid-characters-in-docstring",  # internal in py-enchant
    "invalid-unicode-codec",  # placeholder (not implemented yet)
    "method-check-failed",  # internal
    "parse-error",  # internal
    "raw-checker-failed",  # internal
    "unrecognized-option",  # configuration
}
MESSAGES_WITHOUT_BAD_EXAMPLES = {
    "invalid-character-carriage-return",  # can't be raised in normal pylint use
    "return-arg-in-generator",  # can't be raised in modern python
}


class MessageData(NamedTuple):
    checker: str
    id: str
    name: str
    definition: MessageDefinition
    example_code: str
    checker_module_name: str
    checker_module_path: str
    shared: bool = False
    default_enabled: bool = True


class ExampleType(str, Enum):
    GOOD = "good"
    BAD = "bad"


MessagesDict = dict[str, list[MessageData]]
OldMessagesDict = dict[str, defaultdict[tuple[str, str], list[tuple[str, str]]]]
"""DefaultDict is indexed by tuples of (old name symbol, old name id) and values are
tuples of (new name symbol, new name category).
"""


def _register_all_checkers_and_extensions(linter: PyLinter) -> None:
    """Registers all checkers and extensions found in the default folders."""
    initialize_checkers(linter)
    initialize_extensions(linter)


def _get_example_code(data_path: Path) -> str:
    """Get the example code from the specified path."""
    if not data_path.exists():
        raise AssertionError(
            f"Documentation examples path {data_path} does not exist. "
            "Please create it and add an example."
        )

    good_code = _get_demo_code_for(data_path, ExampleType.GOOD)
    bad_code = _get_demo_code_for(data_path, ExampleType.BAD)
    pylintrc = _get_pylintrc_code(data_path)
    details = _get_titled_rst(
        title="Additional details", text=_get_rst_as_str(data_path / "details.rst")
    )
    related = _get_titled_rst(
        title="Related links", text=_get_rst_as_str(data_path / "related.rst")
    )

    _check_placeholders(data_path, bad_code, details, related)
    return "\n".join((bad_code, good_code, pylintrc, details, related)) + "\n"


def _get_pylintrc_code(data_path: Path) -> str:
    if (data_path / "pylintrc").exists():
        pylintrc = _get_titled_rst(
            title="Configuration file", text=_get_ini_as_rst(data_path / "pylintrc")
        )
    else:
        pylintrc = ""
    return pylintrc


def _get_demo_code_for(data_path: Path, example_type: ExampleType) -> str:
    """Get code examples while handling multi-file code templates."""
    if data_path.name in MESSAGES_WITHOUT_EXAMPLES or (
        data_path.name in MESSAGES_WITHOUT_BAD_EXAMPLES
        and example_type is ExampleType.BAD
    ):
        return ""
    single_file_path = data_path / f"{example_type.value}.py"
    multiple_code_path = data_path / f"{example_type.value}"

    if single_file_path.exists() and multiple_code_path.exists():
        raise ValueError(
            f"You cannot have a single file '{example_type.value}.py' and multiple files "
            f"example '{multiple_code_path}' existing at the same time."
        )

    title = "Problematic code" if example_type is ExampleType.BAD else "Correct code"
    if single_file_path.exists():
        return _get_titled_rst(
            title=title, text=_get_python_code_as_rst(single_file_path)
        )

    if multiple_code_path.exists():
        files: list[str] = []
        # Sort so the order of the files makes sense
        for file_as_str in sorted([str(p) for p in multiple_code_path.iterdir()]):
            file = Path(file_as_str)
            if file.suffix == ".py":
                files.append(
                    f"""\
``{file.name}``:

.. literalinclude:: /{file.relative_to(Path.cwd())}
    :language: python

"""
                )
        return _get_titled_rst(title=title, text="\n".join(files))
    raise AssertionError(
        f"Please add a {example_type.value} code example for {data_path}"
    )


def _check_placeholders(
    data_path: Path, bad_code: str, details: str, related: str
) -> None:
    # Check if the placeholder file can even be presented by checking if its path exists
    good_path = data_path / "good.py"
    if not good_path.exists():
        return

    if bad_code or related:
        placeholder_details = "help us make the doc better" in details
        with open(good_path, encoding="utf-8") as f:
            placeholder_good = "placeholder" in f.read()
        assert_msg = (
            f"Please remove placeholders in '{data_path}' "
            f"as you started completing the documentation"
        )
        assert not placeholder_good and not placeholder_details, assert_msg


def _get_titled_rst(title: str, text: str) -> str:
    """Return rst code with a title if there is anything in the section."""
    return f"**{title}:**\n\n{text}" if text else ""


def _get_rst_as_str(rst_path: Path) -> str:
    """Return the content of an 'rst' file or an empty string if the file does not
    exist.
    """
    if not rst_path.exists():
        return ""
    with open(rst_path, encoding="utf-8") as f:
        return f.read()


def _get_python_code_as_rst(code_path: Path) -> str:
    """Return the 'rst' representation of a python file or an empty string if the file
    does not exist.
    """
    if not code_path.exists():
        return ""
    return f"""\
.. literalinclude:: /{code_path.relative_to(Path.cwd())}
   :language: python
"""


def _get_ini_as_rst(code_path: Path) -> str:
    return f"""\
.. literalinclude:: /{code_path.relative_to(Path.cwd())}
    :language: ini
"""


def _get_all_messages(linter: PyLinter) -> tuple[MessagesDict, OldMessagesDict]:
    """Get all messages registered to a linter and return a dictionary indexed by
    message type.

    Also return a dictionary of old message and the new messages they can be mapped to.
    """
    messages_dict: MessagesDict = {
        "fatal": [],
        "error": [],
        "warning": [],
        "convention": [],
        "refactor": [],
        "information": [],
    }
    old_messages: OldMessagesDict = {
        "fatal": defaultdict(list),
        "error": defaultdict(list),
        "warning": defaultdict(list),
        "convention": defaultdict(list),
        "refactor": defaultdict(list),
        "information": defaultdict(list),
    }
    checker_message_mapping = chain.from_iterable(
        ((checker, msg) for msg in checker.messages)
        for checker in linter.get_checkers()
    )

    for checker, message in checker_message_mapping:
        example_code = _get_example_code(_get_message_data_path(message))

        checker_module = getmodule(checker)

        assert (
            checker_module and checker_module.__file__
        ), f"Cannot find module for checker {checker}"

        message_data = MessageData(
            message.checker_name,
            message.msgid,
            message.symbol,
            message,
            example_code,
            checker_module.__name__,
            checker_module.__file__,
            message.shared,
            message.default_enabled,
        )
        msg_type = MSG_TYPES_DOC[message.msgid[0]]
        messages_dict[msg_type].append(message_data)
        if message.old_names:
            for old_name in message.old_names:
                category = MSG_TYPES_DOC[old_name[0][0]]
                # We check if the message is already in old_messages, so we don't
                # duplicate shared messages.
                if (message.symbol, msg_type) not in old_messages[category][
                    (old_name[1], old_name[0])
                ]:
                    old_messages[category][(old_name[1], old_name[0])].append(
                        (message.symbol, msg_type)
                    )

    return messages_dict, old_messages


def _get_message_data_path(message: MessageDefinition) -> Path:
    return PYLINT_MESSAGES_DATA_PATH / message.symbol[0] / message.symbol


def _message_needs_update(message_data: MessageData, category: str) -> bool:
    """Do we need to regenerate this message .rst ?"""
    message_path = _get_message_path(category, message_data)
    if not message_path.exists():
        return True
    message_path_stats = message_path.stat().st_mtime
    checker_path_stats = Path(message_data.checker_module_path).stat().st_mtime
    return checker_path_stats > message_path_stats


def _get_category_directory(category: str) -> Path:
    return PYLINT_MESSAGES_PATH / category


def _get_message_path(category: str, message: MessageData) -> Path:
    category_dir = _get_category_directory(category)
    return category_dir / f"{message.name}.rst"


def _write_message_page(messages_dict: MessagesDict) -> None:
    """Create or overwrite the file for each message."""
    for category, messages in messages_dict.items():
        category_dir = _get_category_directory(category)
        if not category_dir.exists():
            category_dir.mkdir(parents=True, exist_ok=True)
        for message in messages:
            if message.shared:
                continue
            if not _message_needs_update(message, category):
                continue
            _write_single_message_page(category_dir, message)
        for _, shared_messages in groupby(
            sorted(
                (message for message in messages if message.shared), key=lambda m: m.id
            ),
            key=lambda m: m.id,
        ):
            shared_messages_list = list(shared_messages)
            if len(shared_messages_list) > 1:
                _write_single_shared_message_page(category_dir, shared_messages_list)
            else:
                _write_single_message_page(category_dir, shared_messages_list[0])


def _generate_single_message_body(message: MessageData) -> str:
    body = f""".. _{message.name}:

{get_rst_title(f"{message.name} / {message.id}", "=")}
**Message emitted:**

``{message.definition.msg}``

**Description:**

*{message.definition.description}*
"""
    if not message.default_enabled:
        body += f"""
.. caution::
  This message is disabled by default. To enable it, add ``{message.name}`` to the ``enable`` option.

"""
    if message.id.startswith("I"):
        body += f"""
.. caution::
  By default, this message will not fail the execution (pylint will return 0).
  To make pylint fail for this message use the ``--fail-on={message.id}`` option
  or ``--fail-on=I`` to fail on all enabled informational messages.

"""

    body += f"\n{message.example_code}\n"

    if message.checker_module_name.startswith("pylint.extensions."):
        body += f"""
.. note::
  This message is emitted by the optional :ref:`'{message.checker}'<{message.checker_module_name}>`
  checker, which requires the ``{message.checker_module_name}`` plugin to be loaded.

"""
    return body


def _generate_checker_url(message: MessageData) -> str:
    checker_module_rel_path = os.path.relpath(
        message.checker_module_path, PYLINT_BASE_PATH
    )
    return f"https://github.com/pylint-dev/pylint/blob/main/{checker_module_rel_path}"


def _write_single_shared_message_page(
    category_dir: Path, messages: list[MessageData]
) -> None:
    message = messages[0]
    with open(category_dir / f"{message.name}.rst", "w", encoding="utf-8") as stream:
        stream.write(_generate_single_message_body(message))
        checker_urls = ", ".join(
            [
                f"`{message.checker} <{_generate_checker_url(message)}>`__"
                for message in messages
            ]
        )
        stream.write(f"Created by the {checker_urls} checkers.")


def _write_single_message_page(category_dir: Path, message: MessageData) -> None:
    with open(category_dir / f"{message.name}.rst", "w", encoding="utf-8") as stream:
        stream.write(_generate_single_message_body(message))
        checker_url = _generate_checker_url(message)
        stream.write(f"Created by the `{message.checker} <{checker_url}>`__ checker.")


def _write_messages_list_page(
    messages_dict: MessagesDict, old_messages_dict: OldMessagesDict
) -> None:
    """Create or overwrite the page with the list of all messages."""
    messages_file = os.path.join(PYLINT_MESSAGES_PATH, "messages_overview.rst")
    with open(messages_file, "w", encoding="utf-8") as stream:
        # Write header of file
        title = "Messages overview"
        stream.write(
            f"""
.. _messages-overview:

{"#" * len(title)}
{get_rst_title(title, "#")}

.. This file is auto-generated. Make any changes to the associated
.. docs extension in 'doc/exts/pylint_messages.py'.

Pylint can emit the following messages:

"""
        )
        # Iterate over tuple to keep same order
        for category in (
            "fatal",
            "error",
            "warning",
            "convention",
            "refactor",
            "information",
        ):
            # We need to remove all duplicated shared messages
            messages = sorted(
                {msg.id: msg for msg in messages_dict[category]}.values(),
                key=lambda item: item.name,
            )
            old_messages = sorted(old_messages_dict[category], key=lambda item: item[0])
            messages_string = "".join(
                f"   {category}/{message.name}\n" for message in messages
            )
            old_messages_string = "".join(
                f"   {category}/{old_message[0]}\n" for old_message in old_messages
            )
            # Write list per category. We need the '-category' suffix in the reference
            # because 'fatal' is also a message's symbol
            stream.write(
                f"""
.. _{category.lower()}-category:

{get_rst_title(category.capitalize(), "*")}
All messages in the {category} category:

.. toctree::
   :maxdepth: 2
   :titlesonly:

{messages_string}
All renamed messages in the {category} category:

.. toctree::
   :maxdepth: 1
   :titlesonly:

{old_messages_string}"""
            )


def _write_redirect_pages(old_messages: OldMessagesDict) -> None:
    """Create redirect pages for old-messages."""
    for category, old_names in old_messages.items():
        category_dir = PYLINT_MESSAGES_PATH / category
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
        for old_name, new_names in old_names.items():
            _write_redirect_old_page(category_dir, old_name, new_names)


def _write_redirect_old_page(
    category_dir: Path,
    old_name: tuple[str, str],
    new_names: list[tuple[str, str]],
) -> None:
    old_name_file = os.path.join(category_dir, f"{old_name[0]}.rst")
    new_names_string = "".join(
        f"   ../{new_name[1]}/{new_name[0]}.rst\n" for new_name in new_names
    )
    content = f""".. _{old_name[0]}:

{get_rst_title(" / ".join(old_name), "=")}
'{old_name[0]}' has been renamed. The new message can be found at:

.. toctree::
   :maxdepth: 2
   :titlesonly:

{new_names_string}
"""
    with open(old_name_file, "w", encoding="utf-8") as stream:
        stream.write(content)


# pylint: disable-next=unused-argument
def build_messages_pages(app: Sphinx | None) -> None:
    """Overwrite messages files by printing the documentation to a stream.

    Documentation is written in ReST format.
    """
    # Create linter, register all checkers and extensions and get all messages
    linter = PyLinter()
    _register_all_checkers_and_extensions(linter)
    messages, old_messages = _get_all_messages(linter)

    # Write message and category pages
    _write_message_page(messages)
    _write_messages_list_page(messages, old_messages)

    # Write redirect pages
    _write_redirect_pages(old_messages)


def setup(app: Sphinx) -> dict[str, bool]:
    """Connects the extension to the Sphinx process."""
    # Register callback at the builder-inited Sphinx event
    # See https://www.sphinx-doc.org/en/master/extdev/appapi.html
    app.connect("builder-inited", build_messages_pages)
    return {"parallel_read_safe": True}


if __name__ == "__main__":
    pass
    # Uncomment to allow running this script by your local python interpreter
    # build_messages_pages(None)
