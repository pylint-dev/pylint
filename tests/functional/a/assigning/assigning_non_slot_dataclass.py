# pylint: disable=missing-docstring,too-few-public-methods,attribute-defined-outside-init

# ``@dataclass(slots=True)`` turns the fields into ``__slots__``
# https://github.com/pylint-dev/pylint/issues/7790

import dataclasses
from dataclasses import dataclass
from typing import ClassVar


@dataclass(slots=True)
class NoFields:
    def __init__(self):
        self.x = 1  # [assigning-non-slot]


@dataclass(slots=True)
class Point:
    x: int
    y: int = 0
    scale: ClassVar[int] = 1

    def __post_init__(self):
        self.x = abs(self.x)
        self.z = 0  # [assigning-non-slot]

    def move(self):
        self.y = 1
        self.label = "moved"  # [assigning-non-slot]


@dataclasses.dataclass(slots=True)
class Named:
    name: str

    def rename(self, name):
        self.name = name
        self.nickname = name  # [assigning-non-slot]


@dataclass(slots=True)
class Child(Point):
    z: int = 0

    def update(self):
        self.x = 1
        self.z = 1
        self.w = 1  # [assigning-non-slot]


@dataclass(slots=False)
class NoSlots:
    x: int

    def update(self):
        self.extra = 1


@dataclass
class Plain:
    x: int

    def update(self):
        self.extra = 1


class Unslotted:
    pass


@dataclass(slots=True)
class UnslottedBase(Unslotted):
    x: int

    def update(self):
        self.extra = 1


class Generic:  # not typing.Generic
    pass


@dataclass(slots=True)
class UserGenericBase(Generic):
    x: int

    def update(self):
        self.extra = 1


class Slotted:
    __slots__ = ("base",)


@dataclass(slots=True)
class SlottedBase(Slotted):
    x: int

    def update(self):
        self.base = 1
        # No ``__slots__`` in the class body to compare the layout with
        self.__class__ = SlottedBase
        self.extra = 1  # [assigning-non-slot]


class SlottedOnUnslotted(Unslotted):
    __slots__ = ("base",)

    def update(self):
        self.extra = 1


@dataclass(slots=True)
class SlottedOnUnslottedBase(SlottedOnUnslotted):
    x: int

    def update(self):
        self.extra = 1
