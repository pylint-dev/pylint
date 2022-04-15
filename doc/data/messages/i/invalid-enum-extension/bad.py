from enum import Enum


class Color(Enum):
    ORANGE = 1
    CHERRY = 2


class Fruit(Color):  # [invalid-enum-extension]
    APPLE = 3
