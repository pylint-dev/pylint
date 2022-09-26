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

LEGAL_MAGIC_NUMBERS = {-1, 0, 1, "", "__main__"}


class MagicNumberChecker(BaseChecker):
    """Checks for constants in comparisons."""

    name = "magic-number"
    msgs = {
        "R2004": (
            "Unnamed constant %s is used, consider using literal instead of magic numbers.",
            "magic-comparison",
            "Used when magic numbers are used in any side of a comparison ",
        )
    }

    options = ()

    def _check_constants_comparison(self, node: nodes.Compare) -> None:
        """
        Magic numbers in any side of the comparison should be avoided,
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

        if const_operands[LEFT_OPERAND] and self._is_magic_number(left_operand):
            self.add_message(
                "magic-comparison",
                node=node,
                args=(left_operand.value),
                confidence=HIGH,
            )
        elif const_operands[RIGHT_OPERAND] and self._is_magic_number(right_operand):
            self.add_message(
                "magic-comparison",
                node=node,
                args=(right_operand.value),
                confidence=HIGH,
            )

    def _is_magic_number(self, node: nodes.NodeNG) -> bool:
        return (not ComparisonChecker.is_singleton_const(node)) and (
            node.value not in LEGAL_MAGIC_NUMBERS
        )

    @utils.only_required_for_messages("magic-comparison")
    def visit_compare(self, node: nodes.Compare) -> None:
        self._check_constants_comparison(node)


def register(linter: PyLinter) -> None:
    linter.register_checker(MagicNumberChecker(linter))
