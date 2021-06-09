"""Test for https://github.com/PyCQA/pylint/issues/2683"""
# pylint: disable=missing-docstring,too-few-public-methods

class Cls:
    def __init__(self):
        self.count = 5

    def method(self):
        records = []
        for _ in []:
            records += []
        records = records[:self.count]
        records.sort()
