"""Unit tests for the variables checker."""
from __future__ import with_statement
import sys
import os

from astroid import test_utils
from pylint.checkers import variables
from pylint.testutils import CheckerTestCase, linter, set_config

class VariablesCheckerTC(CheckerTestCase):

    CHECKER_CLASS = variables.VariablesChecker

    def test_bitbucket_issue_78(self):
        """ Issue 78 report a false positive for unused-module """
        module = test_utils.build_module("""
        from sys import path
        path += ['stuff']
        def func():
            other = 1
            return len(other)
        """)
        with self.assertNoMessages():
            self.walk(module)

    @set_config(ignored_modules=('argparse',))
    def test_no_name_in_module_skipped(self):
        """Make sure that 'from ... import ...' does not emit a
        'no-name-in-module' with a module that is configured
        to be ignored.
        """

        node = test_utils.extract_node("""
        from argparse import THIS_does_not_EXIST
        """)
        with self.assertNoMessages():
            self.checker.visit_from(node)


class MissingSubmoduleTest(CheckerTestCase):
    CHECKER_CLASS = variables.VariablesChecker

    def test_package_all(self):
        regr_data = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'regrtest_data')
        sys.path.insert(0, regr_data)
        try:
            linter.check(os.path.join(regr_data, 'package_all'))
            got = linter.reporter.finalize().strip()
            self.assertEqual(got, "E:  3: Undefined variable name "
                                  "'missing' in __all__")
        finally:
            sys.path.pop(0)

if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
