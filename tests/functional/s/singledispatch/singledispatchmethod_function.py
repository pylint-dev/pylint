"""Tests for singledispatchmethod-function"""
# pylint: disable=missing-class-docstring, missing-function-docstring,too-few-public-methods


from functools import singledispatchmethod


# Emit `singledispatchmethod-function` when functions are decorated with `singledispatchmethod`
@singledispatchmethod  # [singledispatchmethod-function]
def convert_position2(position):
    print(position)

@convert_position2.register  # [singledispatchmethod-function]
def _(position: str) -> tuple:
    position_a, position_b = position.split(",")
    return (int(position_a), int(position_b))

@convert_position2.register  # [singledispatchmethod-function]
def _(position: tuple) -> str:
    return f"{position[0]},{position[1]}"


class Board1:
    @singledispatchmethod
    def convert_position(self, position):
        pass

    @convert_position.register
    def _(self, position: str) -> tuple:
        position_a, position_b = position.split(",")
        return (int(position_a), int(position_b))

    @convert_position.register
    def _(self, position: tuple) -> str:
        return f"{position[0]},{position[1]}"


class Board2:
    @singledispatchmethod
    @staticmethod
    def convert_position(position):
        pass

    @convert_position.register
    @staticmethod
    def _(position: str) -> tuple:
        position_a, position_b = position.split(",")
        return (int(position_a), int(position_b))

    @convert_position.register
    @staticmethod
    def _(position: tuple) -> str:
        return f"{position[0]},{position[1]}"


class Board3:
    @singledispatchmethod
    @classmethod
    def convert_position(cls, position):
        pass

    @convert_position.register
    @classmethod
    def _(cls, position: str) -> tuple:
        position_a, position_b = position.split(",")
        return (int(position_a), int(position_b))

    @convert_position.register
    @classmethod
    def _(cls, position: tuple) -> str:
        return f"{position[0]},{position[1]}"
