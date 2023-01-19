"""Tests for no-member on decorated properties.

https://github.com/PyCQA/pylint/issues/1127
"""
# pylint: disable=missing-function-docstring, too-few-public-methods, invalid-name
# pylint: disable=deprecated-module, missing-class-docstring

from unittest import TestCase

class prop:
    def __init__(self):
        self.value = 5

class my_class:
    @prop
    def my_property(self):
        pass

print(my_class().my_property.value)


def with_value(klass):
    klass_setup = klass.setup

    def _setup(self):
        self.value = 5
        self.addcleanup(delattr, self, 'value')
        klass_setup(self)

    klass.setup = _setup

    return klass

@with_value
class TestValue(TestCase):
    def test_value(self):
        value = self.value
        self.assertEqual(value, 5)
