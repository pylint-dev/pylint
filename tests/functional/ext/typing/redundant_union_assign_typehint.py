""""Checks for redundant Union typehints in assignments"""
# pylint: disable=deprecated-typing-alias,consider-alternative-union-syntax

from typing import Union, Optional, Sequence

ANSWER_0: Union[int, int] = 0  # [redundant-union-assign-typehint]
ANSWER_1: Optional[int] = 1
ANSWER_1_1: Sequence[int] = 11
ANSWER_2: int | int = 2  # [redundant-union-assign-typehint]

ANSWER_3: Union[int, str, int, int, bool] = 3  # [redundant-union-assign-typehint]
ANSWER_4: Optional[None] = 4   # [redundant-union-assign-typehint]
ANSWER_5: int | str | int | int | bool = 5   # [redundant-union-assign-typehint]
