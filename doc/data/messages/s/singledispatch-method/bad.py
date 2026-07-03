from functools import singledispatch


class Board:
    @singledispatch  # [singledispatch-method]
    def convert_position(self, position):
        pass

    @convert_position.register  # [singledispatch-method]
    def _(self, position: str) -> tuple:
        position_a, position_b = position.split(",")
        return (int(position_a), int(position_b))

    @convert_position.register  # [singledispatch-method]
    def _(self, position: tuple) -> str:
        return f"{position[0]},{position[1]}"
