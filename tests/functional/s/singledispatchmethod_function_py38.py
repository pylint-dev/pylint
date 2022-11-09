"""Tests for singledispatchmethod-function"""
# pylint: disable=missing-class-docstring, missing-function-docstring,too-few-public-methods


from functools import singledispatch, singledispatchmethod


class BoardRight:
    @singledispatch
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
