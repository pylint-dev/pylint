# pylint: disable=missing-module-docstring, invalid-name, missing-class-docstring, unused-variable


from dataclasses import dataclass
from typing import Generic, TypeVar


T_Inner = TypeVar("T_Inner", bound="Inner")


@dataclass
class Inner:
    inner_attribute: str


@dataclass
class Outer(Generic[T_Inner]):
    inner: T_Inner


x = Outer(inner=Inner(inner_attribute="magic xylophone"))

# Test `no-member` is not emitted here.
# https://github.com/pylint-dev/pylint/issues/9069
print(x.inner.inner_attribute)
