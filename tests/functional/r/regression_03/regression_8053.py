# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/8053

An inherited descriptor should not trigger assigning-non-slot, including on an
instance returned by a method annotated with the subclass.

Regressed in pylint 3.0.0 and still present in pylint 4.0.5; fixed by astroid
4.1.0. Only the last block reproduces it.
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

    child_copy = child.copy()
    child_copy.MyParentField = 0
    child_copy.MyChildField = 0
