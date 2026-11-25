"""Deferred annotations can name a class that is local to a function."""

# pylint: disable=missing-docstring, too-few-public-methods

from __future__ import annotations


def factory():
    class Local:
        def clone(self) -> Local:
            return self

    class Nested:
        class Inner:
            def clone(self) -> Inner:  # [undefined-variable]
                return self

    class Parameter:
        def clone(self) -> self.Parameter:  # [undefined-variable]
            return self

    def annotated(value: Unknown) -> None:  # [undefined-variable]
        print(value)

    return Local, Nested, Parameter, annotated
