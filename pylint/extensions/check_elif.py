# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseTokenChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import HIGH, IAstroidChecker, ITokenChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class ElseifUsedChecker(BaseTokenChecker):
    """Checks for use of "else if" when an "elif" could be used."""

    __implements__ = (ITokenChecker, IAstroidChecker)
    name = "else_if_used"
    msgs = {
        "R5501": (
            'Consider using "elif" instead of "else" then "if" to remove one indentation level',
            "else-if-used",
            "Used when an else statement is immediately followed by "
            "an if statement and does not contain statements that "
            "would be unrelated to it.",
        )
    }

    def __init__(self, linter=None):
        super().__init__(linter)
        self._init()

    def _init(self):
        self._elifs = {}

    def process_tokens(self, tokens):
        """Process tokens and look for 'if' or 'elif'."""
        self._elifs = {
            begin: token for _, token, begin, _, _ in tokens if token in {"elif", "if"}
        }

    def leave_module(self, _: nodes.Module) -> None:
        self._init()

    @check_messages("else-if-used")
    def visit_if(self, node: nodes.If) -> None:
        """Current if node must directly follow an 'else'."""
        if (
            isinstance(node.parent, nodes.If)
            and node.parent.orelse == [node]
            and (node.lineno, node.col_offset) in self._elifs
            and self._elifs[(node.lineno, node.col_offset)] == "if"
        ):
            self.add_message("else-if-used", node=node, confidence=HIGH)


def register(linter: "PyLinter") -> None:
    linter.register_checker(ElseifUsedChecker(linter))
