"""Regression test for https://github.com/pylint-dev/pylint/issues/3045

A class attribute that starts as None and is set in a classmethod must not
be reported as not supporting membership tests.
"""

# pylint: disable=missing-docstring,too-few-public-methods


def find_all():
    return [1, 2, 3]


class Registry:
    _all = None

    @classmethod
    def all(cls):
        if not cls._all:
            cls._all = find_all()
        return cls._all

    @classmethod
    def exists(cls, number):
        return number in cls.all()
