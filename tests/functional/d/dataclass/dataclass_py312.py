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


# Regression test for https://github.com/pylint-dev/pylint/issues/10991:
# a kw_only field inherited through a base that forwards a TypeVarTuple.
@dataclasses.dataclass(frozen=True, kw_only=True)
class Base:
    value: str


@dataclasses.dataclass(frozen=True, kw_only=True)
class Middle[T, *Shape](Base):
    pass


@dataclasses.dataclass(frozen=True, kw_only=True)
class Upper[T, *Shape](Middle[T, *Shape]):
    pass


Upper[str, int](value="hello")
Upper(value="hello")
