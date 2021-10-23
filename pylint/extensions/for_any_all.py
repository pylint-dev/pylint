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
            "`for` loop could be %s",
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
        node_after_loop = node.next_sibling()
        if self._node_returns_bool(node_after_loop):
            suggest_any = node_after_loop.value.value is False
            suggested_string = self._build_suggested_string(node, suggest_any)

            self.add_message("consider-using-any-all", node=node, args=suggested_string)

    @staticmethod
    def _node_returns_bool(node):
        """Checks whether a node is a return that returns a constant boolean"""
        return (
            isinstance(node, nodes.Return)
            and isinstance(node.value, nodes.Const)
            and node.value.value in (True, False)
        )

    @staticmethod
    def _build_suggested_string(node, suggest_any):
        """Given nodes.For node can be rewritten as an any/all statement, return a suggestion for that statement
        suggest_any is True if the proposed statement should be a call to any()
        Provides a generic suggestion if the length of the suggestion would be too long.
        """
        loop_var = node.target.as_string()
        loop_iter = node.iter.as_string()
        test_node = next(node.body[0].get_children())
        test = test_node.as_string()
        if suggest_any:
            suggested_function = "any"
        else:
            suggested_function = "all"
            # If the original test has is a compound boolean, wrap in parens
            if isinstance(test_node, nodes.BoolOp):
                test = f"not ({test})"
            else:
                test = f"not {test}"
        suggested_string = (
            suggested_function + f"({test} for {loop_var} in {loop_iter})"
        )
        if len(suggested_string) > 100:
            suggested_string = "any/all statement with a generator"
        return suggested_string


def register(linter):
    """Required method to auto register this checker.

    :param linter: Main interface object for Pylint plugins
    :type linter: Pylint object
    """
    linter.register_checker(ForAnyAllChecker(linter))
