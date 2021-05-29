"""Check invalid value returned by __getnewargs_ex__ """

# pylint: disable=too-few-public-methods,missing-docstring,no-self-use,import-error, useless-object-inheritance
import six

from missing import Missing


class FirstGoodGetNewArgsEx(object):
    """__getnewargs_ex__ returns <type 'tuple'>"""

    def __getnewargs_ex__(self):
        return ((1,), {"2": "2"})


class SecondGoodGetNewArgsEx(object):
    """__getnewargs_ex__ returns <type 'tuple'>"""

    def __getnewargs_ex__(self):
        return (tuple(), dict())


class GetNewArgsExMetaclass(type):
    def __getnewargs_ex__(cls):
        return ((1,), {"2": "2"})


@six.add_metaclass(GetNewArgsExMetaclass)
class ThirdGoodGetNewArgsEx(object):
    """GetNewArgsEx through the metaclass."""


class FirstBadGetNewArgsEx(object):
    """ __getnewargs_ex__ returns an integer """

    def __getnewargs_ex__(self):  # [invalid-getnewargs-ex-returned]
        return 1


class SecondBadGetNewArgsEx(object):
    """ __getnewargs_ex__ returns tuple with incorrect arg length"""

    def __getnewargs_ex__(self):  # [invalid-getnewargs-ex-returned]
        return (tuple(1), dict(x="y"), 1)


class ThirdBadGetNewArgsEx(object):
    """ __getnewargs_ex__ returns tuple with wrong type for first arg """

    def __getnewargs_ex__(self):  # [invalid-getnewargs-ex-returned]
        return (dict(x="y"), dict(x="y"))


class FourthBadGetNewArgsEx(object):
    """ __getnewargs_ex__ returns tuple with wrong type for second arg """

    def __getnewargs_ex__(self):  # [invalid-getnewargs-ex-returned]
        return ((1, ), (1, ))


class FifthBadGetNewArgsEx(object):
    """ __getnewargs_ex__ returns tuple with wrong type for both args """

    def __getnewargs_ex__(self):  # [invalid-getnewargs-ex-returned]
        return ({'x': 'y'}, (2,))


class SixthBadGetNewArgsEx(object):
    """ __getnewargs_ex__ returns node which does not have 'value' in AST """

    def __getnewargs_ex__(self):  # [invalid-getnewargs-ex-returned]
        return lambda: (1, 2)


class AmbigousGetNewArgsEx(object):
    """ Uninferable return value """

    __getnewargs_ex__ = lambda self: Missing


class AnotherAmbiguousGetNewArgsEx(object):
    """Potential uninferable return value"""

    def __getnewargs_ex__(self):
        return tuple(Missing)
