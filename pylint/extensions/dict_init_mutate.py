"""Check for use of dictionary mutation after initialization."""

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages


class DictInitMutateChecker(BaseChecker):
    name = "dict-init-mutate"
    msgs = {
        "W0170": (
            "Dictionary mutated immediately after initialization",
            "dict-init-mutate",
            "Dictionaries can be initialized with a single statement"
            "using dictionary literal syntax.",
        )
    }

    @only_required_for_messages("dict-init-mutate")
    def visit_assign(self, node: nodes.Assign) -> None:
        """
        Detect dictionary mutation immediately after initialization.

        At this time, detecting nested mutation is not supported.
        """
        if not isinstance(node.value, nodes.Dict):
            return

        dict_name = node.targets[0]
        if len(node.targets) != 1 and not isinstance(dict_name, nodes.AssignName):
            return

        next_sibling = node.next_sibling()
        if not next_sibling or not isinstance(next_sibling, nodes.Assign) or len(next_sibling.targets) != 1:
            return

        sibling_target = next_sibling.targets[0]
        if not isinstance(sibling_target, nodes.Subscript):
            return

        sibling_name = sibling_target.value
        if not isinstance(sibling_name, nodes.Name):
            return

        if sibling_name.name == dict_name.name:
            self.add_message("dict-init-mutate", node=node)


def register(linter):
    """Required method to auto register this checker.

    :param linter: Main interface object for Pylint plugins
    :type linter: Pylint object
    """
    linter.register_checker(DictInitMutateChecker(linter))
