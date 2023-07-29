"""Check invalid value returned by __str__ """

# pylint: disable=too-few-public-methods,missing-docstring,import-error,unnecessary-lambda-assignment
import six

from missing import Missing


class FirstGoodStr:
    """__str__ returns <type 'str'>"""

    def __str__(self):
        return "some str"


class SecondGoodStr:
    """__str__ returns <type 'str'>"""

    def __str__(self):
        return str(123)


class StrMetaclass(type):
    def __str__(cls):
        return "some str"


@six.add_metaclass(StrMetaclass)
class ThirdGoodStr:
    """Str through the metaclass."""


class FirstBadStr:
    """ __str__ returns bytes """

    def __str__(self):  # [invalid-str-returned]
        return b"123"


class SecondBadStr:
    """ __str__ returns int """

    def __str__(self):  # [invalid-str-returned]
        return 1


class ThirdBadStr:
    """ __str__ returns node which does not have 'value' in AST """

    def __str__(self):  # [invalid-str-returned]
        return lambda: "some str"


class AmbiguousStr:
    """ Uninferable return value """

    __str__ = lambda self: Missing


class AnotherAmbiguousStr:
    """Potential uninferable return value"""

    def __str__(self):
        return str(Missing)
