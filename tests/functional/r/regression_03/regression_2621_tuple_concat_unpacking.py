"""Regression test for https://github.com/pylint-dev/pylint/issues/2621.

Concatenating tuples keeps the length of the result even when an element has
several possible values, so the unpacking below is balanced.
"""

# pylint: disable=missing-function-docstring


def make_pair():
    value = get_value()
    return 1, value


def get_value():
    value = 1
    if value < 0:
        value = -value
    return value


def make_triple():
    return make_pair() + (3,)


FIRST, SECOND, THIRD = make_triple()
