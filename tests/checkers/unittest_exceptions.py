# Copyright (c) 2015-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Rene Zhang <rz99@cornell.edu>
# Copyright (c) 2015 Steven Myint <hg@stevenmyint.com>
# Copyright (c) 2015 Pavel Roskin <proski@gnu.org>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Brian Shaginaw <brian.shaginaw@warbyparker.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Tests for pylint.checkers.exceptions."""
import astroid

from pylint.checkers import exceptions
from pylint.testutils import CheckerTestCase, TestMessage


class TestExceptionsChecker(CheckerTestCase):
    """Tests for pylint.checkers.exceptions."""

    CHECKER_CLASS = exceptions.ExceptionsChecker

    # These tests aren't in the functional test suite,
    # since they will be converted with 2to3 for Python 3
    # and `raise (Error, ...)` will be converted to
    # `raise Error(...)`, so it beats the purpose of the test.

    def test_raising_bad_type_python3(self) -> None:
        node = astroid.extract_node("raise (ZeroDivisionError, None)  #@")
        message = TestMessage("raising-bad-type", node=node, args="tuple")
        with self.assertAddsMessages(message):
            self.checker.visit_raise(node)

    def test_bad_exception_context_function(self) -> None:
        node = astroid.extract_node(
            """
        def function():
            pass

        try:
            pass
        except function as exc:
            raise Exception from exc  #@
        """
        )
        message = TestMessage("bad-exception-context", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_raise(node)
