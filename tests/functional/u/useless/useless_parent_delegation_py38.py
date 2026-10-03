# pylint: disable=missing-docstring,too-few-public-methods
from typing import Any


class Egg:
    def __init__(self, first: Any, /, second: Any) -> None:
        pass


class Spam(Egg):
    def __init__(self, first: float, /, second: float) -> None:
        super().__init__(first, second)


class Ham(Egg):
    def __init__(self, first: Any, /, second: Any) -> None:  # [useless-parent-delegation]
        super().__init__(first, second)


class EggWithDefaults:
    def __init__(self, first: Any = 1, /, second: Any = 2) -> None:
        pass


class HamChangedPosonlyDefault(EggWithDefaults):
    # Not useless: the positional-only ``first`` has a different default from the
    # base, so the override changes behaviour (regression test for posonlyargs).
    def __init__(self, first: Any = 9, /, second: Any = 2) -> None:
        super().__init__(first, second)


class SpamSamePosonlyDefault(EggWithDefaults):
    def __init__(self, first: Any = 1, /, second: Any = 2) -> None:  # [useless-parent-delegation]
        super().__init__(first, second)
