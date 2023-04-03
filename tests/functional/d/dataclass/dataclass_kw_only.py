"""Test the behaviour of the kw_only keyword."""

# pylint: disable=invalid-name

from dataclasses import dataclass


@dataclass(kw_only=True)
class FooBar:
    """Simple dataclass with a kw_only parameter."""

    a: int
    b: str


@dataclass(kw_only=False)
class BarFoo(FooBar):
    """Simple dataclass with a negated kw_only parameter."""

    c: int


BarFoo(1, a=2, b="")
BarFoo(  # [missing-kwoa,missing-kwoa,redundant-keyword-arg,too-many-function-args]
    1, 2, c=2
)
