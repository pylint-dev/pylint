"""Test to see we don't crash on this code in pandas.
See: https://github.com/pandas-dev/pandas/blob/main/pandas/core/arrays/sparse/array.py
Code written by Guido van Rossum here: https://github.com/python/typing/issues/684"""
# pylint: disable=no-member, redefined-builtin, invalid-name, missing-class-docstring

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enum import Enum

    class ellipsis(Enum):
        Ellipsis = "..."

    Ellipsis = ellipsis.Ellipsis


else:
    ellipsis = type(Ellipsis)
