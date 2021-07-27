# pylint: disable=missing-docstring, too-few-public-methods, invalid-name

class F:
    """0 parents"""

class E(F):
    """1 parent"""

class D:
    """0 parents"""

class B(D, E):
    """3 parents"""

class C:
    """0 parents"""

class A(B, C): # [too-many-ancestors]
    """5 parents"""
