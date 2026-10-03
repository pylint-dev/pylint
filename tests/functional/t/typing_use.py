# pylint: disable=missing-docstring

import typing
from typing import overload

@typing.overload
def double_with_docstring(arg: str) -> str:
    """Return arg, concatenated with itself."""


@typing.overload
def double_with_docstring(arg: int) -> int:
    """Return twice arg."""


def double_with_docstring(arg):
    """Return 2 * arg."""
    return 2 * arg


def double_with_docstring(arg):  # [function-redefined]
    """Redefined function implementation"""
    return 2 * arg


@typing.overload
def double_with_ellipsis(arg: str) -> str:
    ...


@typing.overload
def double_with_ellipsis(arg: int) -> int:
    ...


def double_with_ellipsis(arg):
    return 2 * arg


@typing.overload
def double_with_pass(arg: str) -> str:
    pass


@typing.overload
def double_with_pass(arg: int) -> int:
    pass


def double_with_pass(arg):
    return 2 * arg

# pylint: disable=too-few-public-methods
class Cls:
    @typing.overload
    def method(self, param: int) -> None:
        ...

    @overload
    def method(self, param: str) -> None:
        ...

    def method(self, param):
        return (self, param)
# pylint: enable=too-few-public-methods
