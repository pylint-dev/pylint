"""Test for old tenrary constructs"""
from UNINFERABLE import condition, true_value, false_value, some_callable  # pylint: disable=import-error

SOME_VALUE1 = true_value if condition else false_value
SOME_VALUE2 = condition and true_value or false_value  # [consider-using-ternary]
SOME_VALUE3 = (false_value, true_value)[condition]  # [consider-using-ternary]


def func1():
    """Tenrary return value correct"""
    return true_value if condition else false_value


def func2():
    """Tenrary return value incorrect"""
    return condition and true_value or false_value  # [consider-using-ternary]


def func3():
    """Tenrary return value incorrect"""
    return (false_value, true_value)[condition]  # [consider-using-ternary]


SOME_VALUE4 = some_callable(condition) and 'ERROR' or 'SUCCESS'  # [consider-using-ternary]
