# pylint: disable=missing-docstring
import dataclasses
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
