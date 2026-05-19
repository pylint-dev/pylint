from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)
