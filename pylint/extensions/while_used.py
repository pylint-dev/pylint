# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Check for use of while loops."""
from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import IAstroidChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class WhileChecker(BaseChecker):

    __implements__ = (IAstroidChecker,)
    name = "while_used"
    msgs = {
        "W0149": (
            "Used `while` loop",
            "while-used",
            "Unbounded `while` loops can often be rewritten as bounded `for` loops.",
        )
    }

    @check_messages("while-used")
    def visit_while(self, node: nodes.While) -> None:
        self.add_message("while-used", node=node)


def register(linter: "PyLinter") -> None:
    linter.register_checker(WhileChecker(linter))
