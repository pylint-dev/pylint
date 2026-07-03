"""Tests for singledispatch-method"""
# pylint: disable=missing-class-docstring, missing-function-docstring,too-few-public-methods


from functools import singledispatch


class Board1:
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


class Board2:
    @singledispatch  # [singledispatch-method]
    @classmethod
    def convert_position(cls, position):
        pass

    @convert_position.register  # [singledispatch-method]
    @classmethod
    def _(cls, position: str) -> tuple:
        position_a, position_b = position.split(",")
        return (int(position_a), int(position_b))

    @convert_position.register  # [singledispatch-method]
    @classmethod
    def _(cls, position: tuple) -> str:
        return f"{position[0]},{position[1]}"



class Board3:
    @singledispatch  # [singledispatch-method]
    @staticmethod
    def convert_position(position):
        pass

    @convert_position.register  # [singledispatch-method]
    @staticmethod
    def _(position: str) -> tuple:
        position_a, position_b = position.split(",")
        return (int(position_a), int(position_b))

    @convert_position.register  # [singledispatch-method]
    @staticmethod
    def _(position: tuple) -> str:
        return f"{position[0]},{position[1]}"


# Do not emit `singledispatch-method`:
@singledispatch
def convert_position(position):
    print(position)

@convert_position.register
def _(position: str) -> tuple:
    position_a, position_b = position.split(",")
    return (int(position_a), int(position_b))

@convert_position.register
def _(position: tuple) -> str:
    return f"{position[0]},{position[1]}"
