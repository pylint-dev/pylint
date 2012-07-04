# Copyright (c) 2003-2008 LOGILAB S.A. (Paris, FRANCE).
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
"""functional/non regression tests for pylint"""

import unittest
import sys
import re

from os import getcwd
from os.path import abspath, dirname, join

from logilab.common import testlib

from pylint.testutils import (make_tests, LintTestUsingModule, LintTestUsingFile,
    cb_test_gen, linter, test_reporter)

PY26 = sys.version_info >= (2, 6)
PY3K = sys.version_info >= (3, 0)

# Configure paths
INPUT_DIR = join(dirname(abspath(__file__)), 'input')
MSG_DIR = join(dirname(abspath(__file__)), 'messages')

# Classes

class LintTestNonExistentModuleTC(LintTestUsingModule):
    module = 'nonexistent'
    _get_expected = lambda self: 'F:  1: No module named nonexistent\n'
    tags = testlib.Tags(('generated','pylint_input_%s' % module))

class LintTestNonExistentFileTC(LintTestUsingFile):
    module = join(INPUT_DIR, 'nonexistent.py')
    _get_expected = lambda self: 'F:  1: No module named %s\n' % self.module[len(getcwd())+1 :]
    tags = testlib.Tags(('generated', 'pylint_input_%s' % module))
    def test_functionality(self):
        self._test([self.module])

class TestTests(testlib.TestCase):
    """check that all testable messages have been checked"""
    @testlib.tag('coverage')
    def test_exhaustivity(self):
        # skip fatal messages
        todo = [msgid for msgid in linter._messages if msgid[0] != 'F']
        for msgid in test_reporter.message_ids:
            try:
                todo.remove(msgid)
            except ValueError:
                continue
        todo.sort()
        if PY3K:
            rest = ['E1122', 'I0001',
                    # deprecated exec statement removed from py3k :
                    'W0122',
                    # XXX : no use case for now :
                    'W0402', # deprecated module
                    'W0403', # implicit relative import
                    'W0410', # __future__ import not first statement
                    ]
            self.assertEqual(todo, rest)
        elif PY26:
            self.assertEqual(todo, ['E1122', 'I0001'])
        else:
            self.assertEqual(todo, ['I0001'])

class LintBuiltinModuleTest(LintTestUsingModule):
    output = join(MSG_DIR, 'builtin_module.txt')
    module = 'sys'
    def test_functionality(self):
        self._test(['sys'])

# Callbacks

base_cb_file = cb_test_gen(LintTestUsingFile)

def cb_file(*args):
    if MODULES_ONLY:
        return None
    else:
        return base_cb_file(*args)

callbacks = [cb_test_gen(LintTestUsingModule),
    cb_file]

# Gen tests

def gen_tests(filter_rgx):
    tests = make_tests(INPUT_DIR, MSG_DIR, filter_rgx, callbacks)

    if filter_rgx:
        is_to_run = re.compile(filter_rgx).search
    else:
        is_to_run = lambda x: 1

    if is_to_run('nonexistent'):
        tests.append(LintTestNonExistentModuleTC)
        if not MODULES_ONLY:
            tests.append(LintTestNonExistentFileTC)

    tests.append(LintBuiltinModuleTest)

    if not filter_rgx:
        # test all features are tested :)
        tests.append(TestTests)

    return tests

# Create suite

FILTER_RGX = None
MODULES_ONLY = False

def suite():
    return testlib.TestSuite([unittest.makeSuite(test, suiteClass=testlib.TestSuite)
                              for test in gen_tests(FILTER_RGX)])

if __name__=='__main__':
    if '-m' in sys.argv:
        MODULES_ONLY = True
        sys.argv.remove('-m')

    if len(sys.argv) > 1:
        FILTER_RGX = sys.argv[1]
        del sys.argv[1]
    testlib.unittest_main(defaultTest='suite')
