"""Tests for lru-cache-decorating-method"""
# pylint: disable=no-self-use, missing-function-docstring, reimported, too-few-public-methods
# pylint: disable=missing-class-docstring, function-redefined

import functools
import functools as aliased_functools
from functools import lru_cache
from functools import lru_cache as aliased_cache


@lru_cache
def my_func(param):
    return param + 1


class MyClassWithMethods:
    @lru_cache
    @staticmethod
    def my_func(param):
        return param + 1

    @lru_cache
    @classmethod
    def my_func(cls, param):
        return param + 1

    @lru_cache  # [lru-cache-decorating-method]
    def my_func(self, param):
        return param + 1

    @functools.lru_cache  # [lru-cache-decorating-method]
    def my_func(self, param):
        return param + 1

    @aliased_functools.lru_cache  # [lru-cache-decorating-method]
    def my_func(self, param):
        return param + 1

    @aliased_cache  # [lru-cache-decorating-method]
    def my_func(self, param):
        return param + 1

    @lru_cache()  # [lru-cache-decorating-method]
    def my_func(self, param):
        return param + 1

    @functools.lru_cache()  # [lru-cache-decorating-method]
    def my_func(self, param):
        return param + 1

    @aliased_functools.lru_cache()  # [lru-cache-decorating-method]
    def my_func(self, param):
        return param + 1

    @aliased_cache()  # [lru-cache-decorating-method]
    def my_func(self, param):
        return param + 1

    # Check double decorating to check robustness of checker itself
    @aliased_cache()  # [lru-cache-decorating-method]
    @aliased_cache()  # [lru-cache-decorating-method]
    def my_func(self, param):
        return param + 1
