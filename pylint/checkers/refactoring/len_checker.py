# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING
from typing import List

import astroid
from astroid import DictComp, GeneratorExp, ListComp, SetComp

from pylint import checkers, interfaces
from pylint.checkers import utils


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
        if not utils.is_call_of_name(node, "len"):
            return
        # the len() call could also be nested together with other
        # boolean operations, e.g. `if z or len(x):`
        parent = node.parent
        while isinstance(parent, astroid.BoolOp):
            parent = parent.parent
        # we're finally out of any nested boolean operations so check if
        # this len() call is part of a test condition
        if not utils.is_test_condition(node, parent):
            return
        len_arg = node.args[0]
        generator_or_comprehension = (ListComp, SetComp, DictComp, GeneratorExp)
        if isinstance(len_arg, generator_or_comprehension):
            # The node is a generator or comprehension as in len([x for x in ...])
            self.add_message("len-as-condition", node=node)
            return
        instance = next(len_arg.infer())
        mother_classes = self.base_classes_of_node(instance)
        affected_by_pep8 = any(
            t in mother_classes for t in ["str", "tuple", "list", "set"]
        )
        if "range" in mother_classes or (
            affected_by_pep8 and not self.instance_has_bool(instance)
        ):
            self.add_message("len-as-condition", node=node)

    @staticmethod
    def instance_has_bool(class_def: astroid.ClassDef) -> bool:
        try:
            class_def.getattr("__bool__")
            return True
        except astroid.AttributeInferenceError:
            ...
        return False

    @utils.check_messages("len-as-condition")
    def visit_unaryop(self, node):
        """`not len(S)` must become `not S` regardless if the parent block
        is a test condition or something else (boolean expression)
        e.g. `if not len(S):`"""
        if (
            isinstance(node, astroid.UnaryOp)
            and node.op == "not"
            and utils.is_call_of_name(node.operand, "len")
        ):
            self.add_message("len-as-condition", node=node)

    @staticmethod
    def base_classes_of_node(instance: astroid.nodes.ClassDef) -> List[astroid.Name]:
        """Return all the classes names that a ClassDef inherit from including 'object'."""
        try:
            return [instance.name] + [x.name for x in instance.ancestors()]
        except TypeError:
            return [instance.name]
