""""Checks for redundant Union typehints in assignments - python 3.10"""
from __future__ import annotations


ANSWER_0: int | int = 0  # [redundant-typehint-argument]
ANSWER_1: str | int | None | int | bool = 1   # [redundant-typehint-argument]
ANSWER_2: dict | list[int] | float | str | int | bool = 2
#  +1: [redundant-typehint-argument]
ANSWER_3: list[int] | dict[int] | dict[list[int]] | list[str] | list[str] = 3  #
