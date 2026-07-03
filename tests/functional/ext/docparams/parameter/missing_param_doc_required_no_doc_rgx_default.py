"""Tests for missing-param-doc and missing-type-doc for non-specified style docstrings
with accept-no-param-doc = no and the default value of no-docstring-rgx
"""
# pylint: disable=invalid-name, unused-argument


def _test_skip_no_docstring_rgx(x, y):
    """Example of a function that matches the default 'no-docstring-rgx' config option

    No error message is emitted.
    """
