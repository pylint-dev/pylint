# pylint: disable=missing-docstring, too-few-public-methods

# Disabled because of a bug with pypy 3.8 see
# https://github.com/pylint-dev/pylint/pull/7918#issuecomment-1352737369
# pylint: disable=multiple-statements

from dataclasses import dataclass
from typing import NamedTuple


class Aaaa: # [too-many-instance-attributes]

    def __init__(self):
        self.aaaa = 1
        self.bbbb = 2
        self.cccc = 3
        self.dddd = 4
        self.eeee = 5
        self.ffff = 6
        self.gggg = 7
        self.hhhh = 8
        self.iiii = 9
        self.jjjj = 10
        self._aaaa = 1
        self._bbbb = 2
        self._cccc = 3
        self._dddd = 4
        self._eeee = 5
        self._ffff = 6
        self._gggg = 7
        self._hhhh = 8
        self._iiii = 9
        self._jjjj = 10
        self.tomuch = None


@dataclass
class Foo: # [too-many-instance-attributes]
    one: int
    two: int
    three: int
    four: int
    five: int
    six: int
    seven: int
    eight: int
    nine: int

    def test(self):
        pass


class Bar(NamedTuple): # [too-many-instance-attributes]
    one: int
    two: int
    three: int
    four: int
    five: int
    six: int
    seven: int
    eight: int
    nine: int
    ten: int
    eleven: int

    def test(self):
        pass
