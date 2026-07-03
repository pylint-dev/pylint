# pylint: disable=missing-docstring,invalid-name

from enum import Enum

class Color(Enum):
    red = 1
    green = 2
    blue = 3

    def __lt__(self, other):
        return self.value < other.value
