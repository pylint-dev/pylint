"""Regression test for https://github.com/pylint-dev/pylint/issues/10711."""

# pylint: disable=missing-class-docstring, missing-function-docstring

from dataclasses import dataclass
from typing import ClassVar, Final

module_snake_case_constant: Final[int] = 42  # [invalid-name]
MODULE_UPPER_CASE_CONSTANT: Final[int] = 42


def function() -> None:
    function_snake_case_constant: Final[int] = 42
    FUNCTION_UPPER_CASE_CONSTANT: Final[int] = 42  # [invalid-name]
    print(function_snake_case_constant, FUNCTION_UPPER_CASE_CONSTANT)


@dataclass
class Class:
    class_snake_case_constant: ClassVar[Final[int]] = 42  # [invalid-name]
    CLASS_UPPER_CASE_CONSTANT: ClassVar[Final[int]] = 42

    field_annotated_with_final: Final[int] = 42
    FIELD_ANNOTATED_WITH_FINAL: Final[int] = 42

    def method(self) -> None:
        method_snake_case_constant: Final[int] = 42
        METHOD_UPPER_CASE_CONSTANT: Final[int] = 42  # [invalid-name]
        print(method_snake_case_constant, METHOD_UPPER_CASE_CONSTANT)
