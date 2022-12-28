from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter

COMPARISON_OP = frozenset(("<", "<=", ">", ">=", "!=", "=="))
IDENTITY_OP = frozenset(("is", "is not"))
MEMBERSHIP_OP = frozenset(("in", "not in"))

class BadChainedComparisonChecker(BaseChecker):
    """Checks for unintentional usage of chained comparison"""
    name = "bad-chained-comparison"
    msgs = {
        "W2401": (
            "Expression gets interpreted as a %s-part chained comparison which straddles comparison groups. If this is not the intent, please parenthesize.",
            "bad-chained-comparison",
            "Used when there is a chained comparison where one expression is part of two comparisons that belong to different groups.",
        )
    }

    def _has_diff_comparison_groups(self, node: nodes.Compare) -> bool:
        operators = [op[0] for op in node.ops]
        # Check if comparison operators are in the same group
        for comparison_group in (COMPARISON_OP, IDENTITY_OP, MEMBERSHIP_OP):
            if operators[0] in comparison_group:
                group = comparison_group
        return not all(o in group for o in operators)

    def visit_compare(self, node: nodes.Compare) -> None:
        if self._has_diff_comparison_groups(node):
            num_pieces = f"{len(node.ops)}"
            self.add_message("bad-chained-comparison", node=node, args=(num_pieces))

def register(linter: PyLinter) -> None:
    linter.register_checker(BadChainedComparisonChecker(linter))
