# [missing-module-docstring]
from enum import IntEnum


class Day(IntEnum):  # [missing-class-docstring]
    MONDAY = (1, "Mon")
    TUESDAY = (2, "Tue")
    WEDNESDAY = (3, "Wed")
    THURSDAY = (4, "Thu")
    FRIDAY = (5, "Fri")
    SATURDAY = (6, "Sat")
    SUNDAY = (7, "Sun")

    def __new__(cls, value, abbr):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.abbr = abbr
        return obj


print(Day.FRIDAY.abbr)
print(Day.FRIDAY.foo)  # [no-member]
