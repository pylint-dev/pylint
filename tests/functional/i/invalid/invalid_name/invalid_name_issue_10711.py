""" Regression test for https://github.com/pylint-dev/pylint/issues/10711. """

# pylint: disable=missing-class-docstring

from dataclasses import dataclass
from typing import Final

@dataclass
class ExampleClass:
    snake_case_param: Final[int] = 42
    UPPER_CASE_PARAM: Final[int] = 42
