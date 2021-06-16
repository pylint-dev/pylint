# pylint: disable=missing-docstring
from enum import Enum, IntEnum


class Issue1932(IntEnum):
    """https://github.com/PyCQA/pylint/issues/1932"""
    FOO = 1

    def whats_my_name(self):
        return self.name.lower()


class Issue2062(Enum):
    """https://github.com/PyCQA/pylint/issues/2062"""
    FOO = 1
    BAR = 2

    def __str__(self):
        return self.name.lower()
