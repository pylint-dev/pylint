# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Check for use of nested min/max functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages, safe_infer
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class NestedMinMaxChecker(BaseChecker):
    FUNC_NAMES = ("builtins.min", "builtins.max")

    name = "nested_min_max"
    msgs = {
        "W3201": (
            "Do not use nested call of '%s'  it's possible to do '%s' instead",
            "nested-min-max",
            "Nested calls ``min(1, min(2, 3))`` can be rewritten as ``min(1, 2, 3)``.",
        )
    }

    @classmethod
    def is_min_max_call(cls, node: nodes.NodeNG):
        if not isinstance(node, nodes.Call):
            return False

        inferred = safe_infer(node.func)
        return (
            inferred is not None
            and inferred.is_function
            and inferred.qname() in cls.FUNC_NAMES
        )

    @classmethod
    def get_redundant_calls(cls, node: nodes.Call):
        return [
            arg
            for arg in node.args
            if cls.is_min_max_call(arg) and arg.func.name == node.func.name
        ]

    @only_required_for_messages("nested-min-max")
    def visit_call(self, node: nodes.Call) -> None:
        if not self.is_min_max_call(node):
            return

        redundant_calls = self.get_redundant_calls(node)
        if len(redundant_calls) == 0:
            return

        while len(redundant_calls) > 0:
            for i, arg in enumerate(node.args):
                if arg in redundant_calls:
                    node.args = node.args[:i] + arg.args + node.args[i + 1 :]
                    break

            redundant_calls = self.get_redundant_calls(node)

        self.add_message(
            "nested-min-max",
            node=node,
            args=(node.func.name, node.as_string()),
            confidence=HIGH,
        )


def register(linter: PyLinter) -> None:
    linter.register_checker(NestedMinMaxChecker(linter))
