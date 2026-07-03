"""Tests for method-cache-max-size-none"""
# pylint: disable=missing-function-docstring, reimported, too-few-public-methods
# pylint: disable=missing-class-docstring, function-redefined

import functools
import functools as aliased_functools
from functools import lru_cache
from functools import lru_cache as aliased_cache
from enum import Enum


@lru_cache
def my_func(param):
    return param + 1


class MyClassWithMethods:
    @lru_cache()
    def my_func(self, param):
        return param + 1

    @lru_cache(1)
    def my_func(self, param):
        return param + 1

    @lru_cache(None)  # [method-cache-max-size-none]
    def my_func(self, param):
        return param + 1

    @functools.lru_cache(None)  # [method-cache-max-size-none]
    def my_func(self, param):
        return param + 1

    @aliased_functools.lru_cache(None)  # [method-cache-max-size-none]
    def my_func(self, param):
        return param + 1

    @aliased_cache(None)  # [method-cache-max-size-none]
    def my_func(self, param):
        return param + 1

    # Check double decorating to check robustness of checker itself
    @aliased_cache(None)  # [method-cache-max-size-none]
    @aliased_cache(None)  # [method-cache-max-size-none]
    def my_func(self, param):
        return param + 1

    maxsizeKwarg = {"maxsize": None}
    @lru_cache(**maxsizeKwarg)  # [method-cache-max-size-none]
    def my_func(self, param):
        return param + 1


class MyClassWithMethodsAndMaxSize:
    @lru_cache(maxsize=1)
    def my_func(self, param):
        return param + 1

    @lru_cache(maxsize=1)
    def my_func(self, param):
        return param + 1

    @lru_cache(typed=True)
    def my_func(self, param):
        return param + 1

    @lru_cache(typed=True)
    def my_func(self, param):
        return param + 1

    @lru_cache(typed=True, maxsize=1)
    def my_func(self, param):
        return param + 1

    @lru_cache(typed=True, maxsize=1)
    def my_func(self, param):
        return param + 1

    @lru_cache(typed=True, maxsize=None)  # [method-cache-max-size-none]
    def my_func(self, param):
        return param + 1


@lru_cache(maxsize=None)
def my_func(param):
    return param + 1


class Class(Enum):
    A = 1

    @lru_cache(maxsize=None)
    def func(self) -> None:
        pass
