"""Regression test for https://github.com/pylint-dev/pylint/issues/9250

A class attribute that starts as None and is set to a list through
``cls = self.__class__`` is subscriptable.
"""

# pylint: disable=missing-docstring,too-few-public-methods


class CachedRows:
    cached_name = None
    cached_rows = None

    def __init__(self, name):
        cls = self.__class__
        assert name is not None
        if cls.cached_name != name:
            cls.cached_rows = [0.0] * 10
            cls.cached_name = name
        self.first = cls.cached_rows[0]
