"""Regression test for 8207."""

# pylint: disable=missing-docstring,too-few-public-methods

class Example:
    def __init__(self):
        self.offset = -10

    def minus_offset(self):
        return {
            (x, x): value
            for x, row in enumerate([(5, 10), (20, 30)])
            for y, value in enumerate(row, -self.offset)
        }
