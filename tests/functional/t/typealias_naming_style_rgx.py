"""Test cases for invalid-name for TypeAlias and related classes with non-default settings."""
from typing import TypeAlias, Union

# Valid
TypeAliasShouldBeLikeThis: TypeAlias = int
_TypeAliasShouldBeLikeThis = Union[str, int]

# Invalid
TypeAliasShouldntBeLikeThis: TypeAlias = int  # [invalid-name]
_TypeAliasShouldntBeLikeThis = Union[str, int]  # [invalid-name]
