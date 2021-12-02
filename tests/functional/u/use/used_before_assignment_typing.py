"""Tests for used-before-assignment for typing related issues"""
# pylint: disable=missing-function-docstring


from typing import List


class MyClass:
    """Type annotation or default values for first level methods can't refer to their own class"""

    def incorrect_typing_method(
        self, other: MyClass  # [used-before-assignment]
    ) -> bool:
        return self == other

    def incorrect_nested_typing_method(
        self, other: List[MyClass]  # [used-before-assignment]
    ) -> bool:
        return self == other[0]

    def incorrect_default_method(
        self, other=MyClass()  # [used-before-assignment]
    ) -> bool:
        return self == other

    def correct_string_typing_method(self, other: "MyClass") -> bool:
        return self == other

    def correct_inner_typing_method(self) -> bool:
        def inner_method(self, other: MyClass) -> bool:
            return self == other

        return inner_method(self, MyClass())
