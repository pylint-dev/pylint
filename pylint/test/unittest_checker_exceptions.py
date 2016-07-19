# Copyright (c) 2003-2016 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for pylint.checkers.exceptions."""

import sys
import unittest

from astroid import test_utils
from pylint.checkers import exceptions
from pylint.testutils import CheckerTestCase, Message


class ExceptionsCheckerTest(CheckerTestCase):
    """Tests for pylint.checkers.exceptions."""

    CHECKER_CLASS = exceptions.ExceptionsChecker

    # These tests aren't in the functional test suite,
    # since they will be converted with 2to3 for Python 3
    # and `raise (Error, ...)` will be converted to
    # `raise Error(...)`, so it beats the purpose of the test.

    @unittest.skipUnless(sys.version_info[0] == 3,
                         "The test should emit an error on Python 3.")
    def test_raising_bad_type_python3(self):
        node = test_utils.extract_node('raise (ZeroDivisionError, None)  #@')
        message = Message('raising-bad-type', node=node, args='tuple')
        with self.assertAddsMessages(message):
            self.checker.visit_raise(node)

    @unittest.skipUnless(sys.version_info[0] == 2,
                         "The test is valid only on Python 2.")
    def test_raising_bad_type_python2(self):
        nodes = test_utils.extract_node('''
        raise (ZeroDivisionError, None)  #@
        from something import something
        raise (something, None) #@

        raise (4, None) #@
        raise () #@
        ''')
        with self.assertNoMessages():
            self.checker.visit_raise(nodes[0])
        with self.assertNoMessages():
            self.checker.visit_raise(nodes[1])

        message = Message('raising-bad-type', node=nodes[2], args='tuple')
        with self.assertAddsMessages(message):
            self.checker.visit_raise(nodes[2])
        message = Message('raising-bad-type', node=nodes[3], args='tuple')
        with self.assertAddsMessages(message):
            self.checker.visit_raise(nodes[3])


if __name__ == '__main__':
    unittest.main()
