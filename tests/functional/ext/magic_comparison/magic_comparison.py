"""
Checks that magic numbers are not used in comparisons
"""
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods,import-error,wrong-import-position, comparison-of-constants, singleton-comparison

var = 7
if var > 5:  # [magic-comparison]
    pass

if (var + 5) > 10:  # [magic-comparison]
    pass

is_big = 100 < var  # [magic-comparison]

shouldnt_raise = 5 > 7
shouldnt_raise = var == '__main__'
shouldnt_raise = var == ""
shouldnt_raise = var == 1
shouldnt_raise = var == 0
shouldnt_raise = var == -1
shouldnt_raise = var == True
shouldnt_raise = var == False
shouldnt_raise = var == None
