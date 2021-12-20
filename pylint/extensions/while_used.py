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
    """This required method auto registers the checker during initialization.

    :param linter: The linter to register the checker to.
    """
    linter.register_checker(WhileChecker(linter))
