# Copyright (c) 2015-2018 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Rene Zhang <rz99@cornell.edu>
# Copyright (c) 2015 Steven Myint <hg@stevenmyint.com>
# Copyright (c) 2015 Pavel Roskin <proski@gnu.org>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Brian Shaginaw <brian.shaginaw@warbyparker.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for pylint.checkers.exceptions."""
import astroid

from pylint.checkers import exceptions
from pylint.testutils import CheckerTestCase, Message


class TestExceptionsChecker(CheckerTestCase):
    """Tests for pylint.checkers.exceptions."""

    CHECKER_CLASS = exceptions.ExceptionsChecker

    # These tests aren't in the functional test suite,
    # since they will be converted with 2to3 for Python 3
    # and `raise (Error, ...)` will be converted to
    # `raise Error(...)`, so it beats the purpose of the test.

    def test_raising_bad_type_python3(self):
        node = astroid.extract_node('raise (ZeroDivisionError, None)  #@')
        message = Message('raising-bad-type', node=node, args='tuple')
        with self.assertAddsMessages(message):
            self.checker.visit_raise(node)

    def test_bad_exception_context_function(self):
        node = astroid.extract_node("""
        def function():
            pass

        try:
            pass
        except function as exc:
            raise Exception from exc  #@
        """)
        message = Message('bad-exception-context', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_raise(node)
