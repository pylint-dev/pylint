# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""A test checker with fixable messages, to test the autofix machinery."""

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.message import Applicability, Edit, Fix, source_segment

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class FixTestChecker(BaseChecker):
    name = "fix-test"
    msgs = {
        "W9901": (
            "Use 'new_name' instead of 'old_name'",
            "old-name-used",
            "Used to test safe fixes.",
            {"fixable": True},
        ),
        "W9902": (
            "Useless pass statement",
            "useless-pass-statement",
            "Used to test unsafe fixes.",
            {"fixable": True},
        ),
        "W9903": (
            "Double the number",
            "double-number",
            "Used to test fixes built from the original source code.",
            {"fixable": True},
        ),
    }

    def visit_name(self, node: nodes.Name) -> None:
        if node.name == "old_name":
            self.add_message(
                "old-name-used",
                node=node,
                fix=lambda: Fix.create(
                    "Rename to 'new_name'",
                    Edit.replace(node, "new_name"),
                    applicability=Applicability.SAFE,
                ),
            )

    def visit_pass(self, node: nodes.Pass) -> None:
        if len(node.parent.body) > 1:
            self.add_message(
                "useless-pass-statement",
                node=node,
                fix=Fix.create("Remove the pass statement", Edit.delete(node)),
            )

    def visit_call(self, node: nodes.Call) -> None:
        if isinstance(node.func, nodes.Name) and node.func.name == "double":
            argument = source_segment(node.args[0])
            self.add_message(
                "double-number",
                node=node,
                fix=Fix.create(
                    "Multiply by two",
                    Edit.replace(node, f"({argument}) * 2"),
                    applicability=Applicability.SAFE,
                ),
            )


def register(linter: PyLinter) -> None:
    linter.register_checker(FixTestChecker(linter))
