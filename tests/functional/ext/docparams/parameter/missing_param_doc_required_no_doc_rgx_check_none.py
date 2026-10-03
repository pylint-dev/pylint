"""Tests for missing-param-doc and missing-type-doc for non-specified style docstrings
with accept-no-param-doc = no and no-docstring-rgx = ""
"""
# pylint: disable=invalid-name, unused-argument, too-few-public-methods


class MyClass:
    """test_no_docstring_rgx
    Function that matches "check no functions" 'no-docstring-rgx' config option
    No error message is emitted.
    """

    def __init__(self, my_param: int) -> None:
        """
        My init docstring
        """
