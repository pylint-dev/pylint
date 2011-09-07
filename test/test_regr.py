# Copyright (c) 2005 LOGILAB S.A. (Paris, FRANCE).
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
"""non regression tests for pylint, which requires a too specific configuration
to be incorporated in the automatic functional test framework
"""

import sys
import os
from os.path import abspath, dirname, join

from logilab.common.testlib import TestCase, unittest_main

from utils import TestReporter

from pylint.lint import PyLinter
from pylint import checkers

test_reporter = TestReporter()
linter = PyLinter()
linter.set_reporter(test_reporter)
linter.disable('I')
linter.config.persistent = 0
checkers.initialize(linter)

REGR_DATA = join(dirname(abspath(__file__)), 'regrtest_data')
sys.path.insert(1, REGR_DATA)

class NonRegrTC(TestCase):
    def setUp(self):
        """call reporter.finalize() to cleanup
        pending messages if a test finished badly
        """
        linter.reporter.finalize()

    def test_package___path___manipulation(self):
        linter.check('package.__init__')
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, '')

    def test_package___init___precedence(self):
        linter.check('precedence_test')
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, '')

    def test_check_package___init__(self):
        for variation in ('package.__init__', join(REGR_DATA, 'package', '__init__.py')):
            linter.check(variation)
            got = linter.reporter.finalize().strip()
            checked = linter.stats['by_module'].keys()
            self.failUnlessEqual(checked, ['package.__init__'],
                                 '%s: %s' % (variation, checked))
        cwd = os.getcwd()
        os.chdir(join(REGR_DATA, 'package'))
        sys.path.insert(0, '')
        try:
            for variation in ('__init__', '__init__.py'):
                linter.check(variation)
                got = linter.reporter.finalize().strip()
                checked = linter.stats['by_module'].keys()
                self.failUnlessEqual(checked, ['__init__'],
                                 '%s: %s' % (variation, checked))
        finally:
            sys.path.pop(0)
            os.chdir(cwd)

    def test_gtk_import(self):
        try:
            import gtk
        except ImportError:
            self.skipTest('test skipped: gtk is not available')
        except RuntimeError: # RuntimeError when missing display
            self.skipTest('no display, can\'t run this test')
        linter.check(join(REGR_DATA, 'pygtk_import.py'))
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, '')

    def test_numarray_inference(self):
        try:
            from numarray import random_array
        except ImportError:
            self.skipTest('test skipped: numarray.random_array is not available')
        linter.check(join(REGR_DATA, 'numarray_inf.py'))
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, "E:  5: Instance of 'int' has no 'astype' member (but some types could not be inferred)")

    def test_numarray_import(self):
        try:
            import numarray
        except ImportError:
            self.skipTest('test skipped: numarray is not available')
        linter.check(join(REGR_DATA, 'numarray_import.py'))
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, '')

    def test_socketerror_import(self):
        linter.check(join(REGR_DATA, 'socketerror_import.py'))
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, '')

    def test_class__doc__usage(self):
        linter.check(join(REGR_DATA, 'classdoc_usage.py'))
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, '')

    def test_package_import_relative_subpackage_no_attribute_error(self):
        linter.check('import_package_subpackage_module')
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, '')

    def test_import_assign_crash(self):
        linter.check(join(REGR_DATA, 'import_assign.py'))

    def test_special_attr_scope_lookup_crash(self):
        linter.check(join(REGR_DATA, 'special_attr_scope_lookup_crash.py'))

    def test_module_global_crash(self):
        linter.check(join(REGR_DATA, 'module_global.py'))
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, '')

    def test_decimal_inference(self):
        linter.check(join(REGR_DATA, 'decimal_inference.py'))
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, "")

    def test_descriptor_crash(self):
        for fname in os.listdir(REGR_DATA):
            if fname.endswith('_crash.py'):
                linter.check(join(REGR_DATA, fname))
                linter.reporter.finalize().strip()

    def test_try_finally_disable_msg_crash(self):
        linter.check(join(REGR_DATA, 'try_finally_disable_msg_crash'))

    def test___path__(self):
        linter.check('pylint.checkers.__init__')
        messages = linter.reporter.finalize().strip()
        self.failIf('__path__' in messages, messages)

    def test_absolute_import(self):
        linter.check(join(REGR_DATA, 'absimp', 'string.py'))
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, "W:  6: Uses of a deprecated module 'string'")

if __name__ == '__main__':
    unittest_main()
