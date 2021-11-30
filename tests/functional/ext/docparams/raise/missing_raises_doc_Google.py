"""Tests for missing-raises-doc and missing-raises-type-doc for Google style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument, import-outside-toplevel


def test_find_missing_google_raises(self):  # [missing-raises-doc]
    """This is a docstring.

    Raises:
        NameError: Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]


def test_find_google_attr_raises_exact_exc(self):
    """This is a google docstring.

    Raises:
        re.error: Sometimes
    """
    import re

    raise re.error("hi")
