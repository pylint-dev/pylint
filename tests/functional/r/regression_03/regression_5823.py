# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/5823

@dataclass(slots=True) subclass with super().method() should not suggest super-with-arguments.

Fix landed before pylint 2.13 (oldest Python-3.12-compatible version).
"""

# pylint: disable=missing-docstring,too-few-public-methods
from dataclasses import dataclass


@dataclass(slots=True)
class _Animal:
    name: str
    num_arms: int
    num_legs: int

    def greet(self):
        print(f"Hi, my name is {self.name}")


@dataclass(slots=True)
class Bird(_Animal):
    num_arms: int = 0
    num_legs: int = 2

    def greet(self):
        print("Chirp!")
        super().greet()
