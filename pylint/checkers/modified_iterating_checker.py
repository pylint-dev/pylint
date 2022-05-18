# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from typing import TYPE_CHECKING

import astroid
from astroid import nodes

from pylint import checkers, interfaces
from pylint.checkers import BaseChecker, utils

if TYPE_CHECKING:
    from pylint.lint import PyLinter


_LIST_MODIFIER_METHODS = {"append", "remove"}
_SET_MODIFIER_METHODS = {"add", "remove"}


class ModifiedIterationChecker(checkers.BaseChecker):
    """Checks for modified iterators in for loops iterations.

    Currently supports `for` loops for Sets, Dictionaries and Lists.
    """

    name = "modified_iteration"

    msgs = {
        "W4701": (
            "Iterated list '%s' is being modified inside for loop body, consider iterating through a copy of it "
            "instead.",
            "modified-iterating-list",
            "Emitted when items are added or removed to a list being iterated through. "
            "Doing so can result in unexpected behaviour, that is why it is preferred to use a copy of the list.",
        ),
        "E4702": (
            "Iterated dict '%s' is being modified inside for loop body, iterate through a copy of it instead.",
            "modified-iterating-dict",
            "Emitted when items are added or removed to a dict being iterated through. "
            "Doing so raises a RuntimeError.",
        ),
        "E4703": (
            "Iterated set '%s' is being modified inside for loop body, iterate through a copy of it instead.",
            "modified-iterating-set",
            "Emitted when items are added or removed to a set being iterated through. "
            "Doing so raises a RuntimeError.",
        ),
    }

    options = ()

    @utils.only_required_for_messages(
        "modified-iterating-list", "modified-iterating-dict", "modified-iterating-set"
    )
    def visit_for(self, node: nodes.For) -> None:
        iter_obj = node.iter
        if isinstance(iter_obj, nodes.Name):
            for body_node in node.body:
                self._modified_iterating_check_on_node_and_children(body_node, iter_obj)

    def _modified_iterating_check_on_node_and_children(
        self, body_node: nodes.NodeNG, iter_obj: nodes.NodeNG
    ) -> None:
        """See if node or any of its children raises modified iterating messages."""
        self._modified_iterating_check(body_node, iter_obj)
        for child in body_node.get_children():
            self._modified_iterating_check_on_node_and_children(child, iter_obj)

    def _modified_iterating_check(
        self, node: nodes.NodeNG, iter_obj: nodes.NodeNG
    ) -> None:
        msg_id = None
        if self._modified_iterating_list_cond(node, iter_obj):
            msg_id = "modified-iterating-list"
        elif self._modified_iterating_dict_cond(node, iter_obj):
            msg_id = "modified-iterating-dict"
        elif self._modified_iterating_set_cond(node, iter_obj):
            msg_id = "modified-iterating-set"
        if msg_id:
            self.add_message(
                msg_id,
                node=node,
                args=(iter_obj.name,),
                confidence=interfaces.INFERENCE,
            )

    @staticmethod
    def _is_node_expr_that_calls_attribute_name(node: nodes.NodeNG) -> bool:
        return (
            isinstance(node, nodes.Expr)
            and isinstance(node.value, nodes.Call)
            and isinstance(node.value.func, nodes.Attribute)
            and isinstance(node.value.func.expr, nodes.Name)
        )

    @staticmethod
    def _common_cond_list_set(
        node: nodes.Expr,
        iter_obj: nodes.NodeNG,
        infer_val: nodes.List | nodes.Set,
    ) -> bool:
        return (infer_val == utils.safe_infer(iter_obj)) and (
            node.value.func.expr.name == iter_obj.name
        )

    @staticmethod
    def _is_node_assigns_subscript_name(node: nodes.NodeNG) -> bool:
        return isinstance(node, nodes.Assign) and (
            isinstance(node.targets[0], nodes.Subscript)
            and (isinstance(node.targets[0].value, nodes.Name))
        )

    def _modified_iterating_list_cond(
        self, node: nodes.NodeNG, iter_obj: nodes.NodeNG
    ) -> bool:
        if not self._is_node_expr_that_calls_attribute_name(node):
            return False
        infer_val = utils.safe_infer(node.value.func.expr)
        if not isinstance(infer_val, nodes.List):
            return False
        return (
            self._common_cond_list_set(node, iter_obj, infer_val)
            and node.value.func.attrname in _LIST_MODIFIER_METHODS
        )

    def _modified_iterating_dict_cond(
        self, node: nodes.NodeNG, iter_obj: nodes.NodeNG
    ) -> bool:
        if not self._is_node_assigns_subscript_name(node):
            return False
        infer_val = utils.safe_infer(node.targets[0].value)
        if not isinstance(infer_val, nodes.Dict):
            return False
        if infer_val != utils.safe_infer(iter_obj):
            return False
        return node.targets[0].value.name == iter_obj.name

    def _modified_iterating_set_cond(
        self, node: nodes.NodeNG, iter_obj: nodes.NodeNG
    ) -> bool:
        if not self._is_node_expr_that_calls_attribute_name(node):
            return False
        infer_val = utils.safe_infer(node.value.func.expr)
        if not isinstance(infer_val, nodes.Set):
            return False
        return (
            self._common_cond_list_set(node, iter_obj, infer_val)
            and node.value.func.attrname in _SET_MODIFIER_METHODS
        )


class ChangedIterateeChecker(BaseChecker):
    msgs = {
        "E0130": (
            "Iterated object %r is modified inside the loop",
            "changed-iteratee",
            "Used when iterated object is modified " "inside the loop.",
        ),
    }

    class _LoopContext:
        def __init__(self, node, klass, name):
            self._node = node
            self._klass = klass
            self._name = name

    def __init__(self, linter):
        BaseChecker.__init__(self, linter)
        self._loops = []

    @staticmethod
    def _locate_iterated_objects(node):
        # TODO: other classes which provide __iter__ ?
        if isinstance(node, astroid.Name):
            klass = utils.safe_infer(node)
            if isinstance(klass, astroid.Dict) or isinstance(klass, astroid.List):
                return ChangedIterateeChecker._LoopContext(node, klass, node.name)
            if (
                isinstance(node, astroid.Call)
                and isinstance(node.func, astroid.Attribute)
                and isinstance(node.func.expr, astroid.Name)
            ):
                # Look for dict.values, dict.items or dict.keys
                expr = node.func.expr
                klass = utils.safe_infer(expr)
        if isinstance(klass, astroid.Dict) and node.func.attrname in (
            "keys",
            "values",
            "items",
        ):
            return ChangedIterateeChecker._LoopContext(node, klass, node.func.expr.name)
        return None

        def visit_for(self, node):
            self._loops.append(self._locate_iterated_objects(node.iter))

        def leave_for(self, node):
            self._loops.pop()

    @utils.check_messages("changed-iteratee")
    def visit_assignname(self, node):
        if isinstance(node, astroid.AssignName):
            for loop in self._loops:
                if loop._name == node.name:
                    self.add_message("changed-iteratee", node=node, args=(node.name,))


# TODO: detect other modification types:
# * del x[i], x.append(), x.insert(), x.setdefault(), etc.


def register(linter: PyLinter) -> None:
    linter.register_checker(ModifiedIterationChecker(linter))
    linter.register_checker(ChangedIterateeChecker(linter))
