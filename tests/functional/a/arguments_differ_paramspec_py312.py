"""Overriding a method that takes the parameters of a PEP 695 ParamSpec.

https://github.com/pylint-dev/pylint/issues/9424
"""
# pylint: disable=missing-docstring,too-few-public-methods
from typing import Any


class Base[**P]:
    def forward(self, ctx: str, *args: P.args, **kwargs: P.kwargs) -> Any:
        raise NotImplementedError()


class Derived(Base[[int, int]]):
    def forward(self, ctx: str, x: int, y: int) -> Any:
        del x, y
        return ctx
