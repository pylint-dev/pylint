"""Overriding a method that takes the parameters of a ParamSpec.

https://github.com/pylint-dev/pylint/issues/9424
"""
# pylint: disable=missing-docstring,too-few-public-methods
from typing import Any, Generic, ParamSpec

P = ParamSpec("P")


class Base(Generic[P]):
    @classmethod
    def apply(cls, *args: P.args, **kwargs: P.kwargs) -> Any:
        return cls.forward("ctx", *args, **kwargs)

    @staticmethod
    def forward(ctx: str, *args: P.args, **kwargs: P.kwargs) -> Any:
        raise NotImplementedError()

    @staticmethod
    def backward(ctx: str, *args: P.args, **kwargs: P.kwargs) -> Any:
        raise NotImplementedError()


class Derived(Base[[int, int]]):
    @staticmethod
    def forward(ctx: str, x: int, y: int) -> Any:
        del x, y
        return ctx

    @staticmethod
    def backward(ctx: str, *, x: int, y: int) -> Any:
        del x, y
        return ctx


class RenamedFirstParameter(Base[[int]]):
    @staticmethod
    def forward(context: str, x: int) -> Any:  # [arguments-renamed]
        del x
        return context

    @staticmethod
    def backward() -> Any:  # [arguments-differ]
        return None
