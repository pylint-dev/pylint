"""Unittest for the type checker."""
import unittest

from astroid import test_utils
from pylint.checkers import typecheck
from pylint.testutils import CheckerTestCase, Message, set_config

class TypeCheckerTest(CheckerTestCase):
    "Tests for pylint.checkers.typecheck"
    CHECKER_CLASS = typecheck.TypeChecker

    def test_no_member_in_getattr(self):
        """Make sure that a module attribute access is checked by pylint.
        """

        node = test_utils.extract_node("""
        import optparse
        optparse.THIS_does_not_EXIST 
        """)
        with self.assertAddsMessages(
                Message(
                    'no-member',
                    node=node,
                    args=('Module', 'optparse', 'THIS_does_not_EXIST'))):
            self.checker.visit_getattr(node)

    @set_config(ignored_modules=('argparse',))
    def test_no_member_in_getattr_ignored(self):
        """Make sure that a module attribute access check is omitted with a
        module that is configured to be ignored.
        """

        node = test_utils.extract_node("""
        import argparse
        argparse.THIS_does_not_EXIST
        """)
        with self.assertNoMessages():
            self.checker.visit_getattr(node)


if __name__ == '__main__':
    unittest.main()
