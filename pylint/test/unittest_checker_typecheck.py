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
            self.checker.visit_attribute(node)

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
            self.checker.visit_attribute(node)

    @set_config(ignored_classes=('xml.etree.', ))
    def test_ignored_modules_invalid_pattern(self):
        node = test_utils.extract_node('''
        import xml
        xml.etree.Lala
        ''')
        message = Message('no-member', node=node,
                          args=('Module', 'xml.etree', 'Lala'))
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    @set_config(ignored_modules=('xml.etree*', ))
    def test_ignored_modules_patterns(self):
        node = test_utils.extract_node('''
        import xml
        xml.etree.portocola #@
        ''')
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    @set_config(ignored_classes=('xml.*', ))
    def test_ignored_classes_no_recursive_pattern(self):
        node = test_utils.extract_node('''
        import xml
        xml.etree.ElementTree.Test
        ''')
        message = Message('no-member', node=node,
                          args=('Module', 'xml.etree.ElementTree', 'Test'))
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    @set_config(ignored_classes=('optparse.Values', ))
    def test_ignored_classes_qualified_name(self):
        """Test that ignored-classes supports qualified name for ignoring."""
        node = test_utils.extract_node('''
        import optparse
        optparse.Values.lala
        ''')
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    @set_config(ignored_classes=('Values', ))
    def test_ignored_classes_only_name(self):
        """Test that ignored_classes works with the name only."""
        node = test_utils.extract_node('''
        import optparse
        optparse.Values.lala
        ''')
        with self.assertNoMessages():
            self.checker.visit_attribute(node)


if __name__ == '__main__':
    unittest.main()
