# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING
from typing import Optional

import astroid

from pylint import checkers, interfaces
from pylint.checkers import utils


def _is_call_of_name(node: astroid.node_classes.NodeNG, name: str) -> bool:
    """Checks if node is a function call with the given name"""
    return (
        isinstance(node, astroid.Call)
        and isinstance(node.func, astroid.Name)
        and node.func.name == name
    )


def _is_test_condition(
    node: astroid.node_classes.NodeNG,
    parent: Optional[astroid.node_classes.NodeNG] = None,
) -> bool:
    """Returns true if the given node is being tested for truthiness"""
    parent = parent or node.parent
    if isinstance(parent, (astroid.While, astroid.If, astroid.IfExp, astroid.Assert)):
        return node is parent.test or parent.test.parent_of(node)
    if isinstance(parent, astroid.Comprehension):
        return node in parent.ifs
    return _is_call_of_name(parent, "bool") and parent.parent_of(node)


class LenChecker(checkers.BaseChecker):
    """Checks for incorrect usage of len() inside conditions.
    Pep8 states:
    For sequences, (strings, lists, tuples), use the fact that empty sequences are false.

        Yes: if not seq:
             if seq:

        No: if len(seq):
            if not len(seq):

    Problems detected:
    * if len(sequence):
    * if not len(sequence):
    * elif len(sequence):
    * elif not len(sequence):
    * while len(sequence):
    * while not len(sequence):
    * assert len(sequence):
    * assert not len(sequence):
    * bool(len(sequence))
    """

    __implements__ = (interfaces.IAstroidChecker,)

    # configuration section name
    name = "refactoring"
    msgs = {
        "C1801": (
            "Do not use `len(SEQUENCE)` without comparison to determine if a sequence is empty",
            "len-as-condition",
            "Used when Pylint detects that len(sequence) is being used "
            "without explicit comparison inside a condition to determine if a sequence is empty. "
            "Instead of coercing the length to a boolean, either "
            "rely on the fact that empty sequences are false or "
            "compare the length against a scalar.",
        )
    }

    priority = -2
    options = ()

    @utils.check_messages("len-as-condition")
    def visit_call(self, node):
        # a len(S) call is used inside a test condition
        # could be if, while, assert or if expression statement
        # e.g. `if len(S):`
        if _is_call_of_name(node, "len"):
            # the len() call could also be nested together with other
            # boolean operations, e.g. `if z or len(x):`
            parent = node.parent
            while isinstance(parent, astroid.BoolOp):
                parent = parent.parent

            # we're finally out of any nested boolean operations so check if
            # this len() call is part of a test condition
            if _is_test_condition(node, parent):
                self.add_message("len-as-condition", node=node)

    @utils.check_messages("len-as-condition")
    def visit_unaryop(self, node):
        """`not len(S)` must become `not S` regardless if the parent block
        is a test condition or something else (boolean expression)
        e.g. `if not len(S):`"""
        if (
            isinstance(node, astroid.UnaryOp)
            and node.op == "not"
            and _is_call_of_name(node.operand, "len")
        ):
            self.add_message("len-as-condition", node=node)
