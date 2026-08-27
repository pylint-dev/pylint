"""The __slots__ checks survive a class whose bases are duplicated.

They used to walk an MRO the duplicate bases leave unusable, which aborted the
whole file with a fatal astroid-error instead of reporting duplicate-bases.
"""
# pylint: disable=too-few-public-methods


class Basket(list, list):  # [duplicate-bases]
    """A basket that cannot be built, with a slot for its fruit."""

    __slots__ = ("fruit",)

    def __init__(self):
        """Assigning a slot is what sends the checker looking at the MRO."""
        super().__init__()
        self.fruit = "banana"
