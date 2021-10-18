"""Tests for used-before-assignment with functions added in python 3.7"""
# pylint: disable=missing-function-docstring
from __future__ import annotations


class MyClass:
    """With the future import only default values can't refer to the base class"""

    def incorrect_method(self, other: MyClass) -> bool:
        return self == other

    def second_incorrect_method(
        self, other=MyClass() # [used-before-assignment]
    ) -> bool:
        return self == other

    def correct_method(self, other: "MyClass") -> bool:
        return self == other

    def second_correct_method(self) -> bool:
        def inner_method(self, other: MyClass) -> bool:
            return self == other

        return inner_method(self, MyClass())
