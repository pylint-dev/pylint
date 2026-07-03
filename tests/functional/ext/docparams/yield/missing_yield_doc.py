"""Tests for missing-yield-doc and missing-yield-type-doc"""
# pylint: disable=missing-function-docstring, unused-argument, function-redefined

# Ignore no docstring
def my_func(self):
    yield False


# Ignore unrecognized style docstring
def my_func(self):
    """This is a docstring."""
    yield False
