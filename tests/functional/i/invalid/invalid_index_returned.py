"""Check invalid value returned by __index__ """

# pylint: disable=too-few-public-methods,missing-docstring,no-self-use,import-error, useless-object-inheritance
import six

from missing import Missing


class FirstGoodIndex(object):
    """__index__ returns <type 'int'>"""

    def __index__(self):
        return 1


class SecondGoodIndex(object):
    """__index__ returns <type 'int'>"""

    def __index__(self):
        return 0


class IndexMetaclass(type):
    def __index__(cls):
        return 1


@six.add_metaclass(IndexMetaclass)
class ThirdGoodIndex(object):
    """Index through the metaclass."""


class FirstBadIndex(object):
    """ __index__ returns a dict """

    def __index__(self):  # [invalid-index-returned]
        return {'1': '1'}


class SecondBadIndex(object):
    """ __index__ returns str """

    def __index__(self):  # [invalid-index-returned]
        return "42"


class ThirdBadIndex(object):
    """ __index__ returns a float"""

    def __index__(self):  # [invalid-index-returned]
        return 1.11


class FourthBadIndex(object):
    """ __index__ returns node which does not have 'value' in AST """

    def __index__(self):  # [invalid-index-returned]
        return lambda: 3


class AmbigousIndex(object):
    """ Uninferable return value """

    __index__ = lambda self: Missing


class AnotherAmbiguousIndex(object):
    """Potential uninferable return value"""

    def __index__(self):
        return int(Missing)
