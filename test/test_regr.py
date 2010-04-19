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
from os.path import abspath, join

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

sys.path.insert(1, abspath('regrtest_data'))

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
        for variation in ('package.__init__', 'regrtest_data/package/__init__.py'):
            linter.check(variation)
            got = linter.reporter.finalize().strip()
            checked = linter.stats['by_module'].keys()
            self.failUnlessEqual(checked, ['package.__init__'],
                                 '%s: %s' % (variation, checked))
        cwd = os.getcwd()
        os.chdir('regrtest_data/package')
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
            self.skip('test skipped: gtk is not available')
        except RuntimeError: # RuntimeError when missing display
            self.skip('no display, can\'t run this test')
        linter.check('regrtest_data/pygtk_import.py')
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, '')

    def test_numarray_inference(self):
        try:
            from numarray import random_array
        except ImportError:
            self.skip('test skipped: numarray.random_array is not available')
        linter.check('regrtest_data/numarray_inf.py')
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, "E:  5: Instance of 'int' has no 'astype' member (but some types could not be inferred)")

    def test_numarray_import(self):
        try:
            import numarray
        except ImportError:
            self.skip('test skipped: numarray is not available')
        linter.check('regrtest_data/numarray_import.py')
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, '')

    def test_socketerror_import(self):
        linter.check('regrtest_data/socketerror_import.py')
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, '')

    def test_class__doc__usage(self):
        linter.check('regrtest_data/classdoc_usage.py')
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, '')

    def test_package_import_relative_subpackage_no_attribute_error(self):
        linter.check('import_package_subpackage_module')
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, '')

    def test_module_global_crash(self):
        linter.check('regrtest_data/module_global.py')
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, '')

    def test_decimal_inference(self):
        linter.check('regrtest_data/decimal_inference.py')
        got = linter.reporter.finalize().strip()
        self.failUnlessEqual(got, "")

    def test_descriptor_crash(self):
        for fname in os.listdir('regrtest_data'):
            if fname.endswith('_crash.py'):
                linter.check(join('regrtest_data', fname))
                linter.reporter.finalize().strip()

    def test_try_finally_disable_msg_crash(self):
        linter.check(join('regrtest_data', 'try_finally_disable_msg_crash'))


    def test___path__(self):
        linter.check('pylint.checkers.__init__')
        messages = linter.reporter.finalize().strip()
        self.failIf('__path__' in messages, messages)


if __name__ == '__main__':
    unittest_main()
