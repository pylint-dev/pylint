from __future__ import annotations

# pylint: disable-next=import-error
from lib import Banana, Coconut, Sound  # type: ignore[import]


class Monkey:
    def eat(self, food: Banana | Coconut) -> None:
        print(f"Monkey eats {food}")

    def jump(self, height: int | None = 10) -> None:
        print(f"Monkey jumps {height}")

    def scream(self, volume: int | None) -> Sound:
        if volume is None:
            volume = 0
        return Sound(volume)
