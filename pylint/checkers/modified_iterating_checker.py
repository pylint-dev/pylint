# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

from typing import TYPE_CHECKING

import astroid
from astroid import nodes

from pylint import checkers, interfaces
from pylint.checkers import utils

if TYPE_CHECKING:
    from pylint.lint import PyLinter


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
            "Doing so ccan result in unexpected behaviour, that is why it is preferred to use a copy of the list.",
        ),
        "E4702": (
            "Iterated dict '%s' is being modified inside loop body, iterate through a copy of it instead.",
            "modified-iterating-dict",
            "Emitted when items are added or removed to a dict being iterated through. "
            "Doing so raises a RuntimeError",
        ),
        "E4703": (
            "Iterated set '%s' is being modified inside loop body, iterate through a copy of it instead.",
            "modified-iterating-set",
            "Emitted when items are added or removed to a set being iterated through. "
            "Doing so raises a RuntimeError",
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
                )
                break  # since the msg is raised for the `for` node no further check is needed

    @staticmethod
    def _is_attribute_call_expr(body_node) -> bool:
        return (
            isinstance(body_node, astroid.Expr)
            and isinstance(body_node.value, astroid.Call)
            and isinstance(body_node.value.func, astroid.Attribute)
        )

    @classmethod
    def _common_cond_list_set(cls, node, list_obj, infer_val) -> bool:
        try:
            return (infer_val == utils.safe_infer(list_obj)) and (
                node.value.func.expr.name == list_obj.name
            )
        except AttributeError:
            return False

    @staticmethod
    def _dict_node_cond(node) -> bool:
        return isinstance(node, astroid.Assign) and (
            isinstance(node.targets[0], astroid.Subscript)
        )

    @classmethod
    def _modified_iterating_list_cond(cls, node, list_obj) -> bool:
        if not cls._is_attribute_call_expr(node):
            return False
        infer_val = utils.safe_infer(node.value.func.expr)
        if infer_val is None or infer_val.pytype() != "builtins.list":
            # Uninferable or not a list
            return False
        return cls._common_cond_list_set(
            node, list_obj, infer_val
        ) and node.value.func.attrname in {"append", "remove"}

    @classmethod
    def _modified_iterating_dict_cond(cls, node, list_obj) -> bool:
        if not cls._dict_node_cond(node):
            return False
        infer_val = utils.safe_infer(node.targets[0].value)
        if infer_val is None or infer_val.pytype() != "builtins.dict":
            # Uninferable or not a dict
            return False
        if infer_val != utils.safe_infer(list_obj):
            return False
        try:
            return node.targets[0].value.name == list_obj.name
        except AttributeError:
            return False

    @classmethod
    def _modified_iterating_set_cond(cls, node, list_obj) -> bool:
        if not cls._is_attribute_call_expr(node):
            return False
        infer_val = utils.safe_infer(node.value.func.expr)
        if infer_val is None or infer_val.pytype() != "builtins.set":
            # Uninferable or not a set
            return False
        return cls._common_cond_list_set(
            node, list_obj, infer_val
        ) and node.value.func.attrname in {"add", "remove"}


def register(linter: "PyLinter") -> None:
    linter.register_checker(ModifiedIterationChecker(linter))
