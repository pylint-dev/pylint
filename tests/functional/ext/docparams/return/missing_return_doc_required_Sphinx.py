"""Tests for missing-return-doc and missing-return-type-doc for Sphinx style docstrings
with accept-no-returns-doc = no"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def my_func(self):  # [missing-return-type-doc]
    """This is a docstring.

    :returns: Always False
    """
    return False


def my_func(self) -> bool:
    """This is a docstring.

    :returns: Always False
    """
    return False
