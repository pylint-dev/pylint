"""Tests for missing-function-docstring and the no-docstring-rgx option"""
# pylint: disable=unused-argument, missing-class-docstring, too-few-public-methods


class MyClass:
    pass


class Child(MyClass):  # [eq-without-hash]
    def __eq__(self, other):  # [missing-function-docstring]
        return True
