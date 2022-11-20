"""Tests for used-before-assignment for typing related issues"""
# pylint: disable=missing-function-docstring


from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    if True:  # pylint: disable=using-constant-test
        import math


class MyClass:
    """Type annotation or default values for first level methods can't refer to their own class"""

    def incorrect_typing_method(
        self, other: MyClass  # [undefined-variable]
    ) -> bool:
        return self == other

    def incorrect_nested_typing_method(
        self, other: List[MyClass]  # [undefined-variable]
    ) -> bool:
        return self == other[0]

    def incorrect_default_method(
        self, other=MyClass()  # [undefined-variable]
    ) -> bool:
        return self == other

    def correct_string_typing_method(self, other: "MyClass") -> bool:
        return self == other

    def correct_inner_typing_method(self) -> bool:
        def inner_method(self, other: MyClass) -> bool:
            return self == other

        return inner_method(self, MyClass())


class MySecondClass:
    """Class to test self referential variable typing.
    This regressed, reported in: https://github.com/PyCQA/pylint/issues/5342
    """

    def self_referential_optional_within_method(self) -> None:
        variable: Optional[MySecondClass] = self
        print(variable)

    def correct_inner_typing_method(self) -> bool:
        def inner_method(self, other: MySecondClass) -> bool:
            return self == other

        return inner_method(self, MySecondClass())


class MyOtherClass:
    """Class to test self referential variable typing, no regression."""

    def correct_inner_typing_method(self) -> bool:
        def inner_method(self, other: MyOtherClass) -> bool:
            return self == other

        return inner_method(self, MyOtherClass())

    def self_referential_optional_within_method(self) -> None:
        variable: Optional[MyOtherClass] = self
        print(variable)


class MyThirdClass:
    """Class to test self referential variable typing within conditionals.
    This regressed, reported in: https://github.com/PyCQA/pylint/issues/5499
    """

    def function(self, var: int) -> None:
        if var < 0.5:
            _x: MyThirdClass = self

    def other_function(self) -> None:
        _x: MyThirdClass = self


class MyFourthClass:  # pylint: disable=too-few-public-methods
    """Class to test conditional imports guarded by TYPE_CHECKING two levels
    up then used in function annotation. See https://github.com/PyCQA/pylint/issues/7539"""

    def comparator(self, comparator: math.isclose, first, second):  # [used-before-assignment]
        """Conditional imports guarded are only valid for variable annotations."""
        comparator(first, second)
