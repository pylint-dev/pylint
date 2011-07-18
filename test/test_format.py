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
""" Copyright (c) 2000-2011 LOGILAB S.A. (Paris, FRANCE).
 http://www.logilab.fr/ -- mailto:contact@logilab.fr

Check format checker helper functions
"""

import sys
import re
from os import linesep

from logilab.common.testlib import TestCase, unittest_main

from pylint.checkers.format import *

from utils import TestReporter

REPORTER = TestReporter()

class StringRgxTest(TestCase):
    """test the STRING_RGX regular expression"""

    def test_known_values_1(self):
        self.assertEqual(STRING_RGX.sub('', '"yo"'), '')

    def test_known_values_2(self):
        self.assertEqual(STRING_RGX.sub('', "'yo'"), '')

    def test_known_values_tq_1(self):
        self.assertEqual(STRING_RGX.sub('', '"""yo"""'), '')

    def test_known_values_tq_2(self):
        self.assertEqual(STRING_RGX.sub('', '"""yo\n"""'), '')

    def test_known_values_ta_1(self):
        self.assertEqual(STRING_RGX.sub('', "'''yo'''"), '')

    def test_known_values_ta_2(self):
        self.assertEqual(STRING_RGX.sub('', "'''yo\n'''"), '')

    def test_known_values_5(self):
        self.assertEqual(STRING_RGX.sub('', r'"yo\"yo"'), '')

    def test_known_values_6(self):
        self.assertEqual(STRING_RGX.sub('', r"'yo\'yo'"), '')

    def test_known_values_7(self):
        self.assertEqual(STRING_RGX.sub('', '"yo"upi"yo"upi'), 'upiupi')

    def test_known_values_8(self):
        self.assertEqual(STRING_RGX.sub('', r"'yo\'yo\''"), '')

    def test_known_values_9(self):
        self.assertEqual(STRING_RGX.sub('', r'"yoyo\""'), '')

    def test_known_values_10(self):
        self.assertEqual(STRING_RGX.sub('', 'self.filterFunc = eval(\'lambda %s: %s\'%(\',\'.join(variables),formula),{},{})'),
                         'self.filterFunc = eval(%(.join(variables),formula),{},{})')

    def test_known_values_11(self):
        self.assertEqual(STRING_RGX.sub('', 'cond_list[index] = OLD_PROG.sub(r\'getattr(__old__,"\1")\',cond)'),
                         'cond_list[index] = OLD_PROG.sub(r,cond)')


    def test_no_crash(self):
        crash_str = """wizardBmp = ('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\n', (115, 260), None)"""
        re.sub(SQSTRING_RGX, '', crash_str)
        re.sub(TQSTRING_RGX, '', crash_str)
        re.sub(SASTRING_RGX, '', crash_str)
        re.sub(TASTRING_RGX, '', crash_str)
        self.skipTest('XXX: explain the test, remove it or assert something')

if linesep != '\n':
    LINE_RGX = re.compile(linesep)
    def ulines(strings):
        return strings[0], LINE_RGX.sub('\n', strings[1])
else:
    def ulines(strings):
        return strings

class ChecklineFunctionTest(TestCase):
    """test the check_line method"""

    def test_known_values_opspace_1(self):
        self.assertEqual(ulines(check_line('a=1')), ('C0322', 'a=1\n ^'))

    def test_known_values_opspace_2(self):
        self.assertEqual(ulines(check_line('a= 1')), ('C0322', 'a= 1\n ^') )

    def test_known_values_opspace_3(self):
        self.assertEqual(ulines(check_line('a =1')), ('C0323', 'a =1\n  ^'))

    def test_known_values_opspace_4(self):
        self.assertEqual(check_line('f(a=1)'), None)

    def test_known_values_opspace_4(self):
        self.assertEqual(check_line('f(a=1)'), None)

    def test_known_values_colonnl_2(self):
        self.assertEqual(check_line('a[:1]'), None)

    def test_known_values_colonnl_3(self):
        self.assertEqual(check_line('a[1:]'), None)

    def test_known_values_colonnl_4(self):
        self.assertEqual(check_line('a[1:2]'), None)

    def test_known_values_colonnl_5(self):
        self.assertEqual(check_line('def intersection(list1, list2):'), None)

    def test_known_values_colonnl_6(self):
        self.assertEqual(check_line('def intersection(list1, list2):\n'), None)

    def test_known_values_colonnl_7(self):
        self.assertEqual(check_line('if file[:pfx_len] == path:\n'), None)

    def test_known_values_colonnl_9(self):
        self.assertEqual(check_line('if file[:pfx_len[1]] == path:\n'), None)

    def test_known_values_colonnl_10(self):
        self.assertEqual(check_line('if file[pfx_len[1]] == path:\n'), None)

    def test_known_values_commaspace_1(self):
        self.assertEqual(ulines(check_line('a, b = 1,2')),
                         ('C0324', 'a, b = 1,2\n        ^^'))

    def test_known_values_commaspace_2(self):
        self.assertEqual(check_line('should_not_warn = [1, 2, 3,]\n'),
                         None)

    def test_known_values_commaspace_3(self):
        self.assertEqual(check_line('should_not_warn = {1:2, 3:4,}\n'),
                         None)

    def test_known_values_commaspace_4(self):
        self.assertEqual(check_line('should_not_warn = (1, 2, 3,)\n'),
                         None)

    def test_known_values_instring_1(self):
        self.assertEqual(check_line('f("a=1")'), None)

    def test_known_values_instring_2(self):
        self.assertEqual(ulines(check_line('print >>1, ("a:1")')),
                         ('C0323', 'print >>1, ("a:1")\n       ^'))

    def test_known_values_all_1(self):
        self.assertEqual(ulines(check_line("self.filterFunc = eval('lambda %s: %s'%(','.join(variables),formula),{},{})")),
                         ('C0324', "self.filterFunc = eval('lambda %s: %s'%(','.join(variables),formula),{},{})\n                                                           ^^"))

    def test_known_values_tqstring(self):
        self.assertEqual(check_line('print """<a="=")\n"""'), None)

    def test_known_values_tastring(self):
        self.assertEqual(check_line("print '''<a='=')\n'''"), None)

if __name__ == '__main__':
    unittest_main()
