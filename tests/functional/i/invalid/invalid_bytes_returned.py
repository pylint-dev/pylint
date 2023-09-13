"""Check invalid value returned by __bytes__ """

# pylint: disable=too-few-public-methods,missing-docstring,import-error,unnecessary-lambda-assignment
import six

from missing import Missing


class FirstGoodBytes:
    """__bytes__ returns <type 'bytes'>"""

    def __bytes__(self):
        return b"some bytes"


class SecondGoodBytes:
    """__bytes__ returns <type 'bytes'>"""

    def __bytes__(self):
        return bytes("123", "ascii")


class BytesMetaclass(type):
    def __bytes__(cls):
        return b"some bytes"


@six.add_metaclass(BytesMetaclass)
class ThirdGoodBytes:
    """Bytes through the metaclass."""


class FirstBadBytes:
    """ __bytes__ returns bytes """

    def __bytes__(self):  # [invalid-bytes-returned]
        return "123"


class SecondBadBytes:
    """ __bytes__ returns int """

    def __bytes__(self):  # [invalid-bytes-returned]
        return 1


class ThirdBadBytes:
    """ __bytes__ returns node which does not have 'value' in AST """

    def __bytes__(self):  # [invalid-bytes-returned]
        return lambda: b"some bytes"


class AmbiguousBytes:
    """ Uninferable return value """

    __bytes__ = lambda self: Missing


class AnotherAmbiguousBytes:
    """Potential uninferable return value"""

    def __bytes__(self):
        return bytes(Missing)
