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
# They are not TypeAlias, and thus shouldn't flag the message
x: Union[str, int] = 42
y: Union[str, int]
# But the following, using a good TypeAlias name, is:
GoodTypeAliasToUnion: TypeAlias = Union[str, int]


def my_function():
    """My doc."""
    LocalGoodName: TypeAlias = int
    local_bad_name: TypeAlias = int  # [invalid-name]
    local_declaration: Union[str, int]
    LocalTypeAliasToUnion: TypeAlias = Union[str, int]
    local_declaration = 1
    del local_declaration
    del LocalGoodName, local_bad_name, LocalTypeAliasToUnion
