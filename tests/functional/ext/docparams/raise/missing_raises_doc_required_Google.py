"""Tests for missing-raises-doc and missing-raises-type-doc for Google style docstrings
with accept-no-raise-doc = no"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, import-outside-toplevel


def test_google_raises_with_prefix_one(self):
    """This is a google docstring.

    Raises:
        ~re.error: Sometimes
    """
    import re

    raise re.error("hi")


def test_google_raises_with_prefix_two(self):
    """This is a google docstring.

    Raises:
        !re.error: Sometimes
    """
    import re

    raise re.error("hi")
