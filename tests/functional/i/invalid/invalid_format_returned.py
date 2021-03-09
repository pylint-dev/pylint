"""Check invalid value returned by __format__ """

# pylint: disable=too-few-public-methods,missing-docstring,no-self-use,import-error, useless-object-inheritance
import six

from missing import Missing


class FirstGoodFormat(object):
    """__format__ returns <type 'str'>"""

    def __format__(self, format_spec):
        return "some format"


class SecondGoodFormat(object):
    """__format__ returns <type 'str'>"""

    def __format__(self, format_spec):
        return str(123)


class FormatMetaclass(type):
    def __format__(cls, format_spec):
        return "some format"


@six.add_metaclass(FormatMetaclass)
class ThirdGoodFormat(object):
    """Format through the metaclass."""


class FirstBadFormat(object):
    """ __format__ returns bytes """

    def __format__(self, format_spec):  # [invalid-format-returned]
        return b"123"


class SecondBadFormat(object):
    """ __format__ returns int """

    def __format__(self, format_spec):  # [invalid-format-returned]
        return 1


class ThirdBadFormat(object):
    """ __format__ returns node which does not have 'value' in AST """

    def __format__(self, format_spec):  # [invalid-format-returned]
        return lambda: "some format"


class AmbiguousFormat(object):
    """ Uninferable return value """

    __format__ = lambda self, format_spec: Missing


class AnotherAmbiguousFormat(object):
    """Potential uninferable return value"""

    def __format__(self, format_spec):
        return str(Missing)
