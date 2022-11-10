""""Checks for redundant Union typehints in assignments"""
# pylint: disable=deprecated-typing-alias,consider-alternative-union-syntax,line-too-long

from typing import Union, Optional, Sequence


ANSWER_0: Union[int, int] = 0  # [redundant-union-assign-typehint]
ANSWER_1: Optional[int] = 1
ANSWER_1_1: Sequence[int] = 11
ANSWER_2: int | int = 2  # [redundant-union-assign-typehint]
ANSWER_3: Union[int, str, int, int, bool] = 3  # [redundant-union-assign-typehint]
ANSWER_4: Optional[None] = 4   # [redundant-union-assign-typehint]
ANSWER_5: Optional[list[int]] = 5
ANSWER_6: str | int | int | int | bool = 6   # [redundant-union-assign-typehint]
ANSWER_7: dict | list[int] | float | str | int | bool = 7
ANSWER_8: Union[list[int], dict[int], dict[list[int]], list[str], list[str]] = 8  # [redundant-union-assign-typehint]
