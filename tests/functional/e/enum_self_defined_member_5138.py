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
        self.text = text
        self.unit = unit
        if is_imperial:
            self.suffix = " (imp)"
        else:
            self.suffix = ""


print(f"100 {Length.METRE.unit}{Length.METRE.suffix}")
print(Length.MILE.foo)  # [no-member]
