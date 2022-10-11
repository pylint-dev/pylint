from functools import singledispatch


class GoodBoard:
    @singledispatch
    @staticmethod
    def convert_position(position):
        pass

    @convert_position.register
    @staticmethod
    def _(position: str) -> tuple:
        position_a, position_b = position.split(",")
        return (int(position_a), int(position_b))

    @convert_position.register  # [singledispatch-method]
    @staticmethod
    def _(position: tuple) -> str:
        return f"{position[0]},{position[1]}"
