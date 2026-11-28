"""Check each assignment to a misnamed attribute in its defining class."""
# pylint: disable=missing-class-docstring,missing-function-docstring

from typing import Final


class Counter:
    def __init__(self):
        self.currentValue = 0  # [invalid-name]

    def reset(self):
        self.currentValue = 0  # pylint: disable=invalid-name

    def update(self, value):
        self.currentValue = value  # [invalid-name]


class Constant:  # pylint: disable=too-few-public-methods
    def copy_from(self, other):
        self.OTHER_VALUE = other  # [invalid-name]

    def __init__(self):
        self.OTHER_VALUE: Final[int] = 1
