"""Small script to get a new unused message id category"""
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

from typing import List

from pylint.checkers import initialize as initialize_checkers
from pylint.extensions import initialize as initialize_extensions
from pylint.lint.pylinter import PyLinter


def register_all_checkers_and_plugins(linter: "PyLinter") -> None:
    """Registers all checkers and plugins"""
    linter.cmdline_parser.set_conflict_handler("resolve")
    initialize_checkers(linter)
    initialize_extensions(linter)


def get_next_code_category(message_ids: List[str]) -> int:
    categories = sorted({int(i[:2]) for i in message_ids})
    for i in categories:
        if i + 1 not in categories:
            return i + 1
    return categories[-1] + 1


if __name__ == "__main__":
    pylinter = PyLinter()
    register_all_checkers_and_plugins(pylinter)
    messages = sorted(i.msgid[1:] for i in pylinter.msgs_store.messages)
    next_category = get_next_code_category(messages)
    print(f"Next free message id category is {next_category:02}")
    print(f"Please use {next_category:02}01 for the first message of the new checker")
