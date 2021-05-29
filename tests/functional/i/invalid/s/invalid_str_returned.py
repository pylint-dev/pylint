"""Check invalid value returned by __str__ """

# pylint: disable=too-few-public-methods,missing-docstring,no-self-use,import-error, useless-object-inheritance
import six

from missing import Missing


class FirstGoodStr(object):
    """__str__ returns <type 'str'>"""

    def __str__(self):
        return "some str"


class SecondGoodStr(object):
    """__str__ returns <type 'str'>"""

    def __str__(self):
        return str(123)


class StrMetaclass(type):
    def __str__(cls):
        return "some str"


@six.add_metaclass(StrMetaclass)
class ThirdGoodStr(object):
    """Str through the metaclass."""


class FirstBadStr(object):
    """ __str__ returns bytes """

    def __str__(self):  # [invalid-str-returned]
        return b"123"


class SecondBadStr(object):
    """ __str__ returns int """

    def __str__(self):  # [invalid-str-returned]
        return 1


class ThirdBadStr(object):
    """ __str__ returns node which does not have 'value' in AST """

    def __str__(self):  # [invalid-str-returned]
        return lambda: "some str"


class AmbiguousStr(object):
    """ Uninferable return value """

    __str__ = lambda self: Missing


class AnotherAmbiguousStr(object):
    """Potential uninferable return value"""

    def __str__(self):
        return str(Missing)
