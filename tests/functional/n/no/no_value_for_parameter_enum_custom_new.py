"""Regression test for https://github.com/pylint-dev/pylint/issues/1801.

An enum with a custom ``__new__`` taking several values is looked up by its
value alone: ``Planet(1)`` passes one argument, not the arguments of
``__new__``.
"""

from enum import Enum


class EnumWithDoc(Enum):
    """Each member carries a value and a doc string."""

    def __new__(cls, value, doc):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.doc = doc
        return obj


class Planet(EnumWithDoc):
    """Two members, built with a value and a doc each."""

    MERCURY = (1, "The first planet")
    VENUS = (2, "The second planet")


print(Planet(1).doc)
