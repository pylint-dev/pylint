"""
Checks that magic values are not used in comparisons
"""
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods,import-error,wrong-import-position

from enum import Enum


class Christmas(Enum):
    EVE = 25
    DAY = 26
    MONTH = 12


var = 7
if var > 5:  # [magic-value-comparison]
    pass

if (var + 5) > 10:  # [magic-value-comparison]
    pass

is_big = 100 < var  # [magic-value-comparison]

shouldnt_raise = 5 > 7   # [comparison-of-constants]
shouldnt_raise = var == '__main__'
shouldnt_raise = var == 1
shouldnt_raise = var == 0
shouldnt_raise = var == -1
shouldnt_raise = var == True  # [singleton-comparison]
shouldnt_raise = var == False  # [singleton-comparison]
shouldnt_raise = var == None  # [singleton-comparison]
celebration_started = Christmas.EVE.value == Christmas.MONTH.value
shouldnt_raise = var == ""

shouldnt_raise = var == '\n'
shouldnt_raise = var == '\\b'

should_escape = var == "foo\nbar"  # [magic-value-comparison]
