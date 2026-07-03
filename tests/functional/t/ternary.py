"""Test for old ternary constructs"""
from UNINFERABLE import condition, some_callable, maybe_true, maybe_false  # pylint: disable=import-error

TRUE_VALUE = True
FALSE_VALUE = False

SOME_VALUE1 = TRUE_VALUE if condition else FALSE_VALUE
SOME_VALUE2 = condition and TRUE_VALUE or FALSE_VALUE  # [consider-using-ternary]
NOT_SIMPLIFIABLE_1 = maybe_true if condition else maybe_false
NOT_SIMPLIFIABLE_2 = condition and maybe_true or maybe_false
SOME_VALUE3 = condition

def func1():
    """Ternary return value correct"""
    return TRUE_VALUE if condition else FALSE_VALUE


def func2():
    """Ternary return value incorrect"""
    return condition and TRUE_VALUE or FALSE_VALUE  # [consider-using-ternary]


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
    return condition and truth_value or FALSE_VALUE # [consider-using-ternary]


def func5():
    """"Using a Name that infers to False as a condition does not emit"""
    falsy_value = False
    return condition and falsy_value or FALSE_VALUE # [simplify-boolean-expression]


def func_control_flow():
    """Redefining variables should invalidate simplify-boolean-expression."""
    flag_a = False
    flag_b = False
    for num in range(2):
        if num == 1:
            flag_a = True
        else:
            flag_b = True
    multiple = (flag_a and flag_b) or func5()
    return multiple
