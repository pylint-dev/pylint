from enum import Enum


class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2


def func(color: Color) -> None:
    match color:
        case Color.RED:
            print("I see red!")
        case Color.GREEN:
            print("Grass is green")
        case Color.BLUE:
            print("I'm feeling the blues :(")
