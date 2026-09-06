"""assigning-non-slot survives a class whose bases are duplicated.

Assigning ``__class__`` compares the slots of both classes, which used to walk
an MRO the duplicate bases leave unusable. That aborted the whole file with a
fatal astroid-error instead of reporting duplicate-bases.

A class without a usable MRO has unknowable slots, so it gets the answer any
other class with a different layout gets, exactly like a class that defines no
slot at all.
"""
# pylint: disable=too-few-public-methods


class Basket(list, list):  # [duplicate-bases]
    """A basket that cannot be built, with a slot for its fruit."""

    __slots__ = ("fruit",)


class Bowl:
    """A bowl that spells its slots the same way."""

    __slots__ = ("fruit",)

    def become_a_basket(self):
        """Assigning __class__ is what sends the checker comparing the slots."""
        self.__class__ = Basket  # [assigning-non-slot]
