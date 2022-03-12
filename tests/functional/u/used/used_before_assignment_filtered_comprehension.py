"""Homonym between filtered comprehension and assignment in except block."""

def func():
    """https://github.com/PyCQA/pylint/issues/5586"""
    try:
        print(value for value in range(1 / 0) if isinstance(value, int))
    except ZeroDivisionError:
        value = 1
        print(value)
