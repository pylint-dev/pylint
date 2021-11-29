"""Tests for missing-yield-doc and missing-yield-type-doc with accept-no-yields-doc = no"""
# pylint: disable=missing-function-docstring, unused-argument, function-redefined

# Test missing docstring
def my_func(self):  # [missing-yield-doc, missing-yield-type-doc]
    yield False


# Test partial Sphinx docstring
def my_func(self):  # [missing-yield-type-doc]
    """This is a docstring.

    :returns: Always False
    """
    yield False
