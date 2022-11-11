""""Checks for redundant Union typehints in assignments - python 3.7"""
from typing import Union, Optional, Sequence

#  +1: [redundant-union-assign-typehint, redundant-union-assign-typehint]
ANSWER_0: Union[int, int, str, bool, str] = 0  #
ANSWER_1: Optional[int] = 1
ANSWER_2: Sequence[int] = 2
ANSWER_4: Optional[None] = 4   # [redundant-union-assign-typehint]
