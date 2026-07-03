"""Tests for missing-yield-doc and missing-yield-type-doc with accept-no-yields-doc = no"""
# pylint: disable=missing-function-docstring, unused-argument, function-redefined

from typing import Iterator


# Test missing docstring
def my_func(self):  # [missing-yield-doc, missing-yield-type-doc]
    yield False


# This function doesn't require a docstring, because its name starts
# with an '_' (no-docstring-rgx):
def _function(some_arg: int) -> Iterator[int]:
    yield some_arg
