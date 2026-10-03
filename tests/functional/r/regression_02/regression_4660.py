"""Regression tests for https://github.com/pylint-dev/pylint/issues/4660"""

# pylint: disable=useless-return, unused-argument
# pylint: disable=missing-docstring, too-few-public-methods, invalid-name

from __future__ import annotations

from typing import Union, Any, Literal, overload
from collections.abc import Callable


def my_print(*args: Any) -> None:
    print(", ".join(str(x) for x in args))
    return


class MyClass:
    def my_method(self, option: Literal["mandatory"]) -> Callable[..., Any]:
        return my_print


c = MyClass().my_method("mandatory")
c(1, "foo")

class MyClass1:
    @overload
    def my_method(self, option: Literal["mandatory"]) -> Callable[..., Any]:
        ...

    @overload
    def my_method(
        self, option: Literal["optional", "mandatory"]
    ) -> Union[None, Callable[..., Any]]:
        ...

    def my_method(
        self, option: Literal["optional", "mandatory"]
    ) -> Union[None, Callable[..., Any]]:
        return my_print


d = MyClass1().my_method("mandatory")
d(1, "bar")
