"""Check invalid value returned by __hash__ """

# pylint: disable=too-few-public-methods,missing-docstring,import-error,unnecessary-lambda-assignment
import six

from missing import Missing


class FirstGoodHash:
    """__hash__ returns <type 'int'>"""

    def __hash__(self):
        return 1


class SecondGoodHash:
    """__hash__ returns <type 'int'>"""

    def __hash__(self):
        return 0


class HashMetaclass(type):
    def __hash__(cls):
        return 1


@six.add_metaclass(HashMetaclass)
class ThirdGoodHash:
    """Hash through the metaclass."""


class FirstBadHash:
    """ __hash__ returns a dict """

    def __hash__(self):  # [invalid-hash-returned]
        return {}


class SecondBadHash:
    """ __hash__ returns str """

    def __hash__(self):  # [invalid-hash-returned]
        return "True"


class ThirdBadHash:
    """ __hash__ returns a float"""

    def __hash__(self):  # [invalid-hash-returned]
        return 1.11


class FourthBadHash:
    """ __hash__ returns node which does not have 'value' in AST """

    def __hash__(self):  # [invalid-hash-returned]
        return lambda: 3


class AmbigousHash:
    """ Uninferable return value """

    __hash__ = lambda self: Missing


class AnotherAmbiguousHash:
    """Potential uninferable return value"""

    def __hash__(self):
        return hash(Missing)
