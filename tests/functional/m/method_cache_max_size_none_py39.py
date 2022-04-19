"""Tests for method-cache-max-size-none"""
# pylint: disable=no-self-use, missing-function-docstring, reimported, too-few-public-methods
# pylint: disable=missing-class-docstring, function-redefined

import functools
import functools as aliased_functools
from functools import cache
from functools import cache as aliased_cache


@cache
def my_func(param):
    return param + 1


class MyClassWithMethods:
    @cache
    @staticmethod
    def my_func(param):
        return param + 1

    @cache
    @classmethod
    def my_func(cls, param):
        return param + 1

    @cache  # [method-cache-max-size-none]
    def my_func(self, param):
        return param + 1

    @functools.cache  # [method-cache-max-size-none]
    def my_func(self, param):
        return param + 1

    @aliased_functools.cache  # [method-cache-max-size-none]
    def my_func(self, param):
        return param + 1

    @aliased_cache  # [method-cache-max-size-none]
    def my_func(self, param):
        return param + 1

    # Check double decorating to check robustness of checker itself
    @functools.lru_cache(maxsize=1)
    @aliased_cache  # [method-cache-max-size-none]
    def my_func(self, param):
        return param + 1
