# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Match statement checker for Python code."""

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class MatchStatementChecker(BaseChecker):
    name = "match_statements"
    msgs = {
        "E5000": (
            "The name capture `case %s` makes the remaining patterns unreachable. "
            "Use a dotted name(for example an enum) to fix this",
            "unreachable-match-patterns",
            "Emitted when a name capture pattern in a match statement is used "
            "and there are case statements below it.",
        )
    }

    def open(self) -> None:
        py_version = self.linter.config.py_version
        self._py310_plus = py_version >= (3, 10)

    @only_required_for_messages("unreachable-match-patterns")
    def visit_match(self, node: nodes.Match) -> None:
        """Check if a name capture pattern prevents the other cases from being
        reached
        """
        for idx, case in enumerate(node.cases):
            if (
                isinstance(case.pattern, nodes.MatchAs)
                and case.pattern.pattern is None
                and isinstance(case.pattern.name, nodes.AssignName)
                and idx < len(node.cases) - 1
                and self._py310_plus
            ):
                self.add_message(
                    "unreachable-match-patterns",
                    node=case,
                    args=case.pattern.name.name,
                    confidence=HIGH,
                )


def register(linter: PyLinter) -> None:
    linter.register_checker(MatchStatementChecker(linter))
