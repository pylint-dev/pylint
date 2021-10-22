"""Tests for the pylint checker in :mod:`pylint.extensions.for_any_all
"""

import astroid

from pylint.extensions.for_any_all import ForAnyAllChecker
from pylint.testutils import CheckerTestCase, MessageTest


class TestForAnyAll(CheckerTestCase):

    CHECKER_CLASS = ForAnyAllChecker

    def test_basic_emit_for_any_all(self) -> None:
        """Simple case where we expect the message to be emitted."""
        node = astroid.extract_node(
            """
        def is_from_decorator(node):
            for parent in node.node_ancestors():
                if isinstance(parent, Decorators):
                    return True
            return False
        """
        ).body[0]

        with self.assertAddsMessages(MessageTest("consider-using-any-all", node=node)):
            self.checker.visit_for(node)

    def test_non_conditional_for(self) -> None:
        """Do not emit if there is no If condition in the for loop."""
        node = astroid.extract_node(
            """
        def print_items(items):
            for item in items:
                print(item)
            return True
        """
        ).body[0]

        with self.assertNoMessages():
            self.checker.visit_for(node)

    def test_returns_something_else(self) -> None:
        """Do not emit if anything besides a boolean is returned."""
        node = astroid.extract_node(
            """
        def print_items(items):
            for item in items:
                return items
            return True

        def print_items(items):
            for item in items:
                return False
            return items
        """
        ).body[0]

        with self.assertNoMessages():
            self.checker.visit_for(node)

    def test_additional_statements(self) -> None:
        """Do not emit if there is more logic which can cause side effects
        or become less readable in a list comprehension.
        """
        node = astroid.extract_node(
            """
        def print_items(items):
            for item in items:
                if isinstance(item, str):
                    print(item)
                    return False
            return True
        """
        ).body[0]

        with self.assertNoMessages():
            self.checker.visit_for(node)

    def test_for_if_else(self) -> None:
        """Do not emit if the if has an else condition. Generally implies more complicated logic."""
        node = astroid.extract_node(
            """
        def is_from_decorator(node):
            for parent in node.node_ancestors():
                if isinstance(parent, Decorators):
                    return True
                else:
                    if parent in Annotations.selected_annotations:
                        return False

            return False
        """
        ).body[0]

        with self.assertNoMessages():
            self.checker.visit_for(node)
