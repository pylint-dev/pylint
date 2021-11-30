"""Tests for missing-raises-doc and missing-raises-type-doc for Google style docstrings"""
# pylint: disable=function-redefined, invalid-name, undefined-variable, missing-function-docstring
# pylint: disable=unused-argument


def test_find_missing_google_raises(self):  # [missing-raises-doc]
    """This is a docstring.

    Raises:
        NameError: Never
    """
    raise RuntimeError("hi")
    raise NameError("hi")  # [unreachable]
