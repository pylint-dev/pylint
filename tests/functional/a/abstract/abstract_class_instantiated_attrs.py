"""Regression tests for attrs fields implementing abstract properties."""

# pylint: disable=import-error,missing-docstring,too-few-public-methods,reimported

from abc import ABC, abstractmethod

import attr
import attrs
import attrs as a


class Abstract(ABC):
    @property
    @abstractmethod
    def my_prop(self) -> int:
        ...


@attrs.define
class Concrete(Abstract):
    my_prop: int


@attrs.define
class ConcreteField(Abstract):
    my_prop: int = attrs.field()


@a.define
class ConcreteAliased(Abstract):
    my_prop: int = a.field()


@attr.s
class ConcreteClassic(Abstract):
    my_prop: int = attr.ib()


Concrete(35)
ConcreteField(99)
ConcreteClassic(42)
ConcreteAliased(77)
