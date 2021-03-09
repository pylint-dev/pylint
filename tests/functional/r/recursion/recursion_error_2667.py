"""Add regression test for https://github.com/PyCQA/pylint/issues/2667"""
# pylint: disable=missing-docstring, too-few-public-methods

class MyClass:
    def __init__(self):
        self._slice = slice(0, 10)

    def incr(self):
        self._slice = slice(0, self._slice.stop + 1)
