"""Regression test for https://github.com/pylint-dev/pylint/issues/10972.

An abstract method implemented by a PEP 695 generic base that takes a
TypeVarTuple must count as implemented.
"""

# pylint: disable=too-few-public-methods, missing-docstring, abstract-method

from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def get_item(self) -> None: ...


class Middle[*Shape]:
    def get_item(self) -> None:
        raise NotImplementedError


class Concrete[*Shape](Middle[*Shape], Base):
    pass


class MixedMiddle[T, *Shape]:
    def get_item(self) -> None:
        raise NotImplementedError


class MixedConcrete[T, *Shape](MixedMiddle[T, *Shape], Base):
    pass


class StillAbstract[*Shape](Base):
    pass


Concrete()
MixedConcrete()
StillAbstract()  # [abstract-class-instantiated]
