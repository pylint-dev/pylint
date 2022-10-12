from functools import singledispatchmethod


class Board:
    @singledispatchmethod
    def convert_position(cls, position):
        pass

    @singledispatchmethod
    @classmethod
    def _(cls, position: str) -> tuple:
        position_a, position_b = position.split(",")
        return (int(position_a), int(position_b))

    @singledispatchmethod
    @classmethod
    def _(cls, position: tuple) -> str:
        return f"{position[0]},{position[1]}"
