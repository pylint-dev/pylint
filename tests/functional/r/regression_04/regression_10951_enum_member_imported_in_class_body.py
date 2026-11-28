"""Regression test for https://github.com/pylint-dev/pylint/issues/10951

A name imported in an enum class body is a member of the enum, so
``Seek.START.value`` is fine. Fixed in astroid by pylint-dev/astroid#3466.
"""

# pylint: disable=missing-docstring,import-outside-toplevel

from enum import IntEnum


class Seek(IntEnum):
    from io import SEEK_CUR as CURRENT, SEEK_SET as START


print(Seek.START.value, Seek.CURRENT.name)
print(Seek.START in Seek.__members__.values())
