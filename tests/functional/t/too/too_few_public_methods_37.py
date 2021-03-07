# pylint: disable=missing-docstring
import dataclasses
import typing
from dataclasses import dataclass


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
