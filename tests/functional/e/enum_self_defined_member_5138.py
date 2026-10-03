"""Tests for self-defined Enum members (https://github.com/pylint-dev/pylint/issues/5138)"""
# pylint: disable=missing-docstring
from enum import IntEnum, Enum


class Day(IntEnum):
    MONDAY = (1, "Mon")
    TUESDAY = (2, "Tue")
    WEDNESDAY = (3, "Wed")
    THURSDAY = (4, "Thu")
    FRIDAY = (5, "Fri")
    SATURDAY = (6, "Sat")
    SUNDAY = (7, "Sun")

    def __new__(cls, value, abbr=None):
        obj = int.__new__(cls, value)
        obj._value_ = value
        if abbr:
            obj.abbr = abbr
        else:
            obj.abbr = ""
        return obj

    def __repr__(self):
        return f"{self._value_}: {self.foo}"  # [no-member]


print(Day.FRIDAY.abbr)
print(Day.FRIDAY.foo)  # [no-member]


class Length(Enum):
    METRE = "metre", "m"
    MILE = "mile", "m", True

    def __init__(self, text: str, unit: str,  is_imperial: bool = False):
        self.text: str = text
        self.unit: str = unit
        if is_imperial:
            self.suffix = " (imp)"
        else:
            self.suffix = ""


print(f"100 {Length.METRE.unit}{Length.METRE.suffix}")
print(Length.MILE.foo)  # [no-member]


class Binary(int, Enum):
    ZERO = 0
    ONE = 1

    def __init__(self, value: int) -> None:
        super().__init__()
        self.str, self.inverse = str(value), abs(value - 1)

        def no_op(_value):
            pass
        value_squared = value ** 2
        no_op(value_squared)


print(f"1={Binary.ONE.value} (Inverted: {Binary.ONE.inverse}")
