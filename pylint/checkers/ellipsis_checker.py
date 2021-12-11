"""Ellipsis checker for Python code
"""
from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter


class EllipsisChecker(BaseChecker):
    __implements__ = (IAstroidChecker,)
    name = "unnecessary_ellipsis"
    msgs = {
        "W1801": (
            "Unnecessary ellipsis constant",
            "unnecessary-ellipsis",
            "Used when the ellipsis constant is encountered and can be avoided.",
        )
    }

    @check_messages("unnecessary-ellipsis")
    def visit_const(self, node: nodes.Const) -> None:
        """Check if the ellipsis constant is used unnecessarily"""
        if (
            node.pytype() == "builtins.Ellipsis"
            and not isinstance(node.parent, (nodes.Assign, nodes.AnnAssign, nodes.Call))
            and (
                len(node.parent.parent.child_sequence(node.parent)) > 1
                or (
                    isinstance(node.parent.parent, (nodes.ClassDef, nodes.FunctionDef))
                    and (node.parent.parent.doc is not None)
                )
            )
        ):
            self.add_message("unnecessary-ellipsis", node=node)


def register(linter: PyLinter) -> None:
    """required method to auto register this checker"""
    linter.register_checker(EllipsisChecker(linter))
