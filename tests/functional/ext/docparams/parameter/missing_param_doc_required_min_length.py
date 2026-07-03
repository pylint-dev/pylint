"""Tests for missing-param-doc and missing-type-doc for non-specified style docstrings
with accept-no-param-doc = no and docstring-min-length = 3
"""
# pylint: disable=invalid-name, unused-argument

# Example of a function that is less than 'docstring-min-length' config option
# No error message is emitted.
def test_skip_docstring_min_length(x, y):
    """function is too short and is missing parameter documentation"""
