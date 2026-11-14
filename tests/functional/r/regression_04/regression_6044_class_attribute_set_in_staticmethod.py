"""Regression test for https://github.com/pylint-dev/pylint/issues/6044

A class attribute that starts as None and is set through the class in a
staticmethod can be iterated after the call.
"""

# pylint: disable=missing-docstring,too-few-public-methods


class Holder:
    items = None

    @staticmethod
    def get_items():
        Holder.items = [1, 2, 3]
        return Holder.items

    def __init__(self):
        self.values = [item + 1 for item in Holder.get_items()]
