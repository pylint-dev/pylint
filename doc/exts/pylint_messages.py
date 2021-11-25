# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Script used to generate the messages files."""

import os
from typing import Dict, List, NamedTuple, Optional

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


def _register_all_checkers_and_extensions(linter: PyLinter) -> None:
    """Registers all checkers and extensions found in the default folders."""
    initialize_checkers(linter)
    initialize_extensions(linter)


def _get_all_messages(linter: PyLinter) -> Dict[str, List[MessageData]]:
    """Get all messages registered to a linter and return a dictionary indexed by message
    type.
    """
    messages_dict: Dict[str, List[MessageData]] = {
        "fatal": [],
        "error": [],
        "warning": [],
        "convention": [],
        "refactor": [],
        "information": [],
    }
    for checker in linter.get_checkers():
        for message in checker.messages:
            message_data = MessageData(
                checker.name, message.msgid, message.symbol, message
            )
            messages_dict[MSG_TYPES[message.msgid[0]]].append(message_data)

    return messages_dict


def _write_message_page(messages_dict: Dict[str, List[MessageData]]) -> None:
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


def _write_category_page(messages_dict: Dict[str, List[MessageData]]) -> None:
    """Create or overwrite the file for each category."""
    for category, messages in messages_dict.items():
        category_file = os.path.join(
            PYLINT_BASE_PATH, "doc", "messages", f"{category}.rst"
        )
        with open(category_file, "w", encoding="utf-8") as stream:
            stream.write(f".. _category-{category}:\n\n")
            stream.write(get_rst_title(category.capitalize(), "="))
            stream.write("\n")
            stream.write(f"All messages in the {category} category:\n\n")
            stream.write(".. toctree::\n")
            stream.write("   :maxdepth: 2\n")
            stream.write("   :titlesonly:\n")
            stream.write("\n")
            for message in sorted(messages, key=lambda item: item.name):
                stream.write(f"   {category}/{message.name}.rst\n")


# pylint: disable-next=unused-argument
def build_messages_pages(app: Optional[Sphinx]) -> None:
    """Overwrite messages files by printing the documentation to a stream.
    Documentation is written in ReST format.
    """
    # Create linter, register all checkers and extensions and get all messages
    linter = PyLinter()
    _register_all_checkers_and_extensions(linter)
    messages = _get_all_messages(linter)

    # Write message and category pages
    _write_message_page(messages)
    _write_category_page(messages)


def setup(app: Sphinx) -> None:
    """Connects the extension to the Sphinx process"""
    # Register callback at the builder-inited Sphinx event
    # See https://www.sphinx-doc.org/en/master/extdev/appapi.html
    app.connect("builder-inited", build_messages_pages)


if __name__ == "__main__":
    # Uncomment to allow running this script by your local python interpreter
    # build_messages_pages(None)
    pass
