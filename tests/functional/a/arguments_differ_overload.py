"""Overload stubs in a subclass are not compared to the overridden method.

https://github.com/pylint-dev/pylint/issues/5264
https://github.com/pylint-dev/pylint/issues/10186
"""
# pylint: disable=missing-docstring,unused-argument,too-few-public-methods
from abc import ABC, abstractmethod
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


class ChildOfOverloaded(OverloadedParent):
    """Compared with the parent's implementation, not its first overload stub."""

    def func(
        self, *, b: Union[bool, None] = None, p: int = 0, s: str = ""
    ) -> None:
        pass


class WrongChildOfOverloaded(OverloadedParent):
    def func(self, extra, *, b=None, p=0, s="") -> None:  # [arguments-differ]
        pass


class AbstractStaticParent(ABC):
    @staticmethod
    @abstractmethod
    @overload
    def func(*, b: Literal[True]) -> None: ...

    @staticmethod
    @abstractmethod
    @overload
    def func(*, b: Literal[False], p: int) -> None: ...

    @staticmethod
    @abstractmethod
    @overload
    def func(*, s: str) -> None: ...

    @staticmethod
    @abstractmethod
    def func(
        *, b: Union[bool, None] = None, p: Union[int, None] = None, s: str = ""
    ) -> None:
        """The implementation"""


class StaticChild(AbstractStaticParent):
    @staticmethod
    @overload
    def func(*, b: Literal[True]) -> None: ...

    @staticmethod
    @overload
    def func(*, b: Literal[False], p: int) -> None: ...

    @staticmethod
    @overload
    def func(*, s: str) -> None: ...

    @staticmethod
    def func(
        *, b: Union[bool, None] = None, p: Union[int, None] = None, s: str = ""
    ) -> None:
        pass


class StubOnlyParent:
    """Without an implementation the first overload stub is the reference."""

    @overload
    def func(self, a: int) -> int: ...

    @overload
    def func(self, a: str) -> str: ...


class ChildOfStubOnly(StubOnlyParent):
    def func(self, a):
        return a


class WrongChildOfStubOnly(StubOnlyParent):
    def func(self, a, extra):  # [arguments-differ]
        return a
