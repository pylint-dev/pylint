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


@unittest.skip("don't run this")
class ConstantComparisons(unittest.TestCase):
    '''assertEqual and assertNotEqual have a fixed outcome when both operands are constants.'''

    def test_constants(self):
        # +1:[redundant-unittest-assert]
        self.assertEqual(5, 5)
        # +1:[redundant-unittest-assert]
        self.assertEqual(5, 6)
        # +1:[redundant-unittest-assert]
        self.assertNotEqual('a', 'a', 'with a message')
        # +1:[redundant-unittest-assert]
        self.assertEqual(None, None)

    def test_runtime_values(self):
        some_var = 5
        self.assertEqual(some_var, 5)
        self.assertNotEqual(5, some_var)

    def test_unsupported_operands(self):
        self.assertEqual([1], [1])
        self.assertEqual((1,), (1,))
        self.assertEqual(1 + 1, 2)
        self.assertIs(5, 5)
        self.assertEqual(first=5, second=5)


class NotATestCase:
    '''Methods that only share a name with unittest assertions are left alone.'''

    def assertEqual(self, first, second):  # pylint: disable=invalid-name
        return first == second

    def check(self):
        self.assertEqual(5, 5)
