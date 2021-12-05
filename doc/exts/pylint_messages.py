# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Script used to generate the messages files."""

import os
from collections import defaultdict
from typing import DefaultDict, Dict, List, NamedTuple, Optional, Tuple

from sphinx.application import Sphinx

from pylint.checkers import initialize as initialize_checkers
from pylint.extensions import initialize as initialize_extensions
from pylint.lint import PyLinter
from pylint.message import MessageDefinition
from pylint.utils import get_rst_title

# PACKAGE/docs/exts/pylint_extensions.py --> PACKAGE/
PYLINT_BASE_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
"""Base path to the project folder"""


MSG_TYPES = {
    "I": "information",
    "C": "convention",
    "R": "refactor",
    "W": "warning",
    "E": "error",
    "F": "fatal",
}


class MessageData(NamedTuple):
    checker: str
    id: str
    name: str
    definition: MessageDefinition


MessagesDict = Dict[str, List[MessageData]]
OldMessagesDict = Dict[str, DefaultDict[Tuple[str, str], List[Tuple[str, str]]]]
"""DefaultDict is indexed by tuples of (old name symbol, old name id) and values are
tuples of (new name symbol, new name category)
"""


def _register_all_checkers_and_extensions(linter: PyLinter) -> None:
    """Registers all checkers and extensions found in the default folders."""
    initialize_checkers(linter)
    initialize_extensions(linter)


def _get_all_messages(
    linter: PyLinter,
) -> Tuple[MessagesDict, OldMessagesDict]:
    """Get all messages registered to a linter and return a dictionary indexed by message
    type.
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
    for message in linter.msgs_store.messages:
        message_data = MessageData(
            message.checker_name, message.msgid, message.symbol, message
        )
        messages_dict[MSG_TYPES[message.msgid[0]]].append(message_data)

        if message.old_names:
            for old_name in message.old_names:
                category = MSG_TYPES[old_name[0][0]]
                old_messages[category][(old_name[1], old_name[0])].append(
                    (message.symbol, MSG_TYPES[message.msgid[0]])
                )

    return messages_dict, old_messages


def _write_message_page(messages_dict: MessagesDict) -> None:
    """Create or overwrite the file for each message."""
    for category, messages in messages_dict.items():
        category_dir = os.path.join(PYLINT_BASE_PATH, "doc", "messages", category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
        for message in messages:
            messages_file = os.path.join(category_dir, f"{message.name}.rst")
            with open(messages_file, "w", encoding="utf-8") as stream:
                stream.write(f".. _{message.name}:\n\n")
                stream.write(get_rst_title(f"{message.name} / {message.id}", "="))
                stream.write("**Message emitted:**\n\n")
                stream.write(f"{message.definition.msg}\n\n")
                stream.write("**Description:**\n\n")
                stream.write(f"*{message.definition.description}*\n\n")
                stream.write(f"Created by ``{message.checker}`` checker\n")


def _write_messages_list_page(
    messages_dict: MessagesDict, old_messages_dict: OldMessagesDict
) -> None:
    """Create or overwrite the page with the list of all messages."""
    messages_file = os.path.join(
        PYLINT_BASE_PATH, "doc", "messages", "messages_list.rst"
    )
    with open(messages_file, "w", encoding="utf-8") as stream:
        stream.write(".. _messages-list:\n\n")
        stream.write(get_rst_title("Pylint Messages", "="))
        stream.write("\n")
        stream.write("Pylint can emit the following messages:\n")
        stream.write("\n")
        # Iterate over tuple to keep same order
        for category in (
            "fatal",
            "error",
            "warning",
            "convention",
            "refactor",
            "information",
        ):
            messages = messages_dict[category]
            old_messages = old_messages_dict[category]
            stream.write(get_rst_title(category.capitalize(), "-"))
            stream.write("\n")
            stream.write(f"All messages in the {category} category:\n\n")
            stream.write(".. toctree::\n")
            stream.write("   :maxdepth: 2\n")
            stream.write("   :titlesonly:\n")
            stream.write("\n")
            for message in sorted(messages, key=lambda item: item.name):
                stream.write(f"   {category}/{message.name}.rst\n")
            stream.write("\n")
            stream.write(f"All renamed messages in the {category} category:\n\n")
            stream.write(".. toctree::\n")
            stream.write("   :maxdepth: 1\n")
            stream.write("   :titlesonly:\n")
            stream.write("\n")
            for old_message in sorted(old_messages, key=lambda item: item[0]):
                stream.write(f"   {category}/{old_message[0]}.rst\n")
            stream.write("\n\n")


def _write_redirect_pages(old_messages: OldMessagesDict) -> None:
    """Create redirect pages for old-messages."""
    for category, old_names in old_messages.items():
        category_dir = os.path.join(PYLINT_BASE_PATH, "doc", "messages", category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
        for old_name, new_names in old_names.items():
            old_name_file = os.path.join(category_dir, f"{old_name[0]}.rst")
            with open(old_name_file, "w", encoding="utf-8") as stream:
                stream.write(f".. _{old_name[0]}:\n\n")
                stream.write(get_rst_title(" / ".join(old_name), "="))
                stream.write(
                    f"{old_name[0]} has been renamed. The new message can "
                    "be found at:\n\n"
                )
                stream.write(".. toctree::\n")
                stream.write("   :maxdepth: 2\n")
                stream.write("   :titlesonly:\n")
                stream.write("\n")
                for new_name in new_names:
                    stream.write(f"   ../{new_name[1]}/{new_name[0]}.rst\n")


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
    """Connects the extension to the Sphinx process"""
    # Register callback at the builder-inited Sphinx event
    # See https://www.sphinx-doc.org/en/master/extdev/appapi.html
    app.connect("builder-inited", build_messages_pages)


if __name__ == "__main__":
    pass
    # Uncomment to allow running this script by your local python interpreter
    # build_messages_pages(None)
