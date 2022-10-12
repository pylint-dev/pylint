from functools import singledispatchmethod


class Board:
    @singledispatchmethod  # [singledispatchmethod-function]
    @staticmethod
    def convert_position(position):
        pass

    @convert_position.register  # [singledispatchmethod-function]
    @staticmethod
    def _(position: str) -> tuple:
        position_a, position_b = position.split(",")
        return (int(position_a), int(position_b))

    @convert_position.register  # [singledispatchmethod-function]
    @staticmethod
    def _(position: tuple) -> str:
        return f"{position[0]},{position[1]}"
