# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.constants import DUNDER_METHODS, DUNDER_PROPERTIES, EXTRA_DUNDER_METHODS
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint import PyLinter

# The only dunder methods whose protocol allows ``async def``. Every other one,
# ``__aiter__`` and ``__await__`` included, must return its result directly.
ASYNC_DUNDER_METHODS = ["__aenter__", "__aexit__", "__anext__", "__call__"]


class DunderChecker(BaseChecker):
    """Checks related to dunder methods."""

    name = "dunder"
    msgs = {
        "W3201": (
            "Bad or misspelled dunder method name %s.",
            "bad-dunder-name",
            "Used when a dunder method is misspelled or defined with a name "
            "not within the predefined list of dunder names, or defined with "
            "``async def`` when its protocol requires a regular ``def``.",
        ),
    }
    options = (
        (
            "good-dunder-names",
            {
                "default": [],
                "type": "csv",
                "metavar": "<comma-separated names>",
                "help": "Good dunder names which should always be accepted.",
            },
        ),
    )

    def open(self) -> None:
        self._dunder_methods = DUNDER_PROPERTIES + self.linter.config.good_dunder_names
        for since_vers, extra_dunder_methods in EXTRA_DUNDER_METHODS.items():
            if since_vers <= self.linter.config.py_version:
                self._dunder_methods.extend(extra_dunder_methods)
        for since_vers, dunder_methods in DUNDER_METHODS.items():
            if since_vers <= self.linter.config.py_version:
                self._dunder_methods.extend(list(dunder_methods.keys()))
        self._async_dunder_methods = (
            ASYNC_DUNDER_METHODS + self.linter.config.good_dunder_names
        )

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        """Check if known dunder method is misspelled or dunder name is not one
        of the pre-defined names.
        """
        self._check_dunder_name(node, self._dunder_methods)

    def visit_asyncfunctiondef(self, node: nodes.AsyncFunctionDef) -> None:
        """Check that an async dunder method is one whose protocol allows it."""
        valid_names = self._async_dunder_methods
        if node.is_generator():
            # An async generator is the async iterator ``__aiter__`` returns.
            valid_names = [*valid_names, "__aiter__"]
        self._check_dunder_name(node, valid_names)

    def _check_dunder_name(
        self, node: nodes.FunctionDef, valid_names: list[str]
    ) -> None:
        # ignore module-level functions
        if not node.is_method():
            return

        # Detect something that could be a bad dunder method
        if (
            node.name.startswith("_")
            and node.name.endswith("_")
            and node.name not in valid_names
        ):
            self.add_message(
                "bad-dunder-name",
                node=node,
                args=(node.name),
                confidence=HIGH,
            )


def register(linter: PyLinter) -> None:
    linter.register_checker(DunderChecker(linter))
