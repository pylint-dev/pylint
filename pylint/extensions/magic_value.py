# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Checks for magic numbers instead of literals."""

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker, utils
from pylint.checkers.base.comparison_checker import ComparisonChecker
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class MagicValueChecker(BaseChecker):
    """Checks for constants in comparisons."""

    name = "magic-value"
    msgs = {
        "R2004": (
            "Constant %s is used in comparison. Consider using literals instead of magic values.",
            "magic-value-compare",
            "Using literals instead of magic values helps improve readability and maintainability of your"
            " code, try to avoid them in comparisons ",
        )
    }

    options = (
        (
            "valid-magic-values",
            {
                "default": (-1, 0, 1, "", "__main__"),
                "type": "csv",
                "metavar": "<method names>",
                "help": " List of valid magic numbers that `magic-value-compare` will not detect.",
            },
        ),
    )

    def _check_constants_comparison(self, node: nodes.Compare) -> None:
        """
        Magic values in any side of the comparison should be avoided,
        Detects comparisons that `comparison-of-constants` core checker cannot detect.
        """
        const_operands = []
        LEFT_OPERAND = 0
        RIGHT_OPERAND = 1

        left_operand = node.left
        const_operands.append(isinstance(left_operand, nodes.Const))

        right_operand = node.ops[0][1]
        const_operands.append(isinstance(right_operand, nodes.Const))

        if all(const_operands):
            # `comparison-of-constants` avoided
            return

        if const_operands[LEFT_OPERAND] and self._is_magic_value(left_operand):
            self.add_message(
                "magic-comparison",
                node=node,
                args=(left_operand.value),
                confidence=HIGH,
            )
        elif const_operands[RIGHT_OPERAND] and self._is_magic_value(right_operand):
            self.add_message(
                "magic-comparison",
                node=node,
                args=(right_operand.value),
                confidence=HIGH,
            )

    def _is_magic_value(self, node: nodes.NodeNG) -> bool:
        return (not ComparisonChecker.is_singleton_const(node)) and (
            node.value not in self.linter.config.valid_magic_values
        )

    @utils.only_required_for_messages("magic-comparison")
    def visit_compare(self, node: nodes.Compare) -> None:
        self._check_constants_comparison(node)


def register(linter: PyLinter) -> None:
    linter.register_checker(MagicValueChecker(linter))
