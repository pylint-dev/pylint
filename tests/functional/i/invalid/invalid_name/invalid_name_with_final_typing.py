"""Regression test for https://github.com/pylint-dev/pylint/issues/10711."""

# pylint: disable=missing-class-docstring, missing-function-docstring

from dataclasses import dataclass
from typing import Final

module_snake_case_constant: Final[int] = 42  # [invalid-name]
MODULE_UPPER_CASE_CONSTANT: Final[int] = 42


def function() -> None:
    function_snake_case_constant: Final[int] = 42  # [invalid-name]
    FUNCTION_UPPER_CASE_CONSTANT: Final[int] = 42
    print(function_snake_case_constant, FUNCTION_UPPER_CASE_CONSTANT)


@dataclass
class Class:
    class_snake_case_constant: Final[int] = 42  # [invalid-name]
    CLASS_UPPER_CASE_CONSTANT: Final[int] = 42

    def method(self) -> None:
        method_snake_case_constant: Final[int] = 42  # [invalid-name]
        METHOD_UPPER_CASE_CONSTANT: Final[int] = 42
        print(method_snake_case_constant, METHOD_UPPER_CASE_CONSTANT)
