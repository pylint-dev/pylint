# pylint: disable=missing-docstring,too-few-public-methods
"""http://www.logilab.org/ticket/355"""

import unittest


class Tests(unittest.TestCase):
    def test_something(self):
        ''' Simple test '''
        some_var = 'It should be assertEqual'
        # +1:[redundant-assert]
        self.assertTrue('I meant assertEqual', some_var)
