"""Regression test for https://github.com/pylint-dev/pylint/issues/10082

A class attribute that starts as None and is set through
``cls = self.__class__`` supports item assignment and subscript.
"""

# pylint: disable=missing-docstring,too-few-public-methods


def load(name):
    return {"name": name}


class Loader:
    data = None

    def __init__(self, name):
        cls = self.__class__
        cls.data = load(name)
        cls.data["copy"] = cls.data["name"]
