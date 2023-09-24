# pylint: disable=missing-docstring,invalid-name
from functools import cached_property


# https://github.com/pylint-dev/pylint/issues/4023
# False-positive 'invalid-overridden-method' with 'cached_property'
class Parent:
    @property
    def value(self):
        return 42

    def func(self):
        return False


class Child(Parent):
    @cached_property
    def value(self):
        return 2**6

    @cached_property
    def func(self):  # [invalid-overridden-method]
        return 42
