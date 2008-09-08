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
""" Copyright (c) 2003-2005 LOGILAB S.A. (Paris, FRANCE).
 http://www.logilab.fr/ -- mailto:contact@logilab.fr

Check source code is ascii only or has an encoding declaration (PEP 263)
"""

__revision__ = '$Id: test_encoding.py,v 1.6 2005-11-02 09:22:04 syt Exp $'

from logilab.common.testlib import TestCase, unittest_main
import sys
from pylint.checkers.misc import guess_encoding

class TestGuessEncoding(TestCase):

    def testEmacs(self):
        e = guess_encoding('# -*- coding: UTF-8  -*-')
        self.failUnlessEqual(e, 'UTF-8')
        e = guess_encoding('# -*- coding:UTF-8 -*-')
        self.failUnlessEqual(e, 'UTF-8')
        e = guess_encoding('''
        ### -*- coding: ISO-8859-1  -*-
        ''')
        self.failUnlessEqual(e, 'ISO-8859-1')
        e = guess_encoding('''
        
        ### -*- coding: ISO-8859-1  -*-
        ''')
        self.failUnlessEqual(e, None)

    def testVim(self):
        e = guess_encoding('# vim:fileencoding=UTF-8')
        self.failUnlessEqual(e, 'UTF-8')
        e = guess_encoding('''
        ### vim:fileencoding=ISO-8859-1  
        ''')
        self.failUnlessEqual(e, 'ISO-8859-1')
        e = guess_encoding('''
        
        ### vim:fileencoding= ISO-8859-1  
        ''')
        self.failUnlessEqual(e, None)

    def testUTF8(self):
        e = guess_encoding('\xef\xbb\xbf any UTF-8 data')
        self.failUnlessEqual(e, 'UTF-8')
        e = guess_encoding(' any UTF-8 data \xef\xbb\xbf')
        self.failUnlessEqual(e, None)
        
if __name__ == '__main__':
    unittest_main()
