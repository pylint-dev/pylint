"""Check invalid value returned by __index__ """

# pylint: disable=too-few-public-methods,missing-docstring,import-error,unnecessary-lambda-assignment
import six

from missing import Missing


class FirstGoodIndex:
    """__index__ returns <type 'int'>"""

    def __index__(self):
        return 1


class SecondGoodIndex:
    """__index__ returns <type 'int'>"""

    def __index__(self):
        return 0


class IndexMetaclass(type):
    def __index__(cls):
        return 1


@six.add_metaclass(IndexMetaclass)
class ThirdGoodIndex:
    """Index through the metaclass."""


class FirstBadIndex:
    """ __index__ returns a dict """

    def __index__(self):  # [invalid-index-returned]
        return {'1': '1'}


class SecondBadIndex:
    """ __index__ returns str """

    def __index__(self):  # [invalid-index-returned]
        return "42"


class ThirdBadIndex:
    """ __index__ returns a float"""

    def __index__(self):  # [invalid-index-returned]
        return 1.11


class FourthBadIndex:
    """ __index__ returns node which does not have 'value' in AST """

    def __index__(self):  # [invalid-index-returned]
        return lambda: 3


class AmbigousIndex:
    """ Uninferable return value """

    __index__ = lambda self: Missing


class AnotherAmbiguousIndex:
    """Potential uninferable return value"""

    def __index__(self):
        return int(Missing)
