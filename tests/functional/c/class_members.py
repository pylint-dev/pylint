# pylint: disable=missing-docstring, too-few-public-methods


class Class:
    attr: int


# `bar` definitely does not exist here, but in a complex scenario,
# it might. We simply exclude PEP 526 class and instance variables
# from `no-member`.
print(Class().attr)
print(Class.attr)
