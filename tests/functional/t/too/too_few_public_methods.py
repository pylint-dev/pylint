# pylint: disable=missing-docstring


from enum import Enum


class Aaaa: # [too-few-public-methods]

    def __init__(self):
        pass

    def meth1(self):
        print(self)

    def _dontcount(self):
        print(self)


# Don't emit for these cases.
class Klass:
    """docstring"""

    def meth1(self):
        """first"""

    def meth2(self):
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


class PropertyCalls:
    """Properties built via a direct ``property(...)`` call still count."""
    id = property(lambda self: None)
    name = property(lambda self: None)


def make_property():
    def getter(_self):
        pass

    return property(getter)


class PropertyFactory:
    """Properties returned from a helper function still count."""
    id = make_property()
    name = make_property()


class Descriptor: # [too-few-public-methods]
    """A data descriptor with a single dunder method: still too few."""
    def __get__(self, instance, owner=None):
        pass


class Descriptors:
    """Descriptor instances used as class attributes still count."""
    id = Descriptor()
    name = Descriptor()
