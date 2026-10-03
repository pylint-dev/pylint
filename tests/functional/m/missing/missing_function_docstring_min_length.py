"""Tests for missing-function-docstring and the min-length option"""
# pylint: disable=unused-argument, unnecessary-pass, bare-except


def func(tion):
    pass


def func_two(tion):  # [missing-function-docstring]
    pass
    pass


def func_three(tion):  # [missing-function-docstring]
    try:
        pass
    except:
        pass


def __fun__(tion):
    pass
