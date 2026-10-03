"""Tests for undefined-variable related to decorators"""
# pylint: disable=missing-function-docstring, missing-class-docstring, too-few-public-methods
# pylint: disable=unnecessary-comprehension

# Test that class attributes are in scope for listcomp in decorator.
# Regression reported in https://github.com/pylint-dev/pylint/issues/511

def dec(inp):
    def inner(func):
        print(inp)
        return func
    return inner


class Cls:

    DATA = "foo"

    @dec([x for x in DATA])
    def fun(self):
        pass
