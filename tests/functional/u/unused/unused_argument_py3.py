# pylint: disable=missing-docstring

def func(first, *, second): # [unused-argument, unused-argument]
    pass


def only_raises(first, second=42): # [unused-argument]
    if first == 24:
        raise ValueError


def increment_factory(initial):

    def increment():
        nonlocal initial
        initial += 1

    return increment
