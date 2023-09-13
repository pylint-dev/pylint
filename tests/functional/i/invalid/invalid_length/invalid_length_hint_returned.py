"""Check invalid value returned by __length_hint__ """

# pylint: disable=too-few-public-methods,missing-docstring,import-error,unnecessary-lambda-assignment
import sys

import six

from missing import Missing


class FirstGoodLengthHint:
    """__length_hint__ returns <type 'int'>"""

    def __length_hint__(self):
        return 0


class SecondGoodLengthHint:
    """__length_hint__ returns <type 'long'>"""

    def __length_hint__(self):
        return sys.maxsize + 1


class LengthHintMetaclass(type):
    def __length_hint__(cls):
        return 1


@six.add_metaclass(LengthHintMetaclass)
class ThirdGoodLengthHint:
    """LengthHintgth through the metaclass."""


class FirstBadLengthHint:
    """ __length_hint__ returns a negative integer """

    def __length_hint__(self):  # [invalid-length-hint-returned]
        return -1


class SecondBadLengthHint:
    """ __length_hint__ returns non-int """

    def __length_hint__(self):  # [invalid-length-hint-returned]
        return 3.0


class ThirdBadLengthHint:
    """ __length_hint__ returns node which does not have 'value' in AST """

    def __length_hint__(self):  # [invalid-length-hint-returned]
        return lambda: 3


class AmbigousLengthHint:
    """ Uninferable return value """
    __length_hint__ = lambda self: Missing


class AnotherAmbiguousLengthHint:
    """Potential uninferable return value"""
    def __length_hint__(self):
        return int(Missing)
