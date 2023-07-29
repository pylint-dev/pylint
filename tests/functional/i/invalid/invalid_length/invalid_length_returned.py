"""Check invalid value returned by __len__ """

# pylint: disable=too-few-public-methods,missing-docstring,import-error,unnecessary-lambda-assignment
import sys

import six

from missing import Missing


class FirstGoodLen:
    """__len__ returns <type 'int'>"""

    def __len__(self):
        return 0


class SecondGoodLen:
    """__len__ returns <type 'long'>"""

    def __len__(self):
        return sys.maxsize + 1


class LenMetaclass(type):
    def __len__(cls):
        return 1


@six.add_metaclass(LenMetaclass)
class ThirdGoodLen:
    """Length through the metaclass."""


class FirstBadLen:
    """ __len__ returns a negative integer """

    def __len__(self):  # [invalid-length-returned]
        return -1


class SecondBadLen:
    """ __len__ returns non-int """

    def __len__(self):  # [invalid-length-returned]
        return 3.0


class ThirdBadLen:
    """ __len__ returns node which does not have 'value' in AST """

    def __len__(self):  # [invalid-length-returned]
        return lambda: 3


class NonRegression:
    """ __len__ returns nothing """

    def __len__(self):  # [invalid-length-returned]
        print(3.0)


class AmbigousLen:
    """ Uninferable return value """
    __len__ = lambda self: Missing


class AnotherAmbiguousLen:
    """Potential uninferable return value"""
    def __len__(self):
        return int(Missing)
