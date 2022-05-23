# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Script used to generate the messages files."""

import os
from collections import defaultdict
from inspect import getmodule
from itertools import chain
from pathlib import Path
from typing import DefaultDict, Dict, List, NamedTuple, Optional, Tuple

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


class MessageData(NamedTuple):
    checker: str
    id: str
    name: str
    definition: MessageDefinition
    good_code: str
    bad_code: str
    details: str
    related_links: str
    checker_module_name: str
    checker_module_path: str


MessagesDict = Dict[str, List[MessageData]]
OldMessagesDict = Dict[str, DefaultDict[Tuple[str, str], List[Tuple[str, str]]]]
"""DefaultDict is indexed by tuples of (old name symbol, old name id) and values are
tuples of (new name symbol, new name category).
"""


def _register_all_checkers_and_extensions(linter: PyLinter) -> None:
    """Registers all checkers and extensions found in the default folders."""
    initialize_checkers(linter)
    initialize_extensions(linter)


def _get_message_data(data_path: Path) -> Tuple[str, str, str, str]:
    """Get the message data from the specified path."""
    good_code, bad_code, details, related = "", "", "", ""

    if not data_path.exists():
        return good_code, bad_code, details, related

    if (data_path / "good.py").exists():
        with open(data_path / "good.py", encoding="utf-8") as file:
            file_content = file.readlines()
            indented_file_content = "".join("  " + i for i in file_content)
            good_code = f"""
**Correct code:**

.. code-block:: python

{indented_file_content}"""

    if (data_path / "bad.py").exists():
        with open(data_path / "bad.py", encoding="utf-8") as file:
            file_content = file.readlines()
            indented_file_content = "".join("  " + i for i in file_content)
            bad_code = f"""
**Problematic code:**

.. code-block:: python

{indented_file_content}"""

    if (data_path / "details.rst").exists():
        with open(data_path / "details.rst", encoding="utf-8") as file:
            file_content_string = file.read()
            details = f"""
**Additional details:**

{file_content_string}"""

    if (data_path / "related.rst").exists():
        with open(data_path / "related.rst", encoding="utf-8") as file:
            file_content_string = file.read()
            related = f"""
**Related links:**

{file_content_string}"""

    return good_code, bad_code, details, related


def _get_all_messages(
    linter: PyLinter,
) -> Tuple[MessagesDict, OldMessagesDict]:
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
        message_data_path = (
            PYLINT_MESSAGES_DATA_PATH / message.symbol[0] / message.symbol
        )
        good_code, bad_code, details, related = _get_message_data(message_data_path)

        checker_module = getmodule(checker)

        assert (
            checker_module and checker_module.__file__
        ), f"Cannot find module for checker {checker}"

        message_data = MessageData(
            message.checker_name,
            message.msgid,
            message.symbol,
            message,
            good_code,
            bad_code,
            details,
            related,
            checker_module.__name__,
            checker_module.__file__,
        )
        msg_type = MSG_TYPES_DOC[message.msgid[0]]
        messages_dict[msg_type].append(message_data)
        if message.old_names:
            for old_name in message.old_names:
                category = MSG_TYPES_DOC[old_name[0][0]]
                old_messages[category][(old_name[1], old_name[0])].append(
                    (message.symbol, msg_type)
                )

    return messages_dict, old_messages


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
            if not _message_needs_update(message, category):
                continue
            _write_single_message_page(category_dir, message)


def _write_single_message_page(category_dir: Path, message: MessageData) -> None:
    checker_module_rel_path = os.path.relpath(
        message.checker_module_path, PYLINT_BASE_PATH
    )
    messages_file = os.path.join(category_dir, f"{message.name}.rst")
    with open(messages_file, "w", encoding="utf-8") as stream:
        stream.write(
            f""".. _{message.name}:

{get_rst_title(f"{message.name} / {message.id}", "=")}
**Message emitted:**

{message.definition.msg}

**Description:**

*{message.definition.description}*

{message.good_code}
{message.bad_code}
{message.details}
{message.related_links}
"""
        )
        if message.checker_module_name.startswith("pylint.extensions."):
            stream.write(
                f"""
.. note::
  This message is emitted by the optional :ref:`'{message.checker}'<{message.checker_module_name}>` checker which requires the ``{message.checker_module_name}``
  plugin to be loaded.

"""
            )
        checker_url = (
            f"https://github.com/PyCQA/pylint/blob/main/{checker_module_rel_path}"
        )
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
            messages = sorted(messages_dict[category], key=lambda item: item.name)
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
            old_name_file = os.path.join(category_dir, f"{old_name[0]}.rst")
            with open(old_name_file, "w", encoding="utf-8") as stream:
                new_names_string = "".join(
                    f"   ../{new_name[1]}/{new_name[0]}.rst\n" for new_name in new_names
                )
                stream.write(
                    f""".. _{old_name[0]}:

{get_rst_title(" / ".join(old_name), "=")}
"{old_name[0]} has been renamed. The new message can be found at:

.. toctree::
   :maxdepth: 2
   :titlesonly:

{new_names_string}
"""
                )


# pylint: disable-next=unused-argument
def build_messages_pages(app: Optional[Sphinx]) -> None:
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


def setup(app: Sphinx) -> None:
    """Connects the extension to the Sphinx process."""
    # Register callback at the builder-inited Sphinx event
    # See https://www.sphinx-doc.org/en/master/extdev/appapi.html
    app.connect("builder-inited", build_messages_pages)


if __name__ == "__main__":
    pass
    # Uncomment to allow running this script by your local python interpreter
    # build_messages_pages(None)
