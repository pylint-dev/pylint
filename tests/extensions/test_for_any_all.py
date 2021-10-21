"""Tests for the pylint checker in :mod:`pylint.extensions.for_any_all
"""

import astroid

from pylint.extensions.for_any_all import ForAnyAllChecker
from pylint.testutils import CheckerTestCase, MessageTest


class TestForAnyAll(CheckerTestCase):

    CHECKER_CLASS = ForAnyAllChecker

    def test_for_any_all(self) -> None:
        node = astroid.extract_node(
            """
        def is_from_decorator(node):
            for parent in node.node_ancestors():
                if isinstance(parent, Decorators):
                    return True
            return False
        """
        ).body[0]

        with self.assertAddsMessages(MessageTest("for-any-all", node=node)):
            self.checker.visit_for(node)
