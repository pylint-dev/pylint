# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class LambdaExpressionChecker(BaseChecker):
    """Check for manual __magic__ method calls."""

    __implements__ = IAstroidChecker

    name = "lambda-expressions"
    priority = -1
    msgs = {
        "C2901": (
            'Lambda expression is assigned to a variable. '
            'Define a function using the "def" keyword instead.',
            "lambda-assignment",
            'Used when a lambda expression is assigned to variable '
            'rather than defining a standard function with the "def" keyword.',
        ),
        "C2902": (
            "Lambda expression is called directly. If the lambda expression is "
            "used only once then just put the expression inline instead.",
            "lambda-call",
            "Used when a lambda expression is directly called "
            "rather than executing it's contents inline.",
        ),
    }
    options = ()

    def visit_lambda(self, node: nodes.Call) -> None:
        """Check if method being called uses __magic__ method naming convention."""
        if (
            isinstance(node.func, nodes.Attribute)
            and node.func.attrname in self.includedict
        ):
            self.add_message(
                "lambda-assignment",
                node=node,
            )


def register(linter: "PyLinter") -> None:
    linter.register_checker(LambdaExpressionChecker(linter))
