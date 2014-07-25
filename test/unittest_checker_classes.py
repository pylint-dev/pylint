"""Unit tests for the variables checker."""
from __future__ import with_statement

from astroid import test_utils
from pylint.checkers import classes
from pylint.testutils import CheckerTestCase, Message

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
