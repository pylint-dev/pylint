"""Regression test for https://github.com/pylint-dev/pylint/issues/11609

A slice of a call used as a base class used to crash the class checker.
"""

# pylint: disable=missing-docstring,too-few-public-methods,no-value-for-parameter,inherit-non-class

from typing import Unpack


class Broken(Unpack()[:]):
    pass
