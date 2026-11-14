"""Regression test for https://github.com/pylint-dev/pylint/issues/8325

``__new__`` receives the class explicitly, so passing it is enough.
"""

# pylint: disable=missing-docstring,too-few-public-methods


class Thing:
    def copy(self):
        self.__new__(type(self))
        type(self).__new__(type(self))
