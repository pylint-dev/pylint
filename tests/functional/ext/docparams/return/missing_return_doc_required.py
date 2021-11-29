"""Tests for missing-return-doc and missing-return-type-doc with accept-no-returns-doc = no"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def my_func(self):  # [missing-return-doc, missing-return-type-doc]
    return False


# Ignore unknown style
def my_func(self):
    """This is a docstring."""
    return False
