"""Tests for missing-return-doc and missing-return-type-doc for Google style docstrings
with accept-no-returns-doc = no"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def my_func(self):  # [missing-return-type-doc]
    """This is a docstring.

    Returns:
        Always False
    """
    return False


def my_func(self):  # [missing-return-doc]
    """This is a docstring.

    Returns:
        bool:
    """
    return False
