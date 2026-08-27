"""stop-iteration-return survives a class whose bases are duplicated.

Deciding whether the raised class is a StopIteration used to walk an MRO the
duplicate bases leave unusable, which aborted the whole file with a fatal
astroid-error instead of reporting duplicate-bases.
"""
# pylint: disable=too-few-public-methods


class BasketEmpty(Exception, Exception):  # [duplicate-bases]
    """An error that cannot be built."""


def fruits():
    """Raising the class is what sends the checker looking at the MRO."""
    yield "banana"
    raise BasketEmpty()


class NoMoreFruit(StopIteration, StopIteration):  # [duplicate-bases]
    """A StopIteration subclass that cannot be built either."""


def more_fruits():
    """Losing the MRO does not lose the bases, so the message survives."""
    yield "banana"
    raise NoMoreFruit()  # [stop-iteration-return]
