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
import new
from os import linesep
from os.path import exists

from logilab.common import testlib

from utils import get_tests_info, fix_path, TestReporter

from logilab.astng import MANAGER
from pylint.lint import PyLinter
from pylint import checkers

test_reporter = TestReporter()
linter = PyLinter()
linter.set_reporter(test_reporter)
linter.config.persistent = 0
checkers.initialize(linter)
linter.global_set_option('required-attributes', ('__revision__',))

PY23 = sys.version_info >= (2, 3)
PY24 = sys.version_info >= (2, 4)
PY25 = sys.version_info >= (2, 5)


if linesep != '\n':
    LINE_RGX = re.compile(linesep)
    def ulines(string):
        return LINE_RGX.sub('\n', string)
else:
    def ulines(string):
        return string

INFO_TEST_RGX = re.compile('^func_i\d\d\d\d$')

def exception_str(ex):
    """function used to replace default __str__ method of exception instances"""
    return 'in %s\n:: %s' % (ex.file, ', '.join(ex.args))

class LintTestUsingModule(testlib.TestCase):            
    DEFAULT_PACKAGE = 'input'
    package = DEFAULT_PACKAGE
    linter = linter
    module = None
    depends = None

    _TEST_TYPE = 'module'

    def shortDescription(self):
        values = { 'mode' : self._TEST_TYPE,
                   'input': self.module,
                   'pkg':   self.package,
                   'cls':   self.__class__.__name__}

        if self.package == self.DEFAULT_PACKAGE:
            msg = '%(mode)s test of input file "%(input)s" (%(cls)s)'
        else:
            msg = '%(mode)s test of input file "%(input)s" in "%(pkg)s" (%(cls)s)'
        return msg % values

    def test_functionality(self):
        tocheck = [self.package+'.'+self.module]
        if self.depends:
            tocheck += [self.package+'.%s' % name.replace('.py', '')
                        for name, file in self.depends]
        self._test(tocheck)
        
    def _test(self, tocheck):
        if INFO_TEST_RGX.match(self.module):
            self.linter.enable_message_category('I')
        else:
            self.linter.disable_message_category('I')
        try:
            self.linter.check(tocheck)
        except Exception, ex:
            # need finalization to restore a correct state
            self.linter.reporter.finalize()
            ex.file = tocheck
            ex.__str__ = new.instancemethod(exception_str, ex, None)
            raise
        if self.module.startswith('func_noerror_'):
            expected = ''
        else:
            output = open(self.output)
            expected = output.read().strip()
            output.close()
        got = self.linter.reporter.finalize().strip()
        try:
            self.assertLinesEquals(got, expected)
        except Exception, ex:
            # doesn't work with py 2.5
            #ex.file = tocheck
            #ex.__str__ = new.instancemethod(exception_str, ex, None)
            raise AssertionError('%s: %s' % (self.module, ex)), None, sys.exc_info()[-1]

class LintTestUsingFile(LintTestUsingModule):            
                
    _TEST_TYPE = 'file'

    def test_functionality(self):
        tocheck = [self.package+'/' + self.module + '.py']
        if self.depends:
            tocheck += [self.package+'/%s' % name for name, file in self.depends]
        self._test(tocheck)


class TestTests(testlib.TestCase):
    """check that all testable messages have been checked"""
    @testlib.tag('coverage')
    def test_exhaustivity(self):
        # skip fatal messages
        todo = [msgid for msgid in linter._messages.keys() if msgid[0] != 'F']
        for msgid in test_reporter.message_ids.keys():
            try:
                todo.remove(msgid)
            except ValueError:
                continue
        todo.sort()
        if PY25:
            self.assertEqual(todo, ['E0503', 'I0001'])
        elif PY23:
            self.assertEqual(todo, ['E0503', 'I0001'])
        else: # python < 2.3
            self.assertEqual(todo, ['I0001'])

#bycat = {}
#for msgid in linter._messages.keys():
#    bycat[msgid[0]] = bycat.setdefault(msgid[0], 0) + 1
#for cat, val in bycat.items():
#    print '%s: %s' % (cat, val)
#print 'total', sum(bycat.values())
#
# on 2007/02/17:
#
# W: 48
# E: 42
# R: 15
# C: 13
# F: 7
# I: 5
# total 130

def make_tests(filter_rgx):
    """generate tests classes from test info
    
    return the list of generated test classes
    """
    if filter_rgx:
        is_to_run = re.compile(filter_rgx).search
    else:
        is_to_run = lambda x: 1
    tests = []
    for module_file, messages_file in get_tests_info('func_', '.py') + [('nonexistant', 'messages/nonexistant.txt')]:
        # skip those tests with python >= 2.3 since py2.3 detects them by itself
        if PY23 and module_file == "func_unknown_encoding.py": #"func_nonascii_noencoding.py"):
            continue
        pyrestr = module_file.rsplit('_py', 1)[-1][:-3]
        if pyrestr.isdigit(): # '24', '25'...
            if sys.version_info < tuple([int(i) for i in pyrestr]):
                continue
        if not is_to_run(module_file):
            continue
        base = module_file.replace('func_', '').replace('.py', '')
        dependencies = get_tests_info(base, '.py')
        
        class LintTestUsingModuleTC(LintTestUsingModule):
            module = module_file.replace('.py', '')
            output = messages_file
            depends = dependencies or None
            tags = testlib.Tags(('generated','pylint_input_%s' % module))
        tests.append(LintTestUsingModuleTC)

        if MODULES_ONLY:
            continue
        
        class LintTestUsingFileTC(LintTestUsingFile):
            module = module_file.replace('.py', '')
            output = exists(messages_file + '2') and (messages_file + '2') or messages_file
            depends = dependencies or None
            tags = testlib.Tags(('generated', 'pylint_input_%s' % module))
        tests.append(LintTestUsingFileTC)
        
##     # special test for f0003
##     module_file, messages_file in get_tests_info('func_f0003', '.pyc')
##     class LintTestSubclass(LintTest):
##         module = module_file.replace('.pyc', '')
##         output = messages_file
##         depends = dependencies or None
##     tests.append(LintTestSubclass)
            
    class LintBuiltinModuleTest(LintTestUsingModule):
        output = 'messages/builtin_module.txt'
        module = 'sys'
        def test_functionality(self):
            self._test(['sys'])
    tests.append(LintBuiltinModuleTest)
    
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


