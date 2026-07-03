"""Regression test for alternative Union syntax in runtime contexts.
Syntax support was added in Python 3.10.

The code snipped should not raise any errors.
https://github.com/pylint-dev/pylint/issues/8119
"""
# pylint: disable=missing-docstring,too-few-public-methods
from typing import Generic, TypeVar

T = TypeVar("T")


class Coordinator(Generic[T]):
    def __init__(self, update_interval=None) -> None:
        self.update_interval = update_interval


class Child(Coordinator[int | str]):
    def __init__(self) -> None:
        Coordinator.__init__(self, update_interval=2)

    def _async_update_data(self):
        assert self.update_interval
        self.update_interval = 1
