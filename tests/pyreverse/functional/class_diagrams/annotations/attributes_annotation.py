# pylint: disable=consider-alternative-union-syntax
from __future__ import annotations

from typing import Optional, Union


class Dummy:
    pass


class Dummy2:
    class_attr: list[Dummy] = []

    def __init__(self, param: str) -> None:
        self.param = param
        self.union: Union[int, str] = ""
        self.alternative_union_syntax: str | int = 0
        self.optional: Optional[Dummy] = None
        self.alternative_optional: int | None = None
        self.alternative_optional_swapped: None | int = None
        self.optional_union: int | str = None
