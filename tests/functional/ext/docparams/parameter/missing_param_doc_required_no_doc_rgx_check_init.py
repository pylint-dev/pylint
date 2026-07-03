"""Tests for missing-param-doc and missing-type-doc for non-specified style docstrings
with accept-no-param-doc = no and no-docstring-rgx = ^(?!__init__$)_
"""
# pylint: disable=invalid-name, unused-argument, too-few-public-methods, missing-class-docstring


# test_fail_docparams_check_init
# Check that __init__ is checked correctly, but other private methods aren't
class MyClass:
    def __init__(self, my_param: int) -> None:  # [missing-param-doc]
        """
        My init docstring
        """

    def _private_method(self, my_param: int) -> None:
        """
        My private method
        """
