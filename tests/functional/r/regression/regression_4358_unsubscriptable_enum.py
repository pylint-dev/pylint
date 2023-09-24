# pylint: disable=pointless-statement,missing-docstring
# https://github.com/pylint-dev/pylint/issues/4358

from enum import Enum

class Foo(Enum):
    BAR = 1

Foo.__members__['BAR']  # <-- error: Value 'Foo.__members__' is unsubscriptable
