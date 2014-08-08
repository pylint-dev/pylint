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

import sys
import unittest

from astroid import test_utils

from pylint.checkers import utils
try:
    __builtins__.mybuiltin = 2
except AttributeError:
    __builtins__['mybuiltin'] = 2

class UtilsTC(unittest.TestCase):
    
##     def test_is_native_builtin(self):
##         self.assertEqual(utils.is_native_builtin('min'), True)
##         self.assertEqual(utils.is_native_builtin('__path__'), True)
##         self.assertEqual(utils.is_native_builtin('__file__'), True)
##         self.assertEqual(utils.is_native_builtin('whatever'), False)
##         self.assertEqual(utils.is_native_builtin('mybuiltin'), False)

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
        arg = utils.get_argument_from_call(node, position=1, keyword='this_one')
        self.assertEqual(2, arg.value)
        node = test_utils.extract_node('foo(a)')
        with self.assertRaises(utils.NoSuchArgumentError):
            utils.get_argument_from_call(node, position=1)
        with self.assertRaises(ValueError):
            utils.get_argument_from_call(node, None, None)
                
        name = utils.get_argument_from_call(node, position=0)
        self.assertEqual(name.name, 'a')

if __name__ == '__main__':
    unittest.main()
        
