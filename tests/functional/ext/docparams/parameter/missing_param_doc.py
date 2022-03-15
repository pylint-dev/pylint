"""Tests for missing-param-doc and missing-type-doc for non-specified style docstrings
with accept-no-param-doc = yes
"""
# pylint: disable=invalid-name, unused-argument


def test_tolerate_no_param_documentation_at_all(x, y):
    """Example of a function with no parameter documentation at all

    No error message is emitted.

    missing parameter documentation"""
