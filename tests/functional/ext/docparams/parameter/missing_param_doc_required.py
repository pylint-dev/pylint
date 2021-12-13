"""Tests for missing-param-doc and missing-type-doc for non-specified style docstrings
with accept-no-param-doc = no
"""
# pylint: disable=invalid-name, unused-argument


def test_don_t_tolerate_no_param_documentation_at_all(x, y):  # [missing-any-param-doc]
    """Example of a function with no parameter documentation at all

    Missing documentation error message is emitted.

    missing parameter documentation"""


def test_see_tolerate_no_param_documentation_at_all(x, y):
    """Example for the usage of "For the parameters, see"
    to suppress missing-param warnings.

    For the parameters, see :func:`blah`
    """
