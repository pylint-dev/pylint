# pylint: disable=missing-docstring,too-few-public-methods
from typing import Any


class Egg:
    def __init__(self, first: Any, /, second: Any) -> None:
        pass


class Spam(Egg):
    def __init__(self, first: float, /, second: float) -> None:
        super().__init__(first, second)


class Ham(Egg):
    def __init__(self, first: Any, /, second: Any) -> None:  # [useless-super-delegation]
        super().__init__(first, second)
