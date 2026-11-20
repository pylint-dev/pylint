"""Regression test for https://github.com/pylint-dev/pylint/issues/7891

``self`` in a method of a ``typing.NamedTuple`` subclass has the namedtuple
API and the tuple methods. Fixed in astroid by pylint-dev/astroid#3476.
"""

# pylint: disable=missing-docstring

from typing import NamedTuple


class Fruit(NamedTuple):
    name: str
    color: str

    def describe(self):
        return self._asdict(), self._replace(color="red"), self._fields

    def count_apples(self):
        return self.count("apple"), self.index(self.name)

    def first_and_all(self):
        return self[0], list(self)
