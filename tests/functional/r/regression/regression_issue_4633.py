# pylint: disable=missing-docstring,too-few-public-methods

"""
Regression tests for https://github.com/pylint-dev/pylint/issues/4633
"""

from queue import Queue
from unittest.mock import MagicMock

mock = MagicMock(name="mock")


class Ham(mock.spam):
    def __init__(self):
        self.queue = Queue()


class SecondHam:
    def whatever(self):
        test_var = Ham()
        while not test_var.queue.empty():
            pass
