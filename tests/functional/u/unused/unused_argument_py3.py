# pylint: disable=missing-docstring

def func(first, *, second): # [unused-argument, unused-argument]
    pass


def only_raises(first, second=42): # [unused-argument]
    if first == 24:
        raise ValueError
