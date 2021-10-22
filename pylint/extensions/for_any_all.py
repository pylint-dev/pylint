"""Check for use of for loops that only check for a condition."""
from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import IAstroidChecker


class ForAnyAllChecker(BaseChecker):

    __implements__ = (IAstroidChecker,)
    name = "consider-using-any-all"
    msgs = {
        "W2101": (
            "`for` loop could be any/all",
            "consider-using-any-all",
            "For loops that check for a condition and return a bool can be replaced with any/all.",
        )
    }

    @check_messages("consider-using-any-all")
    def visit_for(self, node: nodes.For) -> None:
        if len(node.body) != 1:  # Only If node with no Else
            return
        if not isinstance(node.body[0], nodes.If):
            return

        if_children = list(node.body[0].get_children())
        if not len(if_children) == 2:  # The If node has only a comparison and return
            return
        if not self._node_returns_bool(if_children[1]):
            return

        # Check for terminating boolean return right after the loop
        if self._node_returns_bool(node.next_sibling()):
            self.add_message("consider-using-any-all", node=node)

    @staticmethod
    def _node_returns_bool(node):
        """Checks whether a node is a return that returns a constant boolean"""
        return (
            isinstance(node, nodes.Return)
            and isinstance(node.value, nodes.Const)
            and node.value.value in (True, False)
        )


def register(linter):
    """Required method to auto register this checker.

    :param linter: Main interface object for Pylint plugins
    :type linter: Pylint object
    """
    linter.register_checker(ForAnyAllChecker(linter))
