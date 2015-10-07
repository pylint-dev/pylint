"""Unittest for the type checker."""
import unittest
import sys

from astroid import test_utils
from pylint.checkers import typecheck
from pylint.testutils import CheckerTestCase, Message, set_config


def python33_and_newer(test):
    """
    Decorator for any tests that will fail if launched not with Python 3.3+.
    """
    return unittest.skipIf(sys.version_info < (3, 3),
                           'Python 3.2 and older')(test)

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

class IterableTest(CheckerTestCase):
    CHECKER_CLASS = typecheck.IterableChecker

    def test_non_iterable_in_for(self):
        node = test_utils.extract_node("""
        for i in 42:
            print(i)
        """)
        message = Message('not-an-iterable', node=node, args='42')
        with self.assertAddsMessages(message):
            self.checker.visit_for(node)

        node = test_utils.extract_node("""
        for i in [1,2,3]:
            print(i)
        """)
        with self.assertNoMessages():
            self.checker.visit_for(node)

        node = test_utils.extract_node("""
        def count():
            i = 0
            while True:
                yield i
                i += 1

        for i in count():
            print(i)
        """)
        with self.assertNoMessages():
            self.walk(node.root())

        node = test_utils.extract_node("""
        for i in "aeiou":
            print(i)
        """)
        with self.assertNoMessages():
            self.checker.visit_for(node)

    @python33_and_newer
    def test_non_iterable_in_yield_from(self):
        node = test_utils.extract_node("""
        yield from 42
        """)
        message = Message('not-an-iterable', node=node, args='42')
        with self.assertAddsMessages(message):
            self.checker.visit_yieldfrom(node)

        node = test_utils.extract_node("""
        yield from [1,2,3]
        """)
        with self.assertNoMessages():
            self.checker.visit_yieldfrom(node)

    def test_non_iterable_in_funcall_starargs(self):
        node = test_utils.extract_node("""
        foo(*123)
        """)
        message = Message('not-an-iterable', node=node, args='123')
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

        node = test_utils.extract_node("""
        stuff = [1,2,3]
        foo(*stuff)
        """)
        with self.assertNoMessages():
            self.walk(node.root())

    def test_non_mapping_in_funcall_kwargs(self):
        node = test_utils.extract_node("""
        foo(**123)
        """)
        message = Message('not-a-mapping', node=node, args='123')
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

        node = test_utils.extract_node("""
        foo(**retdict())
        """)
        with self.assertNoMessages():
            self.walk(node.root())

    def test_non_iterable_in_listcomp(self):
        node = test_utils.extract_node("""
        [x ** 2 for x in 10]
        """)
        message = Message('not-an-iterable', node=node, args='10')
        with self.assertAddsMessages(message):
            self.checker.visit_listcomp(node)

        node = test_utils.extract_node("""
        [x ** 2 for x in range(10)]
        """)
        with self.assertNoMessages():
            self.checker.visit_listcomp(node)

    def test_non_iterable_in_dictcomp(self):
        node = test_utils.extract_node("""
        {x: chr(x) for x in 256}
        """)
        message = Message('not-an-iterable', node=node, args='256')
        with self.assertAddsMessages(message):
            self.checker.visit_dictcomp(node)

        node = test_utils.extract_node("""
        {ord(x): x for x in "aoeui"}
        """)
        with self.assertNoMessages():
            self.checker.visit_dictcomp(node)

    def test_non_iterable_in_setcomp(self):
        node = test_utils.extract_node("""
        {2 ** x for x in 10}
        """)
        message = Message('not-an-iterable', node=node, args='10')
        with self.assertAddsMessages(message):
            self.checker.visit_setcomp(node)

        node = test_utils.extract_node("""
        {2 ** x for x in range(10)}
        """)
        with self.assertNoMessages():
            self.checker.visit_setcomp(node)

    def test_non_iterable_in_generator(self):
        node = test_utils.extract_node("__(x for x in 123)")
        message = Message('not-an-iterable', node=node, args='123')
        with self.assertAddsMessages(message):
            self.walk(node.root())

        node = test_utils.extract_node("__(chr(x) for x in range(25))")
        with self.assertNoMessages():
            self.walk(node.root())


if __name__ == '__main__':
    unittest.main()
