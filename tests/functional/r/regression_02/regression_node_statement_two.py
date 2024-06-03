"""Test to see we don't crash on this code in pandas.
See: https://github.com/pandas-dev/pandas/blob/main/pandas/core/indexes/period.py
Reported in https://github.com/pylint-dev/pylint/issues/5382
"""
# pylint: disable=missing-function-docstring, missing-class-docstring, unused-argument
# pylint: disable=too-few-public-methods, no-method-argument, invalid-name


def my_decorator(*params):
    def decorator(decorated):
        return decorated

    return decorator


class ClassWithProperty:
    def f():
        return "string"

    f.__name__ = "name"
    f.__doc__ = "docstring"

    hour = property(f)


class ClassWithDecorator:
    @my_decorator(ClassWithProperty.hour.fget)
    def my_property(self) -> str:
        return "a string"
