"""Test for the regression on inference of self referential __len__
Reported in https://github.com/pylint-dev/pylint/issues/5244
"""
# pylint: disable=missing-class-docstring, missing-function-docstring


class MyClass:
    def some_func(self):
        return lambda: 42

    def __len__(self):
        return len(self.some_func())
