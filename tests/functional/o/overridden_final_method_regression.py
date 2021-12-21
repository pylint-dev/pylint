"""Test a crash regression for the overridden-final-method checker on uninferable decorators"""


@unknown_decorator  # [undefined-variable]
def crash_test():
    """A docstring"""
