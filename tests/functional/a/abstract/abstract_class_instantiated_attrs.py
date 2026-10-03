"""Regression tests for attrs fields implementing abstract properties."""

# pylint: disable=import-error,missing-docstring,too-few-public-methods

from abc import ABC, abstractmethod

import attrs


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


Concrete(35)
ConcreteField(99)
