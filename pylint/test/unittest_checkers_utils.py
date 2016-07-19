# Copyright (c) 2003-2016 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the pylint.checkers.utils module."""

import unittest
import warnings

from astroid import test_utils

from pylint.checkers import utils
from pylint import __pkginfo__

class UtilsTC(unittest.TestCase):

    def test_is_builtin(self):
        self.assertEqual(utils.is_builtin('min'), True)
        self.assertEqual(utils.is_builtin('__builtins__'), True)
        self.assertEqual(utils.is_builtin('__path__'), False)
        self.assertEqual(utils.is_builtin('__file__'), False)
        self.assertEqual(utils.is_builtin('whatever'), False)
        self.assertEqual(utils.is_builtin('mybuiltin'), False)

    def testGetArgumentFromCall(self):
        node = test_utils.extract_node('foo(bar=3)')
        self.assertIsNotNone(utils.get_argument_from_call(node, keyword='bar'))
        with self.assertRaises(utils.NoSuchArgumentError):
            node = test_utils.extract_node('foo(3)')
            utils.get_argument_from_call(node, keyword='bar')
        with self.assertRaises(utils.NoSuchArgumentError):
            node = test_utils.extract_node('foo(one=a, two=b, three=c)')
            utils.get_argument_from_call(node, position=1)
        node = test_utils.extract_node('foo(a, b, c)')
        self.assertIsNotNone(utils.get_argument_from_call(node, position=1))
        node = test_utils.extract_node('foo(a, not_this_one=1, this_one=2)')
        arg = utils.get_argument_from_call(node, position=2, keyword='this_one')
        self.assertEqual(2, arg.value)
        node = test_utils.extract_node('foo(a)')
        with self.assertRaises(utils.NoSuchArgumentError):
            utils.get_argument_from_call(node, position=1)
        with self.assertRaises(ValueError):
            utils.get_argument_from_call(node, None, None)

        name = utils.get_argument_from_call(node, position=0)
        self.assertEqual(name.name, 'a')

    def test_error_of_type(self):
        nodes = test_utils.extract_node("""
        try: pass
        except AttributeError: #@
             pass
        try: pass
        except Exception: #@
             pass
        except: #@
             pass
        """)
        self.assertTrue(utils.error_of_type(nodes[0], AttributeError))
        self.assertTrue(utils.error_of_type(nodes[0], (AttributeError, )))
        self.assertFalse(utils.error_of_type(nodes[0], Exception))
        self.assertTrue(utils.error_of_type(nodes[1], Exception))
        self.assertFalse(utils.error_of_type(nodes[2], ImportError))

    def test_node_ignores_exception(self):
        nodes = test_utils.extract_node("""
        try:
            1/0 #@
        except ZeroDivisionError:
            pass
        try:
            1/0 #@
        except Exception:
            pass
        try:
            2/0 #@
        except:
            pass
        try:
            1/0 #@
        except ValueError:
            pass
        """)
        self.assertTrue(utils.node_ignores_exception(nodes[0], ZeroDivisionError))
        self.assertFalse(utils.node_ignores_exception(nodes[1], ZeroDivisionError))
        self.assertFalse(utils.node_ignores_exception(nodes[2], ZeroDivisionError))
        self.assertFalse(utils.node_ignores_exception(nodes[3], ZeroDivisionError))


if __name__ == '__main__':
    unittest.main()
