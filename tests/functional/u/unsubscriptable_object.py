"""Tests for unscubscriptable-object"""

# pylint: disable=unused-variable, too-few-public-methods

import typing

from collections.abc import Mapping
from typing import Generic, TypeVar, TypedDict
from dataclasses import dataclass

# Test for typing.NamedTuple
# See: https://github.com/pylint-dev/pylint/issues/1295
MyType = typing.Tuple[str, str]


# https://github.com/pylint-dev/astroid/issues/2305
class Identity(TypedDict):
    """It's the identity."""

    name: str

T = TypeVar("T", bound=Mapping)

@dataclass
class Animal(Generic[T]):
    """It's an animal."""

    identity: T

class Dog(Animal[Identity]):
    """It's a Dog."""

DOG = Dog(identity=Identity(name="Dog"))
print(DOG.identity["name"])


# Regression test for https://github.com/pylint-dev/pylint/issues/9515
class Parents():  # pylint: disable=missing-class-docstring, missing-function-docstring
    name: str
    age: int
    children_name: typing.Optional[list[str]] = None

    def get_first_children_name(self) -> typing.Optional[str]:
        if self.children_name:
            return self.children_name[0]
        return None
