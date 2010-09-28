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
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""test the pylint.checkers.utils module
"""

__revision__ = '$Id: unittest_checkers_utils.py,v 1.6 2005-11-02 09:22:07 syt Exp $'

import unittest
import sys

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

if __name__ == '__main__':
    unittest.main()
        
