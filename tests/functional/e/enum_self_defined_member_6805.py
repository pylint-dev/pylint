"""Tests for self-defined Enum members (https://github.com/pylint-dev/pylint/issues/6805)"""
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
from enum import IntEnum


class Foo(type):
    pass


class Parent:
    def __new__(cls, *_args, **_kwargs):
        return object.__new__(cls)


class NotEnumHasDynamicGetAttrMetaclass(metaclass=Foo):
    def __new__(cls):
        return Parent.__new__(cls)

    def __getattr__(self, item):
        return item

    def magic(self):
        return self.dynamic


NotEnumHasDynamicGetAttrMetaclass().magic()


class Day(IntEnum):
    MONDAY = (1, "Mon")
    TUESDAY = (2, "Tue")
    WEDNESDAY = (3, "Wed")
    THURSDAY = (4, "Thu")
    FRIDAY = (5, "Fri")
    SATURDAY = (6, "Sat")
    SUNDAY = (7, "Sun")

    def __new__(cls, value, _abbr=None):
        return int.__new__(cls, value)


print(Day.FRIDAY.foo)  # [no-member]
