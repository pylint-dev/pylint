"""Regression test for https://github.com/pylint-dev/pylint/issues/9879"""
# pylint: disable=missing-function-docstring


def func(mode):
    if mode == "a":
        pass
    elif mode == "b":
        x = 1
    elif mode == "c":
        pass
    else:
        assert False
    print(x)  # [possibly-used-before-assignment]
