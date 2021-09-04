"""Tests for the pylint checker in :mod:`pylint.extensions.while
"""

import astroid

from pylint.extensions.while_used import WhileChecker
from pylint.testutils import CheckerTestCase, Message


class TestWhileUsed(CheckerTestCase):

    CHECKER_CLASS = WhileChecker

    def test_while_used(self) -> None:
        node = astroid.extract_node(
            """
        def f():
            i = 0
            while i < 10:
                i += 1
        """
        ).body[1]

        with self.assertAddsMessages(Message("while-used", node=node)):
            self.checker.visit_while(node)
