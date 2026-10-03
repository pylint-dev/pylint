"""Overload stubs in a subclass are not compared to the overridden method.

https://github.com/pylint-dev/pylint/issues/5264
https://github.com/pylint-dev/pylint/issues/10186
"""
# pylint: disable=missing-docstring,unused-argument,too-few-public-methods
from typing import Literal, Union, overload


class Parent:
    def statement(self, future: Literal[None, True] = None) -> Union[int, str]:
        pass


class Child(Parent):
    @overload
    def statement(self, future: Literal[None] = ...) -> int: ...

    @overload
    def statement(self, future: Literal[True]) -> str: ...

    def statement(self, future: Literal[None, True] = None) -> Union[int, str]:
        pass


class OverloadedParent:
    @overload
    def func(self, *, b: Literal[True]) -> None: ...

    @overload
    def func(self, *, b: Literal[False], p: int) -> None: ...

    @overload
    def func(self, *, s: str) -> None: ...

    def func(
        self, *, b: Union[bool, None] = None, p: int = 0, s: str = ""
    ) -> None:
        pass


class OverloadedChild(OverloadedParent):
    @overload
    def func(self, *, b: Literal[True]) -> None: ...

    @overload
    def func(self, *, b: Literal[False], p: int) -> None: ...

    @overload
    def func(self, *, s: str) -> None: ...

    def func(
        self, *, b: Union[bool, None] = None, p: int = 0, s: str = ""
    ) -> None:
        pass


class ChildWithWrongImplementation(Parent):
    """The implementation after the overload stubs is still checked."""

    @overload
    def statement(self, future: Literal[None] = ...) -> int: ...

    @overload
    def statement(self, future: Literal[True]) -> str: ...

    def statement(self, future, extra) -> Union[int, str]:  # [arguments-differ]
        pass


class ChildWithoutOverload(Parent):
    def statement(self, future, extra):  # [arguments-differ]
        pass
