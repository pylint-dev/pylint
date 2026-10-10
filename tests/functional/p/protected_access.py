"""Tests for protected_access"""
# pylint: disable=missing-class-docstring, too-few-public-methods, pointless-statement
# pylint: disable=missing-function-docstring, invalid-metaclass, no-member
# pylint: disable=no-self-argument, undefined-variable, unused-variable

import os
from typing import Generic, TypeVar

# Test that exclude-protected can be used to exclude names from protected-access warning
class Protected:
    def __init__(self):
        self._meta = 42
        self._manager = 24
        self._teta = 29


OBJ = Protected()
OBJ._meta
OBJ._manager
OBJ._teta  # [protected-access]


class Light:
    @property
    def _light_internal(self) -> None:
        return None

    @staticmethod
    def func(light) -> None:
        print(light._light_internal)  # [protected-access]


def func(light: Light) -> None:
    print(light._light_internal)  # [protected-access]


# os._exit is excluded from the protected-access check by default
print(os._exit)

# BaseTomato._sauce is included in the `exclude-protected` list
# and does not emit a `protected-access` message:
class BaseTomato:
    _sauce = 42


# Calling a protected method through a subscripted generic base is fine,
# as it is for a plain base class.
T = TypeVar("T")


class GenericParent(Generic[T]):
    def _foo(self):
        pass


class GenericChild(GenericParent[T]):
    def _foo(self):
        GenericParent._foo(self)
