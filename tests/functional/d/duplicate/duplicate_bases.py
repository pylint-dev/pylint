"""Test duplicate bases error."""
# pylint: disable=missing-docstring,too-few-public-methods,attribute-defined-outside-init


class Duplicates(str, str):  # [duplicate-bases]
    pass


class Alpha(str):
    pass


class NotDuplicates(Alpha, str):
    """The error should not be emitted for this case, since the
    other same base comes from the ancestors."""


print(Duplicates.__mro__)


INSTANCE = Duplicates()


class SlottedDuplicates(str, str):  # [duplicate-bases]
    __slots__ = ("attr",)


SLOTTED = SlottedDuplicates()
SLOTTED.attr = 1


class DuplicateErrors(TypeError, TypeError):  # [duplicate-bases]
    pass


def generator():
    yield 1
    raise DuplicateErrors()
