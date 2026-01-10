# pylint: disable=missing-class-docstring
"""Dataclasses using PEP 695 syntax."""
import dataclasses


@dataclasses.dataclass
class B[X]:
    x: X


@dataclasses.dataclass
class C(B[int]):
    pass


C(x=0)
