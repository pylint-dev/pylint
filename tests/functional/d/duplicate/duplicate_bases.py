"""Test duplicate bases error."""
# pylint: disable=missing-docstring,too-few-public-methods


class Duplicates(str, str):  # [duplicate-bases]
    pass


class Alpha(str):
    pass


class NotDuplicates(Alpha, str):
    """The error should not be emitted for this case, since the
    other same base comes from the ancestors."""


print(Duplicates.__mro__)


# The name checker asks whether this is an enum member, which used to walk an
# MRO the duplicate bases leave unusable and abort the whole file.
INSTANCE = Duplicates()
print(INSTANCE)
