# Copyright (c) 2003-2005 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
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

    def test_is_import_error(self):
        import_error, not_import_error = test_utils.extract_node("""
        try:
            pass
        except ImportError: #@
            pass

        try:
            pass
        except AttributeError: #@
            pass
        """)

        if __pkginfo__.numversion >= (1, 6, 0):
            with self.assertRaises(AttributeError):
                utils.is_import_error

        with warnings.catch_warnings(record=True) as cm:
            warnings.simplefilter("always")

            self.assertTrue(utils.is_import_error(import_error))
            self.assertFalse(utils.is_import_error(not_import_error))

        self.assertEqual(len(cm), 2)
        self.assertIsInstance(cm[0].message, DeprecationWarning)

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
        self.assertTrue(utils.error_of_type(nodes[2], ImportError))

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
            1/0 #@
        except:
            pass
        try:
            1/0 #@
        except ValueError:
            pass
        """)
        self.assertTrue(utils.node_ignores_exception(nodes[0], ZeroDivisionError))
        self.assertTrue(utils.node_ignores_exception(nodes[1], ZeroDivisionError))
        self.assertTrue(utils.node_ignores_exception(nodes[2], ZeroDivisionError))
        self.assertFalse(utils.node_ignores_exception(nodes[3], ZeroDivisionError))


if __name__ == '__main__':
    unittest.main()
