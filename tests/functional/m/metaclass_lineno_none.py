# pylint: disable=missing-class-docstring,missing-function-docstring,missing-module-docstring,too-few-public-methods
"""Regression test: a metaclass whose name binding has no line number.

Using ``__annotations__`` as a metaclass produces a synthetic binding node
without a ``lineno``; checking the class used to crash with
``TypeError: '<=' not supported between instances of 'NoneType' and 'int'``.
See https://github.com/pylint-dev/pylint/issues/11511
"""
from __future__ import annotations


class _Outer:
    """Outer class."""

    class _InClassBody(metaclass=__annotations__):
        """The class body holding the lineno-less binding runs this statement."""

    def _method(self) -> None:
        """Method holding a nested class using a synthetic metaclass."""

        # The body of the class is not visible from its methods.
        class _Inner(metaclass=__annotations__):  # [undefined-variable]
            """Inner class using a lineno-less metaclass binding."""
