"""Check invalid value returned by __getnewargs__ """

# pylint: disable=too-few-public-methods,missing-docstring,no-self-use,import-error, useless-object-inheritance
import six

from missing import Missing


class FirstGoodGetNewArgs(object):
    """__getnewargs__ returns <type 'tuple'>"""

    def __getnewargs__(self):
        return (1, "2", 3)


class SecondGoodGetNewArgs(object):
    """__getnewargs__ returns <type 'tuple'>"""

    def __getnewargs__(self):
        return tuple()


class GetNewArgsMetaclass(type):
    def __getnewargs__(cls):
        return (1, 2, 3)


@six.add_metaclass(GetNewArgsMetaclass)
class ThirdGoodGetNewArgs(object):
    """GetNewArgs through the metaclass."""


class FirstBadGetNewArgs(object):
    """ __getnewargs__ returns an integer """

    def __getnewargs__(self):  # [invalid-getnewargs-returned]
        return 1


class SecondBadGetNewArgs(object):
    """ __getnewargs__ returns str """

    def __getnewargs__(self):  # [invalid-getnewargs-returned]
        return "(1, 2, 3)"


class ThirdBadGetNewArgs(object):
    """ __getnewargs__ returns node which does not have 'value' in AST """

    def __getnewargs__(self):  # [invalid-getnewargs-returned]
        return lambda: tuple(1, 2)


class AmbigousGetNewArgs(object):
    """ Uninferable return value """
    __getnewargs__ = lambda self: Missing


class AnotherAmbiguousGetNewArgs(object):
    """Potential uninferable return value"""
    def __getnewargs__(self):
        return tuple(Missing)
