"""
If you are using assertTrue or assertFalse and the first argument is a constant
(like a string), then the assert will always be true. Therefore, it should emit
a warning message.
"""

# pylint: disable=missing-docstring,too-few-public-methods

# Disabled because of a bug with pypy 3.8 see
# https://github.com/pylint-dev/pylint/pull/7918#issuecomment-1352737369
# pylint: disable=multiple-statements

import unittest


@unittest.skip("don't run this")
class Tests(unittest.TestCase):
    def test_something(self):
        ''' Simple test '''
        some_var = 'It should be assertEqual'
        # +1:[redundant-unittest-assert]
        self.assertTrue('I meant assertEqual not assertTrue', some_var)
        # +1:[redundant-unittest-assert]
        self.assertFalse('I meant assertEqual not assertFalse', some_var)
        # +1:[redundant-unittest-assert]
        self.assertTrue(True, some_var)
        # +1:[redundant-unittest-assert]
        self.assertFalse(False, some_var)
        # +1:[redundant-unittest-assert]
        self.assertFalse(None, some_var)
        # +1:[redundant-unittest-assert]
        self.assertTrue(0, some_var)

        self.assertTrue('should be' in some_var, some_var)
        self.assertTrue(some_var, some_var)


@unittest.skip("don't run this")
class RegressionWithArgs(unittest.TestCase):
    '''Don't fail if the bound method doesn't have arguments.'''

    def test(self):
        self.run()
