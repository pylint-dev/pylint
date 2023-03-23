"""Tests for singledispatch-method"""
# pylint: disable=missing-class-docstring, missing-function-docstring,too-few-public-methods


from functools import singledispatch


class Board:
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
