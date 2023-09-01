""""Tests for return type checkers for protocol methods with ellipsis function body"""
# pylint: disable=missing-class-docstring
from typing import Any, Iterator


class MyClass:
    """The "invalid-*-returned" messages shouldn't be emitted for stub functions
    Original issue: https://github.com/pylint-dev/pylint/issues/4736"""

    def __len__(self) -> int:
        ...

    def __hash__(self) -> int:
        ...

    def __index__(self) -> int:
        ...

    def __iter__(self) -> Iterator[Any]:
        ...

    def __bool__(self) -> bool:
        ...

    def __repr__(self) -> object:
        ...

    def __str__(self) -> str:
        ...

    def __bytes__(self) -> bytes:
        ...

    def __length_hint__(self) -> int:
        ...

    def __format__(self, format_spec: str) -> str:
        ...

    def __getnewargs__(self) -> tuple:
        ...

    def __getnewargs_ex__(self) -> tuple:
        ...
