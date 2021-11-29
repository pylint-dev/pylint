"""Tests for missing-return-doc and missing-return-type-doc"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def my_func(self):
    return False


# Ignore unknown style
def my_func(self):
    """This is a docstring."""
    return False
