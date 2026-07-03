"""Test that unused-import is not emitted here when everything else is disabled

https://github.com/pylint-dev/pylint/issues/3445
https://github.com/pylint-dev/pylint/issues/6089
"""
from math import e, pi
from os import environ

for k, v in environ.items():
    print(k, v)


class MyClass:
    """For the bug reported in #6089 it is important to use the same names for the class attributes as in the imports."""

    e = float(e)
    pi = pi
