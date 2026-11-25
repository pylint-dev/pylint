"""Tests for missing-function-docstring"""
# pylint: disable=unused-argument, missing-class-docstring, too-few-public-methods, unused-variable
import typing


def func(tion):  # [missing-function-docstring]
    pass


def func_two(tion):
    """Documented"""

    def inner(fun):
        # Not documented
        pass


class MyClass:
    def __init__(self, my_param: int) -> None:  # [missing-function-docstring]
        pass


# Regression test for https://github.com/pylint-dev/pylint/issues/7934
T = typing.TypeVar("T")
U = typing.TypeVar("U")


class Bases(typing.Generic[T]):
    def method(self):
        """Documented"""


class TwoParamBase(typing.Generic[T, U]):
    def method(self):
        """Documented"""


class Plain:
    pass


class ClassTypedDict(typing.TypedDict):
    a: int


FunctionalTypedDict = typing.TypedDict("FunctionalTypedDict", {"a": int})


class Child(Bases[FunctionalTypedDict]):
    def __init__(self):  # [missing-function-docstring]
        pass

    def method(self):
        pass


class ClassTypedDictChild(Bases[ClassTypedDict]):
    def method(self):
        pass


class PlainChild(Bases):
    def method(self):
        pass


class OtherChild(Bases[Plain()]):
    def method(self):
        pass

    def new_method(self):  # [missing-function-docstring]
        pass


class MultiBaseChild(Plain, Bases[Plain()]):
    def method(self):
        pass


class NestedSubscriptChild(TwoParamBase[T, int][Plain()]):
    def method(self):
        pass


class Subscriptable:
    def __getitem__(self, item):
        """Documented"""
        raise NotImplementedError


SUBSCRIPTABLE = Subscriptable()


class NonClassSubscriptChild(SUBSCRIPTABLE[Plain()]):
    def method(self):  # [missing-function-docstring]
        pass
