# pylint: disable=missing-docstring, useless-object-inheritance
from __future__ import print_function


from enum import Enum


class Aaaa(object): # [too-few-public-methods]

    def __init__(self):
        pass

    def meth1(self):
        print(self)

    def _dontcount(self):
        print(self)


# Don't emit for these cases.
class Klass(object):
    """docstring"""

    def meth1(self):
        """first"""

    def meth2(self):
        """second"""


class EnoughPublicMethods(Klass):
    """We shouldn't emit too-few-public-methods for this."""


class BossMonster(Enum):
    """An enum does not need methods to be useful."""
    megashark = 1
    octopus = 2


class DumbList:
    """A class can define only special methods."""
    def __init__(self, iterable):
        self._list = list(iterable)

    def __len__(self):
        return len(self._list)

    def __getitem__(self, index):
        return self._list[index]
