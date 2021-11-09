"""Tests for the use of typing.final whenever the py-version is set < 3.8"""
# pylint: disable=missing-class-docstring, no-member, too-few-public-methods, missing-function-docstring, no-name-in-module, reimported

import typing
import typing as mytyping
from typing import final
from typing import final as myfinal


@final  # [using-final-decorator-in-unsupported-version]
class MyClass1:
    @final  # [using-final-decorator-in-unsupported-version]
    @final  # [using-final-decorator-in-unsupported-version]
    def my_method(self):
        pass


@myfinal  # [using-final-decorator-in-unsupported-version]
class MyClass2:
    @myfinal  # [using-final-decorator-in-unsupported-version]
    def my_method(self):
        pass


@typing.final  # [using-final-decorator-in-unsupported-version]
class MyClass3:
    @typing.final  # [using-final-decorator-in-unsupported-version]
    def my_method(self):
        pass


@mytyping.final  # [using-final-decorator-in-unsupported-version]
class MyClass4:
    @mytyping.final  # [using-final-decorator-in-unsupported-version]
    def my_method(self):
        pass
