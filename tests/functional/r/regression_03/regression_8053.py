# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/8053

Inherited descriptor with __slots__=() should not trigger assigning-non-slot.

Fix landed before pylint 2.13 (oldest Python-3.12-compatible version).
"""

# pylint: disable=missing-docstring,too-few-public-methods,unused-argument,invalid-name
from typing import Any, cast


class MyDescriptor:
    __slots__ = ("offset", "value")

    def __init__(self, offset: int) -> None:
        self.offset = offset
        self.value = 0

    def __set__(self, instance: Any, value: int) -> None:
        self.value = value

    def __get__(self, instance: Any, owner: Any) -> int:
        return self.value


class Parent:
    __slots__ = ()
    MyParentField = MyDescriptor(0)

    def copy(self) -> "Parent":
        return type(self)()


class Child(Parent):
    __slots__ = ()
    MyChildField = MyDescriptor(1)

    def copy(self) -> "Child":
        return cast(Child, super().copy())


if __name__ == "__main__":
    child = Child()
    child.MyChildField = 0
    child.MyParentField = 0
