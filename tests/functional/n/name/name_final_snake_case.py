# pylint: disable=missing-docstring,too-few-public-methods
"""Test typing.Final with name style snake_case."""
import typing
from typing import Final

class Foo:
    """Class with class constants annotated with Final."""
    CLASS_CONST: Final[int] = 42  # [invalid-name]
    CLASS_CONST2: Final = "const"  # [invalid-name]
    variable: Final[str] = "invalid name"
    CLASS_CONST3: typing.Final  # [invalid-name]
    variable2: typing.Final[int]
    CLASS_CONST4: Final[typing.ClassVar[str]] = "invalid name"  # [invalid-name]

MODULE_CONST: Final = 1  # [invalid-name]
module_var: typing.Final[str] = "const"
