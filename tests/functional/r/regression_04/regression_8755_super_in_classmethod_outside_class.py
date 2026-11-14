"""Regression test for https://github.com/pylint-dev/pylint/issues/8755

``super()`` in a function decorated with ``classmethod`` outside of a class
used to crash.
"""

# pylint: disable=missing-docstring,too-few-public-methods


class Base:
    pass


@classmethod
def method(cls, value):
    result = super(Base, cls).method(value)
    return result
