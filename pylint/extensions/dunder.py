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

# Dunder methods that cannot be ``async def``: Python checks the type of their
# return value, uses it as a bool, or ignores it, so the coroutine an
# ``async def`` returns is never awaited. The value is the async method that
# was probably meant. ``__aiter__`` is handled apart: it can be an async
# generator.
ASYNC_INCOMPATIBLE_DUNDER_METHODS = {
    "__enter__": "__aenter__",
    "__exit__": "__aexit__",
    "__iter__": "__aiter__",
    "__next__": "__anext__",
    **dict.fromkeys(
        (
            # The return value must have a given type.
            "__init__",
            "__await__",
            "__bool__",
            "__len__",
            "__length_hint__",
            "__hash__",
            "__index__",
            "__int__",
            "__float__",
            "__complex__",
            "__str__",
            "__repr__",
            "__bytes__",
            "__format__",
            "__fspath__",
            "__sizeof__",
            "__reversed__",
            "__dir__",
            "__reduce__",
            # The return value is used as a bool, so a coroutine is always true.
            "__contains__",
            "__eq__",
            "__ne__",
            "__lt__",
            "__le__",
            "__gt__",
            "__ge__",
            "__instancecheck__",
            "__subclasscheck__",
            # The return value is ignored.
            "__del__",
            "__setitem__",
            "__delitem__",
            "__setattr__",
            "__delattr__",
            "__set__",
            "__delete__",
            "__set_name__",
            "__init_subclass__",
            "__post_init__",
        ),
        "",
    ),
}


class DunderChecker(BaseChecker):
    """Checks related to dunder methods."""

    name = "dunder"
    msgs = {
        "W3201": (
            "Bad or misspelled dunder method name %s.",
            "bad-dunder-name",
            "Used when a dunder method is misspelled or defined with a name "
            "not within the predefined list of dunder names, or defined with "
            "``async def`` when Python cannot await the coroutine it returns.",
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

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        """Check if known dunder method is misspelled or dunder name is not one
        of the pre-defined names.
        """
        if self._is_unknown_dunder_name(node):
            self._add_bad_dunder_name(node, node.name)

    def visit_asyncfunctiondef(self, node: nodes.AsyncFunctionDef) -> None:
        """Also check that Python can await the coroutine an async dunder method
        returns.
        """
        if self._is_unknown_dunder_name(node):
            self._add_bad_dunder_name(node, node.name)
            return
        if not node.is_method() or node.name in self.linter.config.good_dunder_names:
            return
        if node.name == "__aiter__":
            # An async generator is the async iterator ``__aiter__`` returns.
            if not node.is_generator():
                self._add_bad_dunder_name(
                    node, "__aiter__ (cannot be async unless it is an async generator)"
                )
            return
        if node.name in ASYNC_INCOMPATIBLE_DUNDER_METHODS:
            async_name = ASYNC_INCOMPATIBLE_DUNDER_METHODS[node.name]
            reason = (
                f"cannot be async, use {async_name}"
                if async_name
                else "cannot be async"
            )
            self._add_bad_dunder_name(node, f"{node.name} ({reason})")

    def _is_unknown_dunder_name(self, node: nodes.FunctionDef) -> bool:
        # ignore module-level functions
        return (
            node.is_method()
            and node.name.startswith("_")
            and node.name.endswith("_")
            and node.name not in self._dunder_methods
        )

    def _add_bad_dunder_name(self, node: nodes.FunctionDef, name: str) -> None:
        self.add_message("bad-dunder-name", node=node, args=(name,), confidence=HIGH)


def register(linter: PyLinter) -> None:
    linter.register_checker(DunderChecker(linter))
