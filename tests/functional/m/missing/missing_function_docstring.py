"""Tests for missing-function-docstring"""
# pylint: disable=unused-argument, missing-class-docstring, too-few-public-methods, unused-variable


def func(tion):  # [missing-function-docstring]
    pass


def func_two(tion):
    """Documented"""

    def inner(fun):
        # Not documented
        pass


class MyClass:
    def __init__(self, my_param: int) -> None:  # [missing-function-docstring]
        pass
