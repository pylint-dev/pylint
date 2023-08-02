
""" Tests for invalid-name checker in the context of enums. """
# pylint: disable=too-few-public-methods


from enum import Enum


class JustARegularClass:
    """ No `invalid-name` by default for class attributes
    """
    apple = 42
    orange = 24


class EnumClass(Enum):
    """ Members of a subclass of `enum.Enum` are expected to be UPPERCASE.
    """
    apple = 42  # [invalid-name]
    orange = 24  # [invalid-name]
    PEAR = 1
