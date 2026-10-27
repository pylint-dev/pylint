"""Regression test for imported constants used as IntEnum members."""

# pylint: disable=import-outside-toplevel,missing-class-docstring
from enum import IntEnum


class LogLevel(IntEnum):
    from os import O_RDONLY as READ_ONLY


print(LogLevel.READ_ONLY.value)  # [no-member]
