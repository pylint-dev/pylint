"""Tests for broad exception handling."""

import contextlib
from contextlib import suppress

# pylint: disable=missing-docstring
__revision__ = 0

class CustomBroadException(Exception):
    pass


class CustomNarrowException(CustomBroadException):
    pass


try:
    __revision__ += 1
except Exception:  # [broad-exception-caught]
    print('error')


try:
    __revision__ += 1
except BaseException: # [broad-exception-caught]
    print('error')


try:
    __revision__ += 1
except ValueError:
    print('error')


try:
    __revision__ += 1
except CustomBroadException: # [broad-exception-caught]
    print('error')


try:
    __revision__ += 1
except CustomNarrowException:
    print('error')

def suppress_broad_exception(file):
    with contextlib.suppress(Exception):  # [broad-exception-caught]
        file.seek(0)

def suppress_narrow_exception(file):
    with contextlib.suppress(ValueError):
        file.seek(0)

def suppress_broad_exception_alias(file):
    with suppress(Exception):  # [broad-exception-caught]
        file.seek(0)
