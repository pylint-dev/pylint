# pylint: disable=missing-docstring
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


class DumbList(object):
    """A class can define only special methods."""
    def __setattr__(self, key, value):
        return key + value

    def __len__(self):
        return 0

    def __getitem__(self, index):
        return index
