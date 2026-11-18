"""Regression test for https://github.com/pylint-dev/pylint/issues/7379.

A generic class that overrides ``__class_getitem__`` with a ``super()`` call
still gives its members to the classes that subclass ``Base[int]``.
"""

# pylint: disable=too-few-public-methods

from typing import Generic, TypeVar

T = TypeVar("T")


class Base(Generic[T]):
    """Overrides ``__class_getitem__`` and calls the parent's."""

    name = "base"

    def __class_getitem__(cls, item):
        return super().__class_getitem__(item)


class Child(Base[int]):
    """Inherits ``name``."""

    def get_name(self):
        """Read the inherited attribute."""
        return self.name


class GenericChild(Base[T]):
    """Inherits ``name`` and stays generic."""

    def get_name(self):
        """Read the inherited attribute."""
        return self.name


print(Child.name, Child().get_name(), GenericChild.name, GenericChild().get_name())
