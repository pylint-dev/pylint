"""Test for old tenrary constructs"""
from UNINFERABLE import condition, true_value, false_value, some_callable  # pylint: disable=import-error

SOME_VALUE1 = true_value if condition else false_value
SOME_VALUE2 = condition and true_value or false_value  # [consider-using-ternary]
SOME_VALUE3 = (false_value, true_value)[condition]  # [consider-using-ternary]


def func1():
    """Ternary return value correct"""
    return true_value if condition else false_value


def func2():
    """Ternary return value incorrect"""
    return condition and true_value or false_value  # [consider-using-ternary]


def func3():
    """Ternary return value incorrect"""
    return (false_value, true_value)[condition]  # [consider-using-ternary]


SOME_VALUE4 = some_callable(condition) and 'ERROR' or 'SUCCESS'  # [consider-using-ternary]
SOME_VALUE5 = SOME_VALUE1 > 3 and 'greater' or 'not greater'  # [consider-using-ternary]
SOME_VALUE6 = (SOME_VALUE2 > 4 and SOME_VALUE3) and 'both' or 'not'  # [consider-using-ternary]
SOME_VALUE7 = 'both' if (SOME_VALUE2 > 4) and (SOME_VALUE3) else 'not'
SOME_VALUE8 = SOME_VALUE1 and SOME_VALUE2 and SOME_VALUE3 or SOME_VALUE4
SOME_VALUE9 = SOME_VALUE1 and False or SOME_VALUE2  # [simplify-boolean-expression]

YEAR = 1992
# Cannot be simplified with a ternary.
IS_LEAP_YEAR = YEAR % 4 == 0 and YEAR % 100 != 0 or YEAR % 400 == 0


def func4():
    """"Using a Name as a condition but still emits"""
    truth_value = 42
    return condition and truth_value or false_value # [consider-using-ternary]
