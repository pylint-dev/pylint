"""Regression test for https://github.com/pylint-dev/pylint/issues/3586

A function decorated with a decorator named like a property (``lazy``)
outside a class is a function, not a property.
"""

# pylint: disable=missing-docstring,unused-argument


def lazy(func):
    def wrapped(*args, **kwargs):
        return 1

    return wrapped


@lazy
def function(value):
    return value


def main():
    result = function("value")
    return result
