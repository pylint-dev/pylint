"""Test that check-protected-access-in-special-methods can be used to
trigger protected-access message emission for single underscore prefixed names
inside special methods.
"""
# pylint: disable=missing-class-docstring, invalid-name, unused-variable
# pylint: disable=too-few-public-methods


class Protected:
    """A class"""

    def __init__(self):
        self._protected = 42
        self.public = "A"
        self.__private = None  # [unused-private-member]

    def __eq__(self, other):
        self._protected = other._protected  # [protected-access]

    def _fake_special_(self, other):
        a = other.public
        self.public = other._protected  # [protected-access]
        self.__private = other.__private  # [protected-access, unused-private-member]
