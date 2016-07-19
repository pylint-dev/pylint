# Copyright (c) 2005-2016 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""non regression tests for pylint, which requires a too specific configuration
to be incorporated in the automatic functional test framework
"""

import sys
import platform
import os
from os.path import abspath, dirname, join
import unittest

from pylint.testutils import TestReporter
from pylint.lint import PyLinter
from pylint import checkers
from pylint import epylint

test_reporter = TestReporter()
linter = PyLinter()
linter.set_reporter(test_reporter)
linter.disable('I')
linter.config.persistent = 0
checkers.initialize(linter)

REGR_DATA = join(dirname(abspath(__file__)), 'regrtest_data')
sys.path.insert(1, REGR_DATA)

class NonRegrTC(unittest.TestCase):
    def setUp(self):
        """call reporter.finalize() to cleanup
        pending messages if a test finished badly
        """
        linter.reporter.finalize()

    def test_package___path___manipulation(self):
        linter.check('package.__init__')
        got = linter.reporter.finalize().strip()
        self.assertEqual(got, '')

    def test_package___init___precedence(self):
        linter.check('precedence_test')
        got = linter.reporter.finalize().strip()
        self.assertEqual(got, '')

    def test_check_package___init__(self):
        for variation in ('package.__init__', join(REGR_DATA, 'package', '__init__.py')):
            linter.check(variation)
            got = linter.reporter.finalize().strip()
            checked = list(linter.stats['by_module'].keys())
            self.assertEqual(checked, ['package.__init__'],
                             '%s: %s' % (variation, checked))
        cwd = os.getcwd()
        os.chdir(join(REGR_DATA, 'package'))
        sys.path.insert(0, '')
        try:
            for variation in ('__init__', '__init__.py'):
                linter.check(variation)
                got = linter.reporter.finalize().strip()
                checked = list(linter.stats['by_module'].keys())
                self.assertEqual(checked, ['__init__'],
                                 '%s: %s' % (variation, checked))
        finally:
            sys.path.pop(0)
            os.chdir(cwd)

    def test_numarray_inference(self):
        try:
            from numarray import random_array
        except ImportError:
            self.skipTest('test skipped: numarray.random_array is not available')
        linter.check(join(REGR_DATA, 'numarray_inf.py'))
        got = linter.reporter.finalize().strip()
        self.assertEqual(got, "E:  5: Instance of 'int' has no 'astype' member (but some types could not be inferred)")

    def test_numarray_import(self):
        try:
            import numarray
        except ImportError:
            self.skipTest('test skipped: numarray is not available')
        linter.check(join(REGR_DATA, 'numarray_import.py'))
        got = linter.reporter.finalize().strip()
        self.assertEqual(got, '')

    def test_class__doc__usage(self):
        linter.check(join(REGR_DATA, 'classdoc_usage.py'))
        got = linter.reporter.finalize().strip()
        self.assertEqual(got, '')

    def test_package_import_relative_subpackage_no_attribute_error(self):
        linter.check('import_package_subpackage_module')
        got = linter.reporter.finalize().strip()
        self.assertEqual(got, '')

    def test_import_assign_crash(self):
        linter.check(join(REGR_DATA, 'import_assign.py'))

    def test_special_attr_scope_lookup_crash(self):
        linter.check(join(REGR_DATA, 'special_attr_scope_lookup_crash.py'))

    def test_module_global_crash(self):
        linter.check(join(REGR_DATA, 'module_global.py'))
        got = linter.reporter.finalize().strip()
        self.assertEqual(got, '')

    def test_decimal_inference(self):
        linter.check(join(REGR_DATA, 'decimal_inference.py'))
        got = linter.reporter.finalize().strip()
        self.assertEqual(got, "")

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
        self.assertFalse('__path__' in messages, messages)

    def test_absolute_import(self):
        linter.check(join(REGR_DATA, 'absimp', 'string.py'))
        got = linter.reporter.finalize().strip()
        self.assertEqual(got, "")

    def test_no_context_file(self):
        expected = "Unused import missing"
        linter.check(join(REGR_DATA, 'bad_package'))
        got = linter.reporter.finalize().strip()
        self.assertIn(expected, got)

    def test_epylint_does_not_block_on_huge_files(self):
        path = join(REGR_DATA, 'huge.py')
        out, err = epylint.py_run(path, return_std=True)
        self.assertTrue(hasattr(out, 'read'))
        self.assertTrue(hasattr(err, 'read'))
        output = out.read(10)
        self.assertIsInstance(output, str)


if __name__ == '__main__':
    unittest.main()
