# pylint: disable=invalid-name,missing-docstring,too-few-public-methods

# Slots with base that inherits from 'Generic'
# https://github.com/pylint-dev/pylint/issues/4509
# https://github.com/pylint-dev/astroid/issues/999

from typing import Generic, TypeVar
T = TypeVar("T")

class Base(Generic[T]):
    __slots__ = ()

class Foo(Base[T]):
    __slots__ = ['_value']

    def __init__(self, value: T):
        self._value = value
        self._bar = value  # [assigning-non-slot]
