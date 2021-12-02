"""Tests for undefined-variable related to classes"""
# pylint: disable=missing-function-docstring, missing-class-docstring, too-few-public-methods

# Test that list comprehensions in base classes are scoped correctly
# Regression reported in https://github.com/PyCQA/pylint/issues/3434

import collections

l = ["a", "b", "c"]


class Foo(collections.namedtuple("Foo", [x + "_foo" for x in l])):
    pass


# Test that class attributes are in scope for return type annotations.
# Regression reported in https://github.com/PyCQA/pylint/issues/1976
class MyObject:
    class MyType:
        pass

    def my_method(self) -> MyType:
        pass
