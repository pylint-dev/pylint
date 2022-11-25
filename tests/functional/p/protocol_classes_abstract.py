"""Test that classes inheriting from protocols should not warn about abstract-method."""

# pylint: disable=too-few-public-methods,disallowed-name,invalid-name

from abc import abstractmethod
from typing import Protocol, Literal


class FooProtocol(Protocol):
    """Foo Protocol"""

    @abstractmethod
    def foo(self) -> Literal["foo"]:
        """foo method"""

    def foo_no_abstract(self) -> Literal["foo"]:
        """foo not abstract method"""


class BarProtocol(Protocol):
    """Bar Protocol"""
    @abstractmethod
    def bar(self) -> Literal["bar"]:
        """bar method"""


class FooBarProtocol(FooProtocol, BarProtocol, Protocol):
    """FooBar Protocol"""


class IndirectProtocol(FooProtocol):
    """Doesn't subclass typing.Protocol directly"""


class FooBar(FooBarProtocol):
    """FooBar object"""

    def bar(self) -> Literal["bar"]:
        return "bar"

    def foo(self) -> Literal["foo"]:
        return "foo"
