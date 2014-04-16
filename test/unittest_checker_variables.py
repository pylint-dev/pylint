"""Unit tests for the variables checker."""

from astroid import test_utils
from pylint.checkers import variables
from pylint.testutils import CheckerTestCase

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
