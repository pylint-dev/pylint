"""Test check for classes extending an Enum class."""
# pylint: disable=missing-class-docstring,invalid-name
from enum import Enum, IntFlag

# We don't flag the Enum class itself
class A(Enum):
    x = 1
    y = 2

# But we do flag any inheriting classes
# that try to extend the Enum class.
class B(A):  # [invalid-enum-extension]
    z = 3

# If no items have been added to the base
# Enum class then the lint is not raised.
class C(Enum):
    pass

class D(C):
    x = 3


# Similarly, items that are only type annotations are okay.
class ColorEnum(Enum):
    red: int
    green: int
    blue: int

    def __init__(self, red: int, green: int, blue: int) -> None:
        self.red = red
        self.green = green
        self.blue = blue


class Pastel(ColorEnum):
    SAGE = (170, 200, 167)


class IncorrectColorEnum(Enum):
    red: None = None

    def __init__(self, red: None) -> None:
        self.red = red


class IncorrectPastel(IncorrectColorEnum):  # [invalid-enum-extension]
    SOME_COLOR = 170


class CustomFlags(IntFlag):
    SUPPORT_OPEN = 1
    SUPPORT_CLOSE = 2
