from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint import PyLinter

COMPARISON_OP = frozenset(("<", "<=", ">", ">=", "!=", "=="))
IDENTITY_OP = frozenset(("is", "is not"))
MEMBERSHIP_OP = frozenset(("in", "not in"))


class BadChainedComparisonChecker(BaseChecker):
    """Checks for unintentional usage of chained comparison."""

    name = "bad-chained-comparison"
    msgs = {
        "W3501": (
            "Suspicious %s-part chained comparison using semantically incompatible operators (%s)",
            "bad-chained-comparison",
            "Used when there is a chained comparison where one expression is part of two comparisons that belong to different semantic groups "
            ' ("<" does not mean the same thing as "is", chaining them in "0 < x is None" is probably a mistake).',
        )
    }

    def _get_distinct_operators(self, node: nodes.Compare) -> list:
        operators = [op[0] for op in node.ops]
        return list(dict.fromkeys(operators))

    def _has_diff_semantic_groups(self, operators: list) -> bool:
        # Check if comparison operators are in the same semantic group
        for comparison_group in (COMPARISON_OP, IDENTITY_OP, MEMBERSHIP_OP):
            if operators[0] in comparison_group:
                group = comparison_group
        return not all(o in group for o in operators)

    def visit_compare(self, node: nodes.Compare) -> None:
        operators = self._get_distinct_operators(node)
        if self._has_diff_semantic_groups(operators):
            num_parts = f"{len(node.ops)}"
            incompatibles = (
                ", ".join(f"'{o}'" for o in operators[:-1]) + f" and '{operators[-1]}'"
            )
            self.add_message(
                "bad-chained-comparison",
                node=node,
                args=(num_parts, incompatibles),
                confidence=HIGH,
            )


def register(linter: PyLinter) -> None:
    linter.register_checker(BadChainedComparisonChecker(linter))
