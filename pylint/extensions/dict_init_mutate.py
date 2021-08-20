"""Check for use of dictionary mutation after intialization."""

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import IAstroidChecker


class DictInitMutateChecker(BaseChecker):

    __implements__ = (IAstroidChecker,)
    name = "dict-init-mutate"
    msgs = {
        "W0170": (
            "Dictionary mutated immediately after initialization",
            "dict-init-mutate",
            "Dictionaries can be initialized with a single statement"
            "using dictionary literal syntax.",
        )
    }

    @check_messages("dict-init-mutate")
    def visit_assign(self, node: nodes.Assign) -> None:
        # For now, we're just looking for the simple case in which the
        # dictionary is assigned to a name and that name is
        # subscripted and then mutated. Looking at nested instances
        # would be cool, but it's more # complicated.

        if not isinstance(node.value, nodes.Dict):
            return

        if len(node.targets) != 1:
            return

        if not isinstance((dict_name := node.targets[0]), nodes.AssignName):
            return

        if (sibling := node.next_sibling()) is None:
            return

        if not isinstance(sibling, nodes.Assign):
            return

        if len(sibling.targets) != 1:
            return

        if not isinstance((sibling_target := sibling.targets[0]), nodes.Subscript):
            return

        if not isinstance((sibling_name := sibling_target.value), nodes.Name):
            return

        if sibling_name.name == dict_name.name:
            self.add_message("dict-init-mutate", node=node)


def register(linter):
    """Required method to auto register this checker.

    :param linter: Main interface object for Pylint plugins
    :type linter: Pylint object
    """
    linter.register_checker(DictInitMutateChecker(linter))
