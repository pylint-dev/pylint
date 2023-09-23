""" Tests for invalid-name checker in the context of enums. """
# pylint: disable=too-few-public-methods


from enum import Enum


class Color(Enum):
    """Represents colors as (red, green, blue) tuples."""

    YELLOW      = 250, 250,   0
    KHAKI       = 250, 250, 125
    MAGENTA     = 250,   0, 250
    VIOLET      = 250, 125, 250
    CYAN        =   0, 250, 250
    aquamarine  = 125, 250, 250  # [invalid-name]

    red: int
    green: int
    blue: int

    def __init__(self, red: int, green: int, blue: int) -> None:
        self.red   = red
        self.green = green
        self.blue  = blue

    @property
    def as_hex(self) -> str:
        """Get hex 'abcdef' representation for a color."""
        return f'{self.red:0{2}x}{self.green:0{2}x}{self.blue:0{2}x}'
