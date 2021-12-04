"""Tests for missing-yield-doc and missing-yield-type-doc for Sphinx style docstrings"""
# pylint: disable=missing-function-docstring, unused-argument, function-redefined
# pylint: disable=invalid-name, undefined-variable
import typing


# Test missing yields typing docstring
def generator() -> typing.Iterator[int]:
    """A simple function for checking type hints.

    :returns: The number 0
    """
    yield 0
