# pylint: disable=pointless-statement,missing-docstring
from enum import Enum
class Foo(Enum):
    BAR = 1
Foo.__members__['BAR']  # <-- error: Value 'Foo.__members__' is unsubscriptable
