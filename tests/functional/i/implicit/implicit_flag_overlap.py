"""Test check for classes extending an Enum class."""
from enum import IntFlag

class DisjointFlags(IntFlag):
    """Class with flags that do not overlap"""
    X = 1
    W = 2
    R = 4

class ExplicitUnionFlags(IntFlag):
    """Class with flags that overlap using explicit union syntax"""
    X = 1
    W = 2
    R = 4
    RO = 4
    RW = R | W

class SubclassUnionFlags(ExplicitUnionFlags):  # [invalid-enum-extension]
    """Class with flags that overlap a superclass"""
    RWX = 7

class ImplicitUnionFlags(IntFlag):
    """Class with flags that overlap implicitly"""
    A = 1
    B = 2
    C = 3  # [implicit-flag-overlap]
    D = 5  # [implicit-flag-overlap]
    E = 8

    def irrelevant(self):
        """Irrelevant method definition"""
        return
