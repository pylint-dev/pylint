"""Check invalid value returned by __bool__ """

# pylint: disable=too-few-public-methods,missing-docstring,import-error,unnecessary-lambda-assignment
import six

from missing import Missing


class FirstGoodBool:
    """__bool__ returns <type 'bool'>"""

    def __bool__(self):
        return True


class SecondGoodBool:
    """__bool__ returns <type 'bool'>"""

    def __bool__(self):
        return bool(0)


class BoolMetaclass(type):
    def __bool__(cls):
        return True


@six.add_metaclass(BoolMetaclass)
class ThirdGoodBool:
    """Bool through the metaclass."""


class FirstBadBool:
    """ __bool__ returns an integer """

    def __bool__(self):  # [invalid-bool-returned]
        return 1


class SecondBadBool:
    """ __bool__ returns str """

    def __bool__(self):  # [invalid-bool-returned]
        return "True"


class ThirdBadBool:
    """ __bool__ returns node which does not have 'value' in AST """

    def __bool__(self):  # [invalid-bool-returned]
        return lambda: 3


class AmbigousBool:
    """ Uninferable return value """
    __bool__ = lambda self: Missing


class AnotherAmbiguousBool:
    """Potential uninferable return value"""
    def __bool__(self):
        return bool(Missing)
