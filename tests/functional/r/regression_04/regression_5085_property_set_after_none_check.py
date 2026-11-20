"""Regression test for https://github.com/pylint-dev/pylint/issues/5085

A property that replaces None before returning must not be reported as
returning None.
"""

# pylint: disable=missing-docstring,too-few-public-methods


class Holder:
    def __init__(self):
        self.__value = None

    @property
    def value(self) -> int:
        if self.__value is None:
            self.__value = 42
        return self.__value

    def method(self):
        return "abc"[: -self.value]
