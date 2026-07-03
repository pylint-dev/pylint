# pylint: disable=missing-docstring,invalid-name,too-few-public-methods

# https://github.com/pylint-dev/pylint/issues/2822
# Base should be subscriptable, even with ABCMeta as metaclass
from abc import ABC, ABCMeta
from typing import Generic, TypeVar

T = TypeVar("T")

class Base(Generic[T], metaclass=ABCMeta):
    """Base"""

class Impl(Base[str]):
    """Impl"""


# https://github.com/pylint-dev/astroid/issues/942
Anything = TypeVar("Anything")
MoreSpecific = TypeVar("MoreSpecific", str, int)

class A(ABC, Generic[Anything]):
    def a_method(self) -> None:
        print("hello")

class B(A[MoreSpecific]):
    pass

class C(B[str]):
    pass

c = C()
c.a_method()  # should NOT emit `no-member` error
