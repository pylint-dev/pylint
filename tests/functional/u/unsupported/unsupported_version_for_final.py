"""Tests for the use of typing.final whenever the py-version is set < 3.8"""
# pylint: disable=missing-class-docstring, too-few-public-methods, missing-function-docstring, no-name-in-module

from typing import final


@final # [using-final-in-unsupported-version]
class Base:
    @final # [using-final-in-unsupported-version]
    def my_method(self):
        pass


class Subclass(Base): # [subclassed-final-class]
    def my_method(self): # [overridden-final-method]
        pass
