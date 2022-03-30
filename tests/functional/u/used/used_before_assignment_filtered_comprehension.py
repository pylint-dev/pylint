"""Homonym between filtered comprehension and assignment in except block."""

def func():
    """https://github.com/PyCQA/pylint/issues/5586"""
    try:
        print(value for value in range(1 / 0) if isinstance(value, int))
    except ZeroDivisionError:
        value = 1
        print(value)


def func2():
    """Same, but with attribute access."""
    try:
        print(value for value in range(1 / 0) if isinstance(value.num, int))
    except ZeroDivisionError:
        value = 1
        print(value)


def func3():
    """Same, but with no call."""
    try:
        print(value for value in range(1 / 0) if value)
    except ZeroDivisionError:
        value = 1
        print(value)
