"""Tests for no-member in relation to binary operations."""
# pylint: disable=too-few-public-methods, missing-class-docstring, missing-function-docstring

# Test for: https://github.com/pylint-dev/pylint/issues/4826
class MyClass:
    def __init__(self):
        self.a_list = []
        self.data = []

    def operator(self):
        for i in [self] + self.a_list:
            for _ in i.data:
                pass
