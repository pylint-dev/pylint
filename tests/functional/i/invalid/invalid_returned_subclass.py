"""Special methods may return an instance of a subclass of the expected builtin type."""

# pylint: disable=too-few-public-methods,missing-docstring,unnecessary-pass

from collections import namedtuple


class MyStr(str):
    """A str subclass; ``self`` is a valid str."""

    def __repr__(self):
        return self

    def __str__(self):
        return self

    def __format__(self, format_spec):
        return self


class MyInt(int):
    """An int subclass; ``self`` is a valid int."""

    def __hash__(self):
        return self

    def __index__(self):
        return self

    def __len__(self):
        return self

    def __length_hint__(self):
        return self


class MyBytes(bytes):
    def __bytes__(self):
        return self


class MyTuple(tuple):
    def __getnewargs__(self):
        return self


Args = namedtuple("Args", ["first", "second"])


class ReturnsSubclassInstances:
    """The subclass instance is returned from an unrelated class."""

    def __init__(self):
        self.text = MyStr("text")
        self.number = MyInt(1)

    def __repr__(self):
        return self.text

    def __str__(self):
        return self.text

    def __format__(self, format_spec):
        return MyStr(format_spec)

    def __bytes__(self):
        return MyBytes(b"bytes")

    def __hash__(self):
        return self.number

    def __index__(self):
        return self.number

    def __len__(self):
        return self.number

    def __length_hint__(self):
        return MyInt(2)

    def __getnewargs__(self):
        return Args(1, 2)

    def __getnewargs_ex__(self):
        return MyTuple((Args(1, 2), {}))


class NotStr:
    pass


class ReturnsUnrelatedSubclass:
    """Being a subclass of some other builtin is still an error."""

    def __repr__(self):  # [invalid-repr-returned]
        return MyInt(1)

    def __str__(self):  # [invalid-str-returned]
        return NotStr()

    def __index__(self):  # [invalid-index-returned]
        return MyStr("1")

    def __bytes__(self):  # [invalid-bytes-returned]
        return MyStr("1")
