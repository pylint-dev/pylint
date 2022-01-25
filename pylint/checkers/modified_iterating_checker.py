# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

from typing import TYPE_CHECKING, Optional

from astroid import nodes

from pylint import checkers, interfaces
from pylint.checkers import utils

if TYPE_CHECKING:
    from pylint.lint import PyLinter


__LIST_MODIFIER_METHODS__ = {"append", "remove"}
__SET_MODIFIER_METHODS__ = {"add", "remove"}


class ModifiedIterationChecker(checkers.BaseChecker):
    """Checks for modified for loops iterations

    Currently supports `for` loops for Sets, Dictionaries and Lists.
    """

    __implements__ = interfaces.IAstroidChecker

    name = "modified_iteration"

    msgs = {
        "W4701": (
            "Iterated list '%s' is being modified inside loop body, consider iterating through a copy of it instead.",
            "modified-iterating-list",
            "Emitted when items are added or removed to a list being iterated through. "
            "Doing so can result in unexpected behaviour, that is why it is preferred to use a copy of the list.",
        ),
        "E4702": (
            "Iterated dict '%s' is being modified inside loop body, iterate through a copy of it instead.",
            "modified-iterating-dict",
            "Emitted when items are added or removed to a dict being iterated through. "
            "Doing so raises a RuntimeError.",
        ),
        "E4703": (
            "Iterated set '%s' is being modified inside loop body, iterate through a copy of it instead.",
            "modified-iterating-set",
            "Emitted when items are added or removed to a set being iterated through. "
            "Doing so raises a RuntimeError.",
        ),
    }

    options = ()
    priority = -2

    @utils.check_messages(
        "modified-iterating-list", "modified-iterating-dict", "modified-iterating-set"
    )
    def visit_for(self, node: nodes.For) -> None:
        iter_obj = node.iter
        for body_node in node.body:
            msg_id = None
            if self._modified_iterating_list_cond(body_node, iter_obj):
                msg_id = "modified-iterating-list"
            elif self._modified_iterating_dict_cond(body_node, iter_obj):
                msg_id = "modified-iterating-dict"
            elif self._modified_iterating_set_cond(body_node, iter_obj):
                msg_id = "modified-iterating-set"
            if msg_id is not None:
                self.add_message(
                    msg_id,
                    node=node,
                    args=(iter_obj.name,),
                    confidence=interfaces.INFERENCE,
                )
                break  # since the msg is raised for the `for` node no further check is needed

    @staticmethod
    def _is_node_expr_calls_attribute_name(node: nodes.NodeNG) -> bool:
        return (
            isinstance(node, nodes.Expr)
            and isinstance(node.value, nodes.Call)
            and isinstance(node.value.func, nodes.Attribute)
            and isinstance(node.value.func.expr, nodes.Name)
        )

    @classmethod
    def _common_cond_list_set(
        cls,
        node: nodes.NodeNG,
        list_obj: nodes.NodeNG,
        infer_val: Optional[nodes.NodeNG],
    ) -> bool:
        return (infer_val == utils.safe_infer(list_obj)) and (
            node.value.func.expr.name == list_obj.name
        )

    @staticmethod
    def _is_node_assigns_subscript_name(node: nodes.NodeNG) -> bool:
        return isinstance(node, nodes.Assign) and (
            isinstance(node.targets[0], nodes.Subscript)
            and (isinstance(node.targets[0].value, nodes.Name))
        )

    @classmethod
    def _modified_iterating_list_cond(
        cls, node: nodes.NodeNG, list_obj: nodes.NodeNG
    ) -> bool:
        if not cls._is_node_expr_calls_attribute_name(node):
            return False
        infer_val = utils.safe_infer(node.value.func.expr)
        if not isinstance(infer_val, nodes.List):
            return False
        return (
            cls._common_cond_list_set(node, list_obj, infer_val)
            and node.value.func.attrname in __LIST_MODIFIER_METHODS__
        )

    @classmethod
    def _modified_iterating_dict_cond(
        cls, node: nodes.NodeNG, list_obj: nodes.NodeNG
    ) -> bool:
        if not cls._is_node_assigns_subscript_name(node):
            return False
        infer_val = utils.safe_infer(node.targets[0].value)
        if not isinstance(infer_val, nodes.Dict):
            return False
        if infer_val != utils.safe_infer(list_obj):
            return False
        return node.targets[0].value.name == list_obj.name

    @classmethod
    def _modified_iterating_set_cond(
        cls, node: nodes.NodeNG, list_obj: nodes.NodeNG
    ) -> bool:
        if not cls._is_node_expr_calls_attribute_name(node):
            return False
        infer_val = utils.safe_infer(node.value.func.expr)
        if not isinstance(infer_val, nodes.Set):
            return False
        return (
            cls._common_cond_list_set(node, list_obj, infer_val)
            and node.value.func.attrname in __SET_MODIFIER_METHODS__
        )


def register(linter: "PyLinter") -> None:
    linter.register_checker(ModifiedIterationChecker(linter))
