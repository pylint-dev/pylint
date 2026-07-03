# pylint: disable=missing-docstring,too-few-public-methods
"""Test typing.Final"""
import typing
from typing import Final

class Foo:
    """Class with class constants annotated with Final."""
    CLASS_CONST: Final[int] = 42
    CLASS_CONST2: Final = "const"
    variable: Final[str] = "invalid name"  # [invalid-name]
    CLASS_CONST3: typing.Final
    variable2: typing.Final[int]  # [invalid-name]
    CLASS_CONST4: Final[typing.ClassVar[str]] = "valid"

MODULE_CONST: Final = 1
module_var: typing.Final[str] = "const"  # [invalid-name]
