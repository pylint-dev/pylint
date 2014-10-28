"""Unit tests for the variables checker."""
import unittest

from astroid import test_utils
from pylint.checkers import classes
from pylint.testutils import CheckerTestCase, Message, set_config

class VariablesCheckerTC(CheckerTestCase):

    CHECKER_CLASS = classes.ClassChecker

    def test_bitbucket_issue_164(self):
        """Issue 164 report a false negative for access-member-before-definition"""
        n1, n2 = test_utils.extract_node("""
        class MyClass1(object):
          def __init__(self):
            self.first += 5 #@
            self.first = 0  #@
        """)
        with self.assertAddsMessages(Message('access-member-before-definition',
                                             node=n1.target, args=('first', n2.lineno))):
            self.walk(n1.root())

    @set_config(exclude_protected=('_meta', '_manager'))
    def test_exclude_protected(self):
        """Test that exclude-protected can be used to
        exclude names from protected-access warning.
        """

        node = test_utils.build_module("""
        class Protected(object):
            '''empty'''
            def __init__(self):
                self._meta = 42
                self._manager = 24
                self._teta = 29
        OBJ = Protected()
        OBJ._meta
        OBJ._manager
        OBJ._teta
        """)
        with self.assertAddsMessages(
                Message('protected-access',
                        node=node.body[-1].value,
                        args='_teta')):
            self.walk(node.root())


if __name__ == '__main__':
    unittest.main()
