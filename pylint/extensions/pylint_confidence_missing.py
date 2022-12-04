# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Check for use of confidence when adding pylint message."""

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class PylintConfidenceChecker(BaseChecker):

    name = "pylint_confidence_missing"
    msgs = {
        "W3000": (
            "Missing confidence in %s",
            "missing-pylint-confidence",
            "Check that pylint plugins set the confidence correctly when raising a message.",
        )
    }

    @only_required_for_messages("while-used")
    def visit_call(self, node: nodes.While) -> None:
        self.add_message("while-used", node=node)


def register(linter: PyLinter) -> None:
    linter.register_checker(PylintConfidenceChecker(linter))
