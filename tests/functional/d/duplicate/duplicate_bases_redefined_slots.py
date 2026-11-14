"""redefined-slots-in-subclass survives a parent whose bases are duplicated.

Comparing a subclass' slots against its parents' reads the slots of every
ancestor, which used to walk an MRO the duplicate bases leave unusable. That
aborted the whole file with a fatal astroid-error instead of reporting
duplicate-bases.
"""
# pylint: disable=too-few-public-methods


class Basket(list, list):  # [duplicate-bases]
    """A basket that cannot be built, with a slot for its fruit."""

    __slots__ = ("fruit",)


class SmallBasket(Basket):  # [duplicate-bases]
    """Repeating the parent's slot is what sends the checker at the ancestors."""

    __slots__ = ("fruit",)
