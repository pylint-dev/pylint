# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring
# pylint: disable=too-few-public-methods
from typing import overload


class ClassA:
    @classmethod
    @overload
    def method(cls, arg1):
        pass

    @classmethod
    @overload
    def method(cls, arg1, arg2):
        pass

    @classmethod
    def method(cls, arg1, arg2=None):
        pass


ClassA.method(1, 2)


class ClassB:
    @overload
    def method(self, arg1):
        pass

    @overload
    def method(self, arg1, arg2):
        pass

    def method(self, arg1, arg2=None):
        pass


ClassB().method(1, arg2=2)
