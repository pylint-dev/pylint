"""Check invalid value returned by __repr__ """

# pylint: disable=too-few-public-methods,missing-docstring,no-self-use,import-error, useless-object-inheritance
import six

from missing import Missing


class FirstGoodRepr(object):
    """__repr__ returns <type 'str'>"""

    def __repr__(self):
        return "some repr"


class SecondGoodRepr(object):
    """__repr__ returns <type 'str'>"""

    def __repr__(self):
        return str(123)


class ReprMetaclass(type):
    def __repr__(cls):
        return "some repr"


@six.add_metaclass(ReprMetaclass)
class ThirdGoodRepr(object):
    """Repr through the metaclass."""


class FirstBadRepr(object):
    """ __repr__ returns bytes """

    def __repr__(self):  # [invalid-repr-returned]
        return b"123"


class SecondBadRepr(object):
    """ __repr__ returns int """

    def __repr__(self):  # [invalid-repr-returned]
        return 1


class ThirdBadRepr(object):
    """ __repr__ returns node which does not have 'value' in AST """

    def __repr__(self):  # [invalid-repr-returned]
        return lambda: "some repr"


class AmbiguousRepr(object):
    """ Uninferable return value """

    __repr__ = lambda self: Missing


class AnotherAmbiguousRepr(object):
    """Potential uninferable return value"""

    def __repr__(self):
        return str(Missing)
