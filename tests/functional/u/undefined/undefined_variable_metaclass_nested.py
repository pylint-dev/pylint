"""Tests for undefined-variable false positive when a name is used as a metaclass
in a nested class inside a method, and then used again at module level.

https://github.com/pylint-dev/pylint/issues/10823
"""
# pylint: disable=too-few-public-methods,missing-class-docstring,missing-function-docstring
# pylint: disable=unused-variable,pointless-statement

import abc


class Test:
    def test1(self):
        class A(metaclass=abc.ABCMeta):
            pass


# This should NOT trigger undefined-variable — abc was imported at module level
# and consumed by the metaclass usage, but it should still be resolvable.
abc.ABCMeta
