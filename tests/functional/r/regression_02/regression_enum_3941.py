"""
Regression test for https://github.com/PyCQA/pylint/issues/3941

E1101: Class 'Veg' has no '_value2member_map_' member (no-member)
"""

# pylint: disable=protected-access

from enum import Enum


class Veg(Enum):
    ...


print(Veg._value2member_map_)
