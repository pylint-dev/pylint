# pylint: disable=missing-docstring

# Disabled because of a bug with pypy 3.8 see
# https://github.com/pylint-dev/pylint/pull/7918#issuecomment-1352737369
# pylint: disable=multiple-statements

import dataclasses
import typing
from dataclasses import dataclass

import attrs  # pylint: disable=import-error
from attrs import define, frozen  # pylint: disable=import-error


@dataclasses.dataclass
class ScheduledTxSearchModel:
    date_from = None
    date_to = None


@dataclass
class ScheduledTxSearchModelOne:
    date = None


@dataclass(frozen=True)
class Test:
    some_integer: int


class Example(typing.NamedTuple):
    some_int: int


@dataclasses.dataclass(frozen=True)
class Point:
    """A three dimensional point with x, y and z components."""

    attr1: float
    attr2: float
    attr3: float

    def to_array(self):
        """Convert to a NumPy array `np.array((x, y, z))`."""
        return self.attr1


@define
class AttrsBarePoint:
    x: float
    y: float


@frozen
class AttrsBareFrozenPoint:
    x: float
    y: float


@attrs.define
class AttrsQualifiedPoint:
    x: float
    y: float


@attrs.frozen
class AttrsQualifiedFrozenPoint:
    x: float
    y: float
