# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/2981

Subclass assigning attr defined in Generic[T] base __init__ should not warn.

Fix landed before pylint 2.13 (oldest Python-3.12-compatible version).
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


a = Derived()
a.func()
print(a.val)
