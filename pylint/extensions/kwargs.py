# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import bases, nodes

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
            "Call to `%s` misses keyword argument `%s`.",
            "consider-using-keyword-argument",
            "When using a literal directly in a function call, it can be very hard to know which argument it is "
            "if a positional argument is used. In that case there's no variable name or attribute name to "
            "rely on when reading. By using a keyword argument there's at least the attribute name to "
            "help the reader understand the call.",
        ),
    }

    def visit_call(self, node: nodes.Call) -> None:
        """Check that called functions/methods are provided keyword arguments."""
        called = safe_infer(node.func)

        if not called or not isinstance(
            called,
            (nodes.ClassDef, nodes.FunctionDef, bases.BoundMethod, bases.UnboundMethod),
        ):
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
                    "consider-using-keyword-argument",
                    node=node,
                    args=(
                        called.name,
                        arg_name,
                    ),
                    confidence=INFERENCE,
                )

    def _get_args(
        self,
        node: nodes.ClassDef
        | nodes.FunctionDef
        | bases.BoundMethod
        | bases.UnboundMethod,
    ) -> tuple[list[str], list[str]]:
        default_kwargs = []
        needed_keywords = []

        if isinstance(node, nodes.ClassDef) and "__init__" in node.locals:
            init_func = node.locals["__init__"][0]
            if isinstance(init_func, nodes.FunctionDef):
                node_args = init_func.args
                if node_args and node_args.args:
                    needed_keywords = [
                        x.name for x in node_args.args if x.name != "self"
                    ]
                    default_kwargs = [
                        x.name for x in node_args.args[-len(node_args.defaults) :]
                    ]
        elif isinstance(
            node, (nodes.FunctionDef, bases.BoundMethod, bases.UnboundMethod)
        ):
            needed_keywords = node.argnames()
            to_ignore = {"self", "args", "kwargs"}

            if node.is_method():
                needed_keywords = [x for x in needed_keywords if x not in to_ignore]

            if node.args.defaults:
                default_kwargs = [
                    x.name for x in node.args.args[-len(node.args.defaults) :]
                ]

        return needed_keywords, default_kwargs


def register(linter: PyLinter) -> None:
    linter.register_checker(KeywordChecker(linter))
