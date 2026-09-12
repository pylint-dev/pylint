# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/2981

An attribute defined in the ``__init__`` of a ``Generic`` base class is known to
the subclass, so assigning it there is neither attribute-defined-outside-init nor
access-member-before-definition.

Clean on every pylint from 2.13 on, the oldest version that runs on Python
3.12. The report was specific to Python 3.6.
"""

# pylint: disable=missing-docstring,too-few-public-methods
from typing import Generic, TypeVar

T = TypeVar("T")


class Base(Generic[T]):
    def __init__(self):
        self.val = False


class Derived(Base[T]):
    def func(self):
        self.val = True

    def read_then_write(self):
        print(self.val)
        self.val = True


a = Derived()
a.func()
print(a.val)


class Annotated(Generic[T]):
    def __init__(self, x: T):
        self.x = x


class Middle(Annotated[T]):
    pass


class Leaf(Middle[int]):
    def set_x(self, x: int) -> None:
        self.x = x
