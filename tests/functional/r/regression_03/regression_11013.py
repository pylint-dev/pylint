# Regression test for https://github.com/pylint-dev/pylint/issues/11013
# Type aliases annotated with `TypeAlias` inside a `TYPE_CHECKING` block were
# wrongly reported as constants that should use UPPER_CASE naming.
"""No `invalid-name` for type aliases nested in `TYPE_CHECKING`."""
# pylint: disable=too-few-public-methods
from typing import TYPE_CHECKING, TypeAlias, Union

if TYPE_CHECKING:
    AppleType: TypeAlias = "Apple"
    BananaType: TypeAlias = "Banana"
    AnyFruit = Union[AppleType, BananaType]


class Apple:
    """An apple."""


class Banana:
    """A banana."""
