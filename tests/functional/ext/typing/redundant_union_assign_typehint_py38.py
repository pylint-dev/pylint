""""Checks for redundant Union typehints in assignments - python 3.8"""
# pylint: disable=deprecated-typing-alias

from __future__ import annotations
from typing import Union, Optional, Sequence

#  +1: [redundant-union-assign-typehint, redundant-union-assign-typehint]
ANSWER_0: Union[int, int, str, bool, float, str] = 0  #
ANSWER_1: Optional[int] = 1
ANSWER_2: Sequence[int] = 2
ANSWER_3: Union[list[int], str, int, bool, list[int]] = 3  # [redundant-union-assign-typehint]
ANSWER_4: Optional[None] = 4   # [redundant-union-assign-typehint]
ANSWER_5: Optional[list[int]] = 5
ANSWER_4: Union[None, None] = 4   # [redundant-union-assign-typehint]
#  +1: [redundant-union-assign-typehint]
ANSWER_5: Union[list[int], dict[int], dict[list[int]], list[str], list[str]] = 5  #
