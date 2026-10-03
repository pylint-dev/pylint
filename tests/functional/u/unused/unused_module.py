"""Regression test for unused-module.
Reported in https://bitbucket.org/logilab/pylint/issue/78/
"""

from sys import path

path += ["stuff"]


def func():
    """A function"""
    other = 1
    return len(other)
