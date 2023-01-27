"""Test check for classes extending an Enum class."""
from enum import IntFlag, auto

class DisjointFlags(IntFlag):
    """Class with flags that do not overlap"""
    X = 1
    W = 2
    R = 4
    S = auto()

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
    DUPLICATE = 1
    B = 2
    C = 3  # [implicit-flag-alias]
    D = 5  # [implicit-flag-alias]
    E = 8
    F = 17  # [implicit-flag-alias]
    G = 17  # [implicit-flag-alias]
    TRIPLICATE = 1

    def irrelevant(self):
        """Irrelevant method definition"""
        return

class ReverseOrderFlags(IntFlag):
    """Class with flags that overlap and are declared in descending order"""
    A = 5  # [implicit-flag-alias]
    B = 1

class SharedBitsWithoutDeclaration(IntFlag):
    """Class with flags that share a bit, but no value is defined using that bit"""
    A = 3
    B = 5  # [implicit-flag-alias]
