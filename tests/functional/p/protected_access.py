"""Tests for protected_access"""
# pylint: disable=missing-class-docstring, too-few-public-methods, pointless-statement
# pylint: disable=missing-function-docstring, invalid-metaclass, no-member
# pylint: disable=no-self-argument, no-self-use, undefined-variable, unused-variable

# Test that exclude-protected can be used to exclude names from protected-access warning
class Protected:
    def __init__(self):
        self._meta = 42
        self._manager = 24
        self._teta = 29


OBJ = Protected()
OBJ._meta
OBJ._manager
OBJ._teta  # [protected-access]


# Make sure protect-access doesn't raise an exception Uninferable attributes
class MC:
    @property
    def nargs(self):
        return 1 if self._nargs else 2


class Application(metaclass=MC):
    def __no_special__(cls):
        nargs = obj._nargs  # [protected-access]
