"""Tests for missing-raises-doc and missing-raises-type-doc for Sphinx style docstrings
with accept-no-raise-doc = no"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, import-outside-toplevel


def test_sphinx_raises_with_prefix_one(self):
    """This is a sphinx docstring.

    :raises ~re.error: Sometimes
    """
    import re

    raise re.error("hi")


def test_sphinx_raises_with_prefix_two(self):
    """This is a sphinx docstring.

    :raises !re.error: Sometimes
    """
    import re

    raise re.error("hi")
