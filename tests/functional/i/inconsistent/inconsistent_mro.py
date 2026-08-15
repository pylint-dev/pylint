"""Tests for inconsistent-mro."""
# pylint: disable=missing-docstring,too-few-public-methods

class Str(str):
    pass


class Inconsistent(str, Str): # [inconsistent-mro]
    pass


# The name checker asks whether this is an enum member, which used to walk an
# MRO the inconsistent bases leave unusable and abort the whole file.
INSTANCE = Inconsistent()
print(INSTANCE)
