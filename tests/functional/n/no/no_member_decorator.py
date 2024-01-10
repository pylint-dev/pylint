"""Attributes supplied by a decorator."""

from functools import lru_cache


class SomeClass:  # pylint: disable=too-few-public-methods
    """https://github.com/pylint-dev/pylint/issues/9246"""
    @classmethod
    @lru_cache
    def __cached_fun(cls, arg: int) -> str:
        return str(arg)

    @classmethod
    def cache_clear(cls):
        """__cached_fun()'s @cache decorator supplies cache_clear()."""
        cls.__cached_fun.cache_clear()
