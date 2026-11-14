"""Regression test for https://github.com/pylint-dev/pylint/issues/2855

A class attribute that starts as None and is replaced by a tuple in a
classmethod must not be reported as a non-sequence when unpacked.
"""

# pylint: disable=missing-docstring,too-few-public-methods

from typing import ClassVar


class Cache:
    pair: ClassVar[tuple[int, int] | None] = None

    @classmethod
    def cached_pair(cls) -> tuple[int, int]:
        if cls.pair is None:
            cls.pair = (1, 2)
        return cls.pair

    @classmethod
    def use(cls) -> None:
        first, second = cls.cached_pair()
        print(first, second)
