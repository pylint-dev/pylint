"""Regression test for a false positive abstract-class-instantiated
when a subclass uses PEP 695 generic syntax with a TypeVarTuple.
"""
# pylint: disable=missing-docstring, too-few-public-methods

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Base(Generic[T], ABC):
    @abstractmethod
    def get_item(self) -> T: ...


class Middle[NpDtype, *Shape]:
    """Implements the abstract method from Base."""

    def get_item(self) -> NpDtype:
        raise NotImplementedError


class Concrete[NpDtype, *Shape](Middle[NpDtype, *Shape], Base[NpDtype]):
    """All abstract methods are satisfied via Middle."""


Concrete()
