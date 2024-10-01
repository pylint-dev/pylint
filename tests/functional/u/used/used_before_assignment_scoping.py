# pylint: disable=missing-function-docstring, missing-module-docstring

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


def func_two():
    second = datetime.now()  # [used-before-assignment]
    return second


def func():
    first: datetime
    first = datetime.now()  # [used-before-assignment]
    second = datetime.now()
    return first, second
