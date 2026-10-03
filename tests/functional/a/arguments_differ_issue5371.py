"""https://github.com/pylint-dev/pylint/issues/5371"""
from enum import Enum


class MyEnum(Enum):
    """
    Enum._generate_next_value_() in the stdlib currently lacks a
    @staticmethod decorator.
    """

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list):
        return 42
