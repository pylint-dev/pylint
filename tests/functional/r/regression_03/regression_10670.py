# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/10670

Subclass of datetime.datetime with custom __new__ should not trigger
E1121 too-many-function-args.

Fix landed before pylint 2.13 (oldest Python-3.12-compatible version).
"""

# pylint: disable=missing-docstring,too-many-positional-arguments,signature-differs,too-many-arguments
import datetime
from typing import Self


class MyDateTime(datetime.datetime):
    def __new__(
        cls,
        firstArg: object,
        month: int | None = None,
        day: int | None = None,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
    ) -> Self:
        return super().__new__(
            cls, firstArg, month, day, hour, minute, second, microsecond
        )
