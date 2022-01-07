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
        "W4714": (
            "Iterated list '%s' is being modified inside loop body, consider iterating through a copy of it instead.",
            "iterating-modified-list",
            "Emitted when items are added or removed to a list being iterated through."
            "Doing so can result in unexpected behaviour, that is why it is preferred to use a copy of the list.",
        ),
        "E4714": (
            "Iterated dict '%s' is being modified inside loop body, iterate through a copy of it instead.",
            "iterating-modified-dict",
            "Emitted when items are added or removed to a dict being iterated through."
            "Doing so raises a RuntimeError",
        ),
        "E4715": (
            "Iterated set '%s' is being modified inside loop body, iterate through a copy of it instead.",
            "iterating-modified-set",
            "Emitted when items are added or removed to a set being iterated through."
            "Doing so raises a RuntimeError",
        ),
    }

    options = ()
    priority = -2

    @utils.check_messages(
        "iterating-modified-list", "iterating-modified-dict", "iterating-modified-set"
    )
    def visit_for(self, node: nodes.For) -> None:
        iter_obj = node.iter
        for body_node in node.body:
            if self._iterating_modified_list_cond(body_node, iter_obj):
                self.add_message(
                    "iterating-modified-list",
                    node=body_node,
                    args=(iter_obj.name,),
                )
            elif self._iterating_modified_dict_cond(body_node, iter_obj):
                self.add_message(
                    "iterating-modified-dict",
                    node=body_node,
                    args=(iter_obj.name,),
                )
            elif self._iterating_modified_set_cond(body_node, iter_obj):
                self.add_message(
                    "iterating-modified-set",
                    node=body_node,
                    args=(iter_obj.name,),
                )

    @staticmethod
    def _is_attribute_call_expr(body_node) -> bool:
        return (
            isinstance(body_node, astroid.Expr)
            and isinstance(body_node.value, astroid.Call)
            and isinstance(body_node.value.func, astroid.Attribute)
        )

    @classmethod
    def _common_cond_list_set(cls, node, list_obj, infer_val):
        return (
            cls._is_attribute_call_expr(node)
            and (infer_val == list_obj.inferred()[0])
            and (node.value.func.expr.name == list_obj.name)
        )

    @staticmethod
    def _dict_node_cond(node):
        return isinstance(node, astroid.Assign) and (
            isinstance(node.targets[0], astroid.Subscript)
        )

    @classmethod
    def _iterating_modified_list_cond(cls, node, list_obj):
        try:
            infer_val = next(node.value.func.expr.infer())
            return (
                cls._common_cond_list_set(node, list_obj, infer_val)
                and (infer_val.pytype() == "builtins.list")
                and node.value.func.attrname in {"append", "remove"}
            )
        except (astroid.InferenceError, AttributeError):
            return False

    @classmethod
    def _iterating_modified_dict_cond(cls, node, list_obj):
        try:
            infer_val = next(node.targets[0].value.infer())
            return (
                cls._dict_node_cond(node)
                and (infer_val.pytype() == "builtins.dict")
                and (infer_val == list_obj.inferred()[0])
                and (node.targets[0].value.name == list_obj.name)
            )
        except (astroid.InferenceError, AttributeError):
            return False

    @classmethod
    def _iterating_modified_set_cond(cls, node, list_obj):
        try:
            infer_val = next(node.value.func.expr.infer())
            return (
                cls._common_cond_list_set(node, list_obj, infer_val)
                and (infer_val.pytype() == "builtins.set")
                and node.value.func.attrname in {"add", "remove"}
            )
        except (astroid.InferenceError, AttributeError):
            return False


def register(linter: "PyLinter") -> None:
    linter.register_checker(ModifiedIterationChecker(linter))
