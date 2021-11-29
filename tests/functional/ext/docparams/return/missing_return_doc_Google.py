"""Tests for missing-return-doc and missing-return-type-doc for Google style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def my_func(self):
    """This is a docstring.

    Returns:
        bool: Always False
    """
    return False
