# pylint: disable=arguments-differ, missing-docstring, no-self-use, too-few-public-methods, useless-object-inheritance, line-too-long
"""Test where we are emitting arguments-renamed when the
    arguments have been renamed without changing type.
"""

class Parent(object):

    def test(self, arg: int):
        return arg + 1


class Child(Parent):

    def test(self, arg1: int): # [arguments-renamed]
        return arg1 + 1

class Child2(Parent):

    def test(self, var: int): # [arguments-renamed]
        return var + 1

class ParentDefaults(object):

    def test1(self, arg: str, barg: str):
        print(f"Argument values are {arg} and {barg}")

    def test2(self, arg: str, barg: str):
        print(f"Argument values are {arg} and {barg}!")

    def test3(self, arg1: str, arg2: bool):
        print(f"arguments: {arg1} {arg2}")

class ChildDefaults(ParentDefaults):

    def test1(self, param1: str, param2: str): # [arguments-renamed]
        print(f"Argument values are {param1} and {param2}")

    def test2(self, param1: int, param2: bool, param3: int): # no arguments-renamed here
        print(f"Argument values are {param1}, {param2} and {param3}!")

    def test3(self, param1: bool, arg2: bool): # no arguments-renamed here
        print(f"arguments: {param1} {arg2}")
    