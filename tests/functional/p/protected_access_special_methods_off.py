"""Test that when check-protected-access-in-special-methods is False (default)
no protected-access message emission for single underscore prefixed names
inside special methods occur
"""
# pylint: disable=missing-class-docstring, invalid-name, unused-variable
# pylint: disable=too-few-public-methods


class Protected:  # [eq-without-hash]
    """A class"""

    def __init__(self):
        self._protected = 42
        self.public = "A"
        self.__private = None  # [unused-private-member]

    def __eq__(self, other):
        self._protected = other._protected

    def _fake_special_(self, other):
        a = other.public
        self.public = other._protected  # [protected-access]
        self.__private = other.__private  # [protected-access, unused-private-member]
