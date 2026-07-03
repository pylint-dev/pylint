"""Check invalid value returned by __getnewargs__ """

# pylint: disable=too-few-public-methods,missing-docstring,import-error,unnecessary-lambda-assignment,use-dict-literal
import six

from missing import Missing


class FirstGoodGetNewArgs:
    """__getnewargs__ returns <type 'tuple'>"""

    def __getnewargs__(self):
        return (1, "2", 3)


class SecondGoodGetNewArgs:
    """__getnewargs__ returns <type 'tuple'>"""

    def __getnewargs__(self):
        return tuple()


class GetNewArgsMetaclass(type):
    def __getnewargs__(cls):
        return (1, 2, 3)


@six.add_metaclass(GetNewArgsMetaclass)
class ThirdGoodGetNewArgs:
    """GetNewArgs through the metaclass."""


class FirstBadGetNewArgs:
    """ __getnewargs__ returns an integer """

    def __getnewargs__(self):  # [invalid-getnewargs-returned]
        return 1


class SecondBadGetNewArgs:
    """ __getnewargs__ returns str """

    def __getnewargs__(self):  # [invalid-getnewargs-returned]
        return "(1, 2, 3)"


class ThirdBadGetNewArgs:
    """ __getnewargs__ returns node which does not have 'value' in AST """

    def __getnewargs__(self):  # [invalid-getnewargs-returned]
        return lambda: tuple(1, 2)


class AmbigousGetNewArgs:
    """ Uninferable return value """
    __getnewargs__ = lambda self: Missing


class AnotherAmbiguousGetNewArgs:
    """Potential uninferable return value"""
    def __getnewargs__(self):
        return tuple(Missing)
