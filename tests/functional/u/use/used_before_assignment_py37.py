"""Tests for used-before-assignment with functions added in python 3.7"""
# pylint: disable=missing-function-docstring
from __future__ import annotations
from typing import List


class MyClass:
    """With the future import only default values can't refer to the base class"""

    def correct_typing_method(self, other: MyClass) -> bool:
        return self == other

    def second_correct_typing_method(self, other: List[MyClass]) -> bool:
        return self == other[0]

    def incorrect_default_method(
        self, other=MyClass() # [used-before-assignment]
    ) -> bool:
        return self == other

    def correct_string_typing_method(self, other: "MyClass") -> bool:
        return self == other

    def correct_inner_typing_method(self) -> bool:
        def inner_method(self, other: MyClass) -> bool:
            return self == other

        return inner_method(self, MyClass())
