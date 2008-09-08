# Copyright (c) 2007 LOGILAB S.A. (Paris, FRANCE).
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
"""functional/non regression tests for the rpython mode of pylint 
"""

import unittest
import sys
import re
import new
from os import linesep
from os.path import exists

from logilab.common import testlib

from utils import get_tests_info, fix_path, TestReporter

from pylint.lint import PyLinter
from pylint import checkers

test_reporter = TestReporter()
linter = PyLinter()
linter.set_reporter(test_reporter)
linter.config.persistent = 0
checkers.initialize(linter)
linter.enable_checkers(['rpython'], True)
                       
from func_test import ulines, LintTestUsingFile

class RLintTestUsingFile(LintTestUsingFile):            
    package = 'rpythoninput'
    linter = linter
    def setUp(self):
        if sys.version_info[:2] != (2, 4):
            self.skip('only python 2.4 supported for now')
            
    def test_functionality(self):
        tocheck = ['rpythoninput/' + self.module + '.py']
        if self.depends:
            tocheck += ['rpythoninput/%s' % name for name, file in self.depends]
        self._test(tocheck)


class TestTests(testlib.TestCase):
    """check that all testable messages have been checked"""
    def setUp(self):
        if sys.version_info[:2] != (2, 4):
            self.skip('only python 2.4 supported for now')
            
    def test(self):
        # skip rpython checker messages
        missing = [msgid for msgid in linter._messages.keys()
                   if msgid[1:3] == '12' and not msgid in test_reporter.message_ids]
        self.assertEqual(missing, [])
        
def make_tests(filter_rgx):
    """generate tests classes from test info
    
    return the list of generated test classes
    """
    if filter_rgx:
        is_to_run = re.compile(filter_rgx).match
    else:
        is_to_run = lambda x: 1
    tests = []
    for module_file, messages_file in get_tests_info('func_', '.py',
                                                     'rpythoninput', 'rpythonmessages'):
        if not is_to_run(module_file):
            continue
        base = module_file.replace('func_', '').replace('.py', '')
        dependancies = get_tests_info(base, '.py')
        
        class LintTestUsingFileTC(RLintTestUsingFile):
            module = module_file.replace('.py', '')
            output = exists(messages_file + '2') and (messages_file + '2') or messages_file
            depends = dependancies or None
        tests.append(LintTestUsingFileTC)
    
    if not filter_rgx:
        # test all features are tested :)    
        tests.append(TestTests)

    return tests

FILTER_RGX = None
MODULES_ONLY = False

def suite():
    return unittest.TestSuite([unittest.makeSuite(test)
                               for test in make_tests(FILTER_RGX)])

if __name__=='__main__':
    if '-m' in sys.argv:
        MODULES_ONLY = True
        sys.argv.remove('-m')
    
    if len(sys.argv) > 1:            
        FILTER_RGX = sys.argv[1]
        del sys.argv[1]
    testlib.unittest_main(defaultTest='suite')


