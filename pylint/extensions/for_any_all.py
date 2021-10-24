"""Check for use of for loops that only check for a condition."""
from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages, returns_bool
from pylint.interfaces import IAstroidChecker


class ForAnyAllChecker(BaseChecker):

    __implements__ = (IAstroidChecker,)
    name = "consider-using-any-all"
    msgs = {
        "C0501": (
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
        if not returns_bool(if_children[1]):
            return

        # Check for terminating boolean return right after the loop
        node_after_loop = node.next_sibling()
        if returns_bool(node_after_loop):
            suggest_any = node_after_loop.value.value is False
            suggested_string = self._build_suggested_string(node, suggest_any)

            self.add_message("consider-using-any-all", node=node, args=suggested_string)

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
            # We could suggest an all statement with the condition negated, but negated any is easier
            suggested_function = "not any"
        suggested_string = (
            suggested_function + f"({test} for {loop_var} in {loop_iter})"
        )
        return suggested_string


def register(linter):
    """Required method to auto register this checker.

    :param linter: Main interface object for Pylint plugins
    :type linter: Pylint object
    """
    linter.register_checker(ForAnyAllChecker(linter))
