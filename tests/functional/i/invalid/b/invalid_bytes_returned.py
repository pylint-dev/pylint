"""Check invalid value returned by __bytes__ """

# pylint: disable=too-few-public-methods,missing-docstring,no-self-use,import-error, useless-object-inheritance
import six

from missing import Missing


class FirstGoodBytes(object):
    """__bytes__ returns <type 'bytes'>"""

    def __bytes__(self):
        return b"some bytes"


class SecondGoodBytes(object):
    """__bytes__ returns <type 'bytes'>"""

    def __bytes__(self):
        return bytes("123", "ascii")


class BytesMetaclass(type):
    def __bytes__(cls):
        return b"some bytes"


@six.add_metaclass(BytesMetaclass)
class ThirdGoodBytes(object):
    """Bytes through the metaclass."""


class FirstBadBytes(object):
    """ __bytes__ returns bytes """

    def __bytes__(self):  # [invalid-bytes-returned]
        return "123"


class SecondBadBytes(object):
    """ __bytes__ returns int """

    def __bytes__(self):  # [invalid-bytes-returned]
        return 1


class ThirdBadBytes(object):
    """ __bytes__ returns node which does not have 'value' in AST """

    def __bytes__(self):  # [invalid-bytes-returned]
        return lambda: b"some bytes"


class AmbiguousBytes(object):
    """ Uninferable return value """

    __bytes__ = lambda self: Missing


class AnotherAmbiguousBytes(object):
    """Potential uninferable return value"""

    def __bytes__(self):
        return bytes(Missing)
