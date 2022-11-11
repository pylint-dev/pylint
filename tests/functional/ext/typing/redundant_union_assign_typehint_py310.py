""""Checks for redundant Union typehints in assignments - python 3.10"""

ANSWER_0: int | int = 0  # [redundant-union-assign-typehint]
ANSWER_1: str | int | None | int | bool = 1   # [redundant-union-assign-typehint]
ANSWER_2: dict | list[int] | float | str | int | bool = 2
#  +1: [redundant-union-assign-typehint]
ANSWER_3: list[int] | dict[int] | dict[list[int]] | list[str] | list[str] = 3  #
