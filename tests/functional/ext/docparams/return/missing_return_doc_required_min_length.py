"""Tests for missing-return-doc for non-specified style docstrings
with accept-no-return-doc = no and docstring-min-length = 3
"""
# pylint: disable=invalid-name

# Example of a function that is less than 'docstring-min-length' config option
# No error message is emitted.
def test_skip_docstring_min_length() -> None:
    """function is too short and is missing return documentation"""
    return None
