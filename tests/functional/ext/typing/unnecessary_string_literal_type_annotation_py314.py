"""Tests for pylint.extensions.typing unnecessary-string-literal-type-annotation.

'py-version' needs to be set to >= '3.14'.
"""

# pylint: disable=missing-docstring,invalid-name,too-few-public-methods,line-too-long

from typing import Annotated, Literal


class Foo:
    def some_function(self) -> "Bar":  # [unnecessary-string-literal-type-annotation]
        raise NotImplementedError


class Bar:
    def another_function(self) -> "Foo":  # [unnecessary-string-literal-type-annotation]
        raise NotImplementedError


def f(x: "Foo") -> list["Bar"]:  # [unnecessary-string-literal-type-annotation, unnecessary-string-literal-type-annotation]
    del x
    return [Bar()]


value: Literal["x"] = "x"
meta_ok: Annotated[int, "metadata"] = 0
annotated_forwardref: Annotated["Foo", "metadata"] = Foo()  # [unnecessary-string-literal-type-annotation]
