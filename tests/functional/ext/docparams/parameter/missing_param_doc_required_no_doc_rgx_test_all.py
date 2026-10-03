"""Tests for missing-param-doc and missing-type-doc for non-specified style docstrings
with accept-no-param-doc = no and no-docstring-rgx = ^$
"""
# pylint: disable=invalid-name, unused-argument, too-few-public-methods, function-redefined
# pylint: disable=missing-class-docstring


class MyClass:
    """test_all_docstring_rgx
    Function that matches "check all functions" 'no-docstring-rgx' config option
    No error message is emitted.
    """

    def __init__(self, my_param: int) -> None:
        """
        My init docstring
        :param my_param: My first param
        """


# test_fail_empty_docstring_rgx
# Function that matches "check all functions" 'no-docstring-rgx' config option
# An error message is emitted.
class MyClass:
    def __init__(self, my_param: int) -> None:  # [missing-param-doc]
        """
        My init docstring
        """
