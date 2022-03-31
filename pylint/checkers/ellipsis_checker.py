# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Ellipsis checker for Python code."""
from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import IAstroidChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class EllipsisChecker(BaseChecker):
    __implements__ = (IAstroidChecker,)
    name = "unnecessary_ellipsis"
    msgs = {
        "W2301": (
            "Unnecessary ellipsis constant",
            "unnecessary-ellipsis",
            "Used when the ellipsis constant is encountered and can be avoided. "
            "A line of code consisting of an ellipsis is unnecessary if "
            "there is a docstring on the preceding line.",
        )
    }

    @check_messages("unnecessary-ellipsis")
    def visit_const(self, node: nodes.Const) -> None:
        """Check if the ellipsis constant is used unnecessarily.

        Emits a warning when:
         - A line consisting of an ellipsis is preceded by a docstring.
        """
        if (
            node.pytype() == "builtins.Ellipsis"
            and isinstance(node.parent, nodes.Expr)
            and (
                isinstance(node.parent.parent, (nodes.ClassDef, nodes.FunctionDef))
                and node.parent.parent.doc_node
            )
        ):
            self.add_message("unnecessary-ellipsis", node=node)


def register(linter: "PyLinter") -> None:
    linter.register_checker(EllipsisChecker(linter))
