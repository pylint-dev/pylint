# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

from astroid import BoundMethod, nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer
from pylint.interfaces import INFERENCE

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class KeywordChecker(BaseChecker):
    """Checks related to keyword arguments."""

    name = "kwargs"
    msgs = {
        "W3501": (
            "Call to `%s` missing keyword argument `%s`.",
            "missing-keyword-arg",
            "Used when method is called without specifying a keyword argument. ",
        ),
    }

    def visit_call(self, node: nodes.Call) -> None:
        """Check that called functions/methods are provided keyword arguments."""
        called = safe_infer(node.func)

        if not isinstance(called, (nodes.ClassDef, nodes.FunctionDef, BoundMethod)):
            return

        needed_keywords, default_kwarg_names = self._get_args(called)

        if len(needed_keywords) - len(default_kwarg_names) < 2:
            # This checker will not apply if there are less than 2 positional args.
            return

        provided_kwarg_names = [
            kwarg.arg for kwarg in node.keywords
        ] + default_kwarg_names

        for arg_name in needed_keywords:
            if arg_name not in provided_kwarg_names:
                self.add_message(
                    "missing-keyword-arg",
                    node=node,
                    args=(
                        called.name,
                        arg_name,
                    ),
                    confidence=INFERENCE,
                )

    def _get_args(
        self, node: nodes.ClassDef | nodes.FunctionDef | BoundMethod
    ) -> Tuple[list[str], list[str]]:
        if isinstance(node, nodes.ClassDef):
            needed_keywords = node.instance_attrs.keys()
            node_args = node.locals["__init__"][0].args
            default_kwargs = [
                x.name for x in node_args.args[-len(node_args.defaults) :]
            ]
        elif isinstance(node, (nodes.FunctionDef, BoundMethod)):
            needed_keywords = node.argnames()
            if node.is_method():
                needed_keywords = [x for x in needed_keywords if x != "self"]
            default_kwargs = []
            if node.args.defaults:
                default_kwargs = [
                    x.name for x in node.args.args[-len(node.args.defaults) :]
                ]

        return needed_keywords, default_kwargs


def register(linter: PyLinter) -> None:
    linter.register_checker(KeywordChecker(linter))
