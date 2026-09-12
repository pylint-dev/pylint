# pylint: disable=missing-docstring,too-few-public-methods,invalid-name,unused-argument
# pylint: disable=line-too-long,bad-staticmethod-argument,abstract-method
"""Functional tests for the type annotation checker."""
from abc import abstractmethod
from typing import overload

from typing_extensions import override


def missing_return_type(x: int, y: int):  # [missing-return-type-annotation]
    return x + y


def missing_param_types(x, y) -> int:  # [missing-param-type-annotation,missing-param-type-annotation]
    return x + y


def missing_all(x, y):  # [missing-return-type-annotation,missing-param-type-annotation,missing-param-type-annotation]
    return x + y


def fully_annotated(x: int, y: int) -> int:
    return x + y


def variadic(*args, **kwargs):  # [missing-return-type-annotation,missing-param-type-annotation,missing-param-type-annotation]
    return args, kwargs


def variadic_annotated(*args: int, **kwargs: str) -> None:
    return None


def keyword_only(*, x, y: int) -> None:  # [missing-param-type-annotation]
    return None


def positional_only(x, y, /) -> None:  # [missing-param-type-annotation,missing-param-type-annotation]
    return None


async def async_missing_return(x: int):  # [missing-return-type-annotation]
    return x * 2


async def async_fully_annotated(x: int) -> int:
    return x * 2


class Example:
    def __init__(self, value):  # [missing-param-type-annotation]
        self.value = value

    def get_value(self):  # [missing-return-type-annotation]
        return self.value

    def set_value(self, value):  # [missing-return-type-annotation,missing-param-type-annotation]
        self.value = value

    def compute(self, x: int) -> int:
        return self.value + x

    @classmethod
    def from_value(cls, value):  # [missing-return-type-annotation,missing-param-type-annotation]
        return cls(value)

    @staticmethod
    def static_with_self(self, x):  # [missing-return-type-annotation,missing-param-type-annotation,missing-param-type-annotation]
        return self, x

    @property
    def prop(self):
        return self.value

    @prop.setter
    def prop(self, value):
        self.value = value

    @abstractmethod
    def abstract_method(self, x):
        ...

    @overload
    def overloaded(self, x: int) -> int: ...
    @overload
    def overloaded(self, x: str) -> str: ...
    def overloaded(self, x):  # [missing-return-type-annotation,missing-param-type-annotation]
        return x


class Child(Example):
    @override
    def get_value(self):
        return self.value
