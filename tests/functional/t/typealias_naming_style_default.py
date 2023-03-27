"""Test cases for invalid-name for TypeAlias and related classes with default settings."""
from typing import TypeAlias, Union

# PascalCase names
GoodName: TypeAlias = int
_GoodName: TypeAlias = int
__GoodName: TypeAlias = int
AnotherGoodName = Union[int, str]
GOODName: TypeAlias = int
GOODNAMEType: TypeAlias = int
TodoType: TypeAlias = int
Good2Name: TypeAlias = int
GoodName2: TypeAlias = int

# Non-PascalCase names
BadNAME: TypeAlias = int  # [invalid-name]
badName: TypeAlias = int  # [invalid-name]
AlsoBADName: TypeAlias = int  # [invalid-name]
TBadName: TypeAlias = int  # [invalid-name]
TypeTodo: TypeAlias = int  # [invalid-name]
BadNameT: TypeAlias = int  # [invalid-name]
BAD_NAME = Union[int, str]  # [invalid-name]
_BAD_NAME = Union[int, str]  # [invalid-name]
__BAD_NAME = Union[int, str]  # [invalid-name]
_1BadName = Union[int, str]  # [invalid-name]
ANOTHERBADNAME = Union[int, str]  # [invalid-name]

# Regression tests
# This is not a TypeAlias, and thus shouldn't flag the message
x: Union[str, int] = 42
