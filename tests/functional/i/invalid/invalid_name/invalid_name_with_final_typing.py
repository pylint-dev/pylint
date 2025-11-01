""" Regression test for https://github.com/pylint-dev/pylint/issues/10711. """

# pylint: disable=missing-class-docstring, missing-function-docstring

from dataclasses import dataclass
from typing import Final

module_snake_case_param: Final[int] = 42  # [invalid-name]
MODULE_UPPER_CASE_PARAM: Final[int] = 42

def example_function() -> None:
    function_snake_case_param: Final[int] = 42 # [invalid-name]
    FUNCTION_UPPER_CASE_PARAM: Final[int] = 42
    print(function_snake_case_param, FUNCTION_UPPER_CASE_PARAM)

@dataclass
class ExampleClass:
    class_snake_case_param: Final[int] = 42 # [invalid-name]
    CLASS_UPPER_CASE_PARAM: Final[int] = 42

    def method(self) -> None:
        method_snake_case_param: Final[int] = 42 # [invalid-name]
        METHOD_UPPER_CASE_PARAM: Final[int] = 42
        print(method_snake_case_param, METHOD_UPPER_CASE_PARAM)
