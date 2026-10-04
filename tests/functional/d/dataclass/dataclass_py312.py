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


@dataclasses.dataclass
class One[T]:
    one: T


@dataclasses.dataclass
class Two[T](One[T]):
    two: T

one = One(1)
two = Two(1, 2)
