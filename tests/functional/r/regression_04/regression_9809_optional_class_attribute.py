"""Regression test for https://github.com/pylint-dev/pylint/issues/9809

A class attribute that starts as None and is set to a dict through ``cls``
supports item assignment, subscript and membership tests.
"""

# pylint: disable=missing-docstring,too-few-public-methods


class Config:
    values: dict | None = None

    @classmethod
    def init(cls):
        if cls.values is None:
            cls.values = {}
        cls.values[1] = 2
        _ = cls.values[1]
        _ = 1 in cls.values
