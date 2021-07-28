"""Test deprecated abc decorators from Python 3.3."""
# pylint: disable=missing-class-docstring,too-few-public-methods,missing-function-docstring,no-member

import abc

class MyClass:
    @abc.abstractclassmethod  # [deprecated-decorator]
    def my_method(cls):
        pass

class Foo:
    def __init__(self):
        self._baz = 84

    def method(self):
        return self._baz

    @method.setter          # Invalid decorator
    def method(self, value):
        self._baz = value
