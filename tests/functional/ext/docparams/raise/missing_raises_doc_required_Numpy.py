"""Tests for missing-raises-doc and missing-raises-type-doc for Numpy style docstrings
with accept-no-raise-doc = no"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, import-outside-toplevel


def test_numpy_raises_with_prefix_one(self):
    """This is a numpy docstring.

    Raises
    ------
    ~re.error
        Sometimes
    """
    import re

    raise re.error("hi")


def test_numpy_raises_with_prefix_two(self):
    """This is a numpy docstring.

    Raises
    ------
    !re.error
        Sometimes
    """
    import re

    raise re.error("hi")
