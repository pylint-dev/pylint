"""Tests for missing-yield-doc and missing-yield-type-doc for Google style docstrings"""
# pylint: disable=missing-function-docstring, unused-argument, function-redefined
# pylint: disable=invalid-name, undefined-variable
import typing


# Test redundant yields docstring variants
def my_func(self):
    """This is a docstring.

    Yields:
        int or None: One, or sometimes None.
    """
    if a_func():
        yield None
    yield 1


def my_func(self):  # [redundant-yields-doc]
    """This is a docstring.

    Yields:
        int: One
    """
    return 1


# Test missing yields typing docstring
def generator() -> typing.Iterator[int]:
    """A simple function for checking type hints.

    Yields:
        The number 0
    """
    yield 0
