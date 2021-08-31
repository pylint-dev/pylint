"""Check for use of while loops."""
from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import IAstroidChecker


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


def register(linter):
    """Required method to auto register this checker.

    :param linter: Main interface object for Pylint plugins
    :type linter: Pylint object
    """
    linter.register_checker(WhileChecker(linter))
