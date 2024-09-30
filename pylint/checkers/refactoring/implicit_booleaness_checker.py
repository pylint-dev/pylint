# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import itertools

import astroid
from astroid import bases, nodes, util

from pylint import checkers
from pylint.checkers import utils
from pylint.interfaces import HIGH, INFERENCE


def _is_constant_zero(node: str | nodes.NodeNG) -> bool:
    # We have to check that node.value is not False because node.value == 0 is True
    # when node.value is False
    return (
        isinstance(node, astroid.Const) and node.value == 0 and node.value is not False
    )


class ImplicitBooleanessChecker(checkers.BaseChecker):
    """Checks for incorrect usage of comparisons or len() inside conditions.

    Incorrect usage of len()
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

    Incorrect usage of empty literal sequences; (), [], {},

    For empty sequences, (dicts, lists, tuples), use the fact that empty sequences are false.

        Yes: if variable:
             if not variable

        No: if variable == empty_literal:
            if variable != empty_literal:

    Problems detected:
    * comparison such as variable == empty_literal:
    * comparison such as variable != empty_literal:
    """

    name = "refactoring"
    msgs = {
        "C1802": (
            "Do not use `len(SEQUENCE)` without comparison to determine if a sequence is empty",
            "use-implicit-booleaness-not-len",
            "Empty sequences are considered false in a boolean context. You can either"
            " remove the call to 'len' (``if not x``) or compare the length against a"
            " scalar (``if len(x) > 1``).",
            {"old_names": [("C1801", "len-as-condition")]},
        ),
        "C1803": (
            '"%s" can be simplified to "%s", if it is strictly a sequence, as an empty %s is falsey',
            "use-implicit-booleaness-not-comparison",
            "Empty sequences are considered false in a boolean context. Following this"
            " check blindly in weakly typed code base can create hard to debug issues."
            " If the value can be something else that is falsey but not a sequence (for"
            " example ``None``, an empty string, or ``0``) the code will not be "
            "equivalent.",
        ),
        "C1804": (
            '"%s" can be simplified to "%s", if it is strictly a string, as an empty string is falsey',
            "use-implicit-booleaness-not-comparison-to-string",
            "Empty string are considered false in a boolean context. Following this"
            " check blindly in weakly typed code base can create hard to debug issues."
            " If the value can be something else that is falsey but not a string (for"
            " example ``None``, an empty sequence, or ``0``) the code will not be "
            "equivalent.",
            {
                "default_enabled": False,
                "old_names": [("C1901", "compare-to-empty-string")],
            },
        ),
        "C1805": (
            '"%s" can be simplified to "%s", if it is strictly an int, as 0 is falsey',
            "use-implicit-booleaness-not-comparison-to-zero",
            "0 is considered false in a boolean context. Following this"
            " check blindly in weakly typed code base can create hard to debug issues."
            " If the value can be something else that is falsey but not an int (for"
            " example ``None``, an empty string, or an empty sequence) the code will not be "
            "equivalent.",
            {"default_enabled": False, "old_names": [("C2001", "compare-to-zero")]},
        ),
    }

    options = ()
    _operators = {"!=", "==", "is not", "is"}

    @utils.only_required_for_messages("use-implicit-booleaness-not-len")
    def visit_call(self, node: nodes.Call) -> None:
        # a len(S) call is used inside a test condition
        # could be if, while, assert or if expression statement
        # e.g. `if len(S):`
        if not utils.is_call_of_name(node, "len"):
            return
        # the len() call could also be nested together with other
        # boolean operations, e.g. `if z or len(x):`
        parent = node.parent
        while isinstance(parent, nodes.BoolOp):
            parent = parent.parent
        # we're finally out of any nested boolean operations so check if
        # this len() call is part of a test condition
        if not utils.is_test_condition(node, parent):
            return
        len_arg = node.args[0]
        generator_or_comprehension = (
            nodes.ListComp,
            nodes.SetComp,
            nodes.DictComp,
            nodes.GeneratorExp,
        )
        if isinstance(len_arg, generator_or_comprehension):
            # The node is a generator or comprehension as in len([x for x in ...])
            self.add_message(
                "use-implicit-booleaness-not-len",
                node=node,
                confidence=HIGH,
            )
            return
        try:
            instance = next(len_arg.infer())
        except astroid.InferenceError:
            # Probably undefined-variable, abort check
            return
        mother_classes = self.base_names_of_instance(instance)
        affected_by_pep8 = any(
            t in mother_classes for t in ("str", "tuple", "list", "set")
        )
        if "range" in mother_classes or (
            affected_by_pep8 and not self.instance_has_bool(instance)
        ):
            self.add_message(
                "use-implicit-booleaness-not-len",
                node=node,
                confidence=INFERENCE,
            )

    @staticmethod
    def instance_has_bool(class_def: nodes.ClassDef) -> bool:
        try:
            class_def.getattr("__bool__")
            return True
        except astroid.AttributeInferenceError:
            ...
        return False

    @utils.only_required_for_messages("use-implicit-booleaness-not-len")
    def visit_unaryop(self, node: nodes.UnaryOp) -> None:
        """`not len(S)` must become `not S` regardless if the parent block is a test
        condition or something else (boolean expression) e.g. `if not len(S):`.
        """
        if (
            isinstance(node, nodes.UnaryOp)
            and node.op == "not"
            and utils.is_call_of_name(node.operand, "len")
        ):
            self.add_message(
                "use-implicit-booleaness-not-len", node=node, confidence=HIGH
            )

    @utils.only_required_for_messages(
        "use-implicit-booleaness-not-comparison",
        "use-implicit-booleaness-not-comparison-to-string",
        "use-implicit-booleaness-not-comparison-to-zero",
    )
    def visit_compare(self, node: nodes.Compare) -> None:
        if self.linter.is_message_enabled("use-implicit-booleaness-not-comparison"):
            self._check_use_implicit_booleaness_not_comparison(node)
        if self.linter.is_message_enabled(
            "use-implicit-booleaness-not-comparison-to-zero"
        ) or self.linter.is_message_enabled(
            "use-implicit-booleaness-not-comparison-to-str"
        ):
            self._check_compare_to_str_or_zero(node)

    def _check_compare_to_str_or_zero(self, node: nodes.Compare) -> None:
        # note: astroid.Compare has the left most operand in node.left
        # while the rest are a list of tuples in node.ops
        # the format of the tuple is ('compare operator sign', node)
        # here we squash everything into `ops` to make it easier for processing later
        ops: list[tuple[str, nodes.NodeNG]] = [("", node.left), *node.ops]
        iter_ops = iter(ops)
        all_ops = list(itertools.chain(*iter_ops))
        for ops_idx in range(len(all_ops) - 2):
            op_2 = all_ops[ops_idx + 1]
            if op_2 not in self._operators:
                continue
            op_1 = all_ops[ops_idx]
            op_3 = all_ops[ops_idx + 2]
            if self.linter.is_message_enabled(
                "use-implicit-booleaness-not-comparison-to-zero"
            ):
                op = None
                # 0 ?? X
                if _is_constant_zero(op_1):
                    op = op_3
                # X ?? 0
                elif _is_constant_zero(op_3):
                    op = op_1
                if op is not None:
                    original = f"{op_1.as_string()} {op_2} {op_3.as_string()}"
                    suggestion = (
                        op.as_string()
                        if op_2 in {"!=", "is not"}
                        else f"not {op.as_string()}"
                    )
                    self.add_message(
                        "use-implicit-booleaness-not-comparison-to-zero",
                        args=(original, suggestion),
                        node=node,
                        confidence=HIGH,
                    )
            if self.linter.is_message_enabled(
                "use-implicit-booleaness-not-comparison-to-str"
            ):
                node_name = None
                # x ?? ""
                if utils.is_empty_str_literal(op_1):
                    node_name = op_3.as_string()
                # '' ?? X
                elif utils.is_empty_str_literal(op_3):
                    node_name = op_1.as_string()
                if node_name is not None:
                    suggestion = (
                        f"not {node_name}" if op_2 in {"==", "is"} else node_name
                    )
                    self.add_message(
                        "use-implicit-booleaness-not-comparison-to-string",
                        args=(node.as_string(), suggestion),
                        node=node,
                        confidence=HIGH,
                    )

    def _check_use_implicit_booleaness_not_comparison(
        self, node: nodes.Compare
    ) -> None:
        """Check for left side and right side of the node for empty literals."""
        is_left_empty_literal = utils.is_base_container(
            node.left
        ) or utils.is_empty_dict_literal(node.left)

        # Check both left-hand side and right-hand side for literals
        for operator, comparator in node.ops:
            is_right_empty_literal = utils.is_base_container(
                comparator
            ) or utils.is_empty_dict_literal(comparator)
            # Using Exclusive OR (XOR) to compare between two side.
            # If two sides are both literal, it should be different error.
            if is_right_empty_literal ^ is_left_empty_literal:
                # set target_node to opposite side of literal
                target_node = node.left if is_right_empty_literal else comparator
                literal_node = comparator if is_right_empty_literal else node.left
                # Infer node to check
                target_instance = utils.safe_infer(target_node)
                if target_instance is None:
                    continue
                mother_classes = self.base_names_of_instance(target_instance)
                is_base_comprehension_type = any(
                    t in mother_classes for t in ("tuple", "list", "dict", "set")
                )

                # Only time we bypass check is when target_node is not inherited by
                # collection literals and have its own __bool__ implementation.
                if not is_base_comprehension_type and self.instance_has_bool(
                    target_instance
                ):
                    continue

                # No need to check for operator when visiting compare node
                if operator in {"==", "!=", ">=", ">", "<=", "<"}:
                    self.add_message(
                        "use-implicit-booleaness-not-comparison",
                        args=self._implicit_booleaness_message_args(
                            literal_node, operator, target_node
                        ),
                        node=node,
                        confidence=HIGH,
                    )

    def _get_node_description(self, node: nodes.NodeNG) -> str:
        return {
            nodes.List: "list",
            nodes.Tuple: "tuple",
            nodes.Dict: "dict",
            nodes.Const: "str",
        }.get(type(node), "iterable")

    def _implicit_booleaness_message_args(
        self, literal_node: nodes.NodeNG, operator: str, target_node: nodes.NodeNG
    ) -> tuple[str, str, str]:
        """Helper to get the right message for "use-implicit-booleaness-not-comparison"."""
        description = self._get_node_description(literal_node)
        collection_literal = {
            "list": "[]",
            "tuple": "()",
            "dict": "{}",
        }.get(description, "iterable")
        instance_name = "x"
        if isinstance(target_node, nodes.Call) and target_node.func:
            instance_name = f"{target_node.func.as_string()}(...)"
        elif isinstance(target_node, (nodes.Attribute, nodes.Name)):
            instance_name = target_node.as_string()
        original_comparison = f"{instance_name} {operator} {collection_literal}"
        suggestion = f"{instance_name}" if operator == "!=" else f"not {instance_name}"
        return original_comparison, suggestion, description

    @staticmethod
    def base_names_of_instance(
        node: util.UninferableBase | bases.Instance,
    ) -> list[str]:
        """Return all names inherited by a class instance or those returned by a
        function.

        The inherited names include 'object'.
        """
        if isinstance(node, bases.Instance):
            return [node.name] + [x.name for x in node.ancestors()]
        return []
