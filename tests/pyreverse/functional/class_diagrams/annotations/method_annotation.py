# pylint: disable=import-error,consider-alternative-union-syntax
from __future__ import annotations

from typing import Optional, Union

from lib import Banana, Coconut, Insect, Leaf, Sound  # type: ignore[import]


class Monkey:
    def eat(self, food: Banana | Coconut) -> None:
        print(f"Monkey eats {food}")

    def munch(self, food: Union[Leaf, Insect]) -> None:
        print(f"Monkey munches {food}")

    def jump(self, height: Optional[int] = 10) -> None:
        print(f"Monkey jumps {height}")

    def scream(self, volume: int | None) -> Sound:
        if volume is None:
            volume = 0
        return Sound(volume)
