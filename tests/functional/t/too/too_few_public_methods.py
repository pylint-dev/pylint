# pylint: disable=missing-docstring


from enum import Enum


class Aaaa: # [too-few-public-methods]

    def __init__(self) -> None:
        pass

    def meth1(self) -> None:
        print(self)

    def _dontcount(self) -> None:
        print(self)


# Don't emit for these cases.
class Klass:
    """docstring"""

    def meth1(self) -> None:
        """first"""

    def meth2(self) -> None:
        """second"""


class EnoughPublicMethods(Klass):
    """We shouldn't emit too-few-public-methods for this."""


class BossMonster(Enum):
    """An enum does not need methods to be useful."""
    MEGASHARK = 1
    OCTOPUS = 2


class DumbList:
    """A class can define only special methods."""
    def __init__(self, iterable):
        self._list = list(iterable)

    def __len__(self):
        return len(self._list)

    def __getitem__(self, index):
        return self._list[index]
