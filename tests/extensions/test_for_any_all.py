"""Tests for the pylint checker in :mod:`pylint.extensions.for_any_all
"""

import astroid

from pylint.extensions.for_any_all import ConsiderUsingAnyOrAllChecker
from pylint.testutils import CheckerTestCase, MessageTest


class TestForAnyAll(CheckerTestCase):

    CHECKER_CLASS = ConsiderUsingAnyOrAllChecker

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

        with self.assertAddsMessages(
            MessageTest(
                "consider-using-any-or-all",
                node=node,
                args="any(isinstance(parent, Decorators) for parent in node.node_ancestors())",
            )
        ):
            self.checker.visit_for(node)

    def test_emit_not_any_for_any_all(self) -> None:
        """Case where we expect the message to be emitted with a not any suggestion."""
        node = astroid.extract_node(
            """
        def is_from_decorator(node):
            for parent in node.node_ancestors():
                if isinstance(parent, Decorators):
                    return False
            return True
        """
        ).body[0]

        with self.assertAddsMessages(
            MessageTest(
                "consider-using-any-or-all",
                node=node,
                args="not any(isinstance(parent, Decorators) for parent in node.node_ancestors())",
            )
        ):
            self.checker.visit_for(node)

    def test_emit_not_any_boolop_for_any_all(self) -> None:
        """Case where we expect not any statement with a more complicated condition"""
        node = astroid.extract_node(
            """
        def is_from_decorator(items):
            for item in items:
                if item % 2 == 0 and (item % 3 == 0 or item > 15):
                    return False
            return True
        """
        ).body[0]

        with self.assertAddsMessages(
            MessageTest(
                "consider-using-any-or-all",
                node=node,
                args="not any(item % 2 == 0 and (item % 3 == 0 or item > 15) for item in items)",
            )
        ):
            self.checker.visit_for(node)

    def test_emit_long_message_for_any_all(self) -> None:
        """Case where we expect a particularly long message to be emitted."""
        node = astroid.extract_node(
            """
        def is_from_decorator(node):
            for ancestor in itertools.chain([node], ancestors):
                if (
                    ancestor.name in ("Exception", "BaseException")
                    and ancestor.root().name == EXCEPTIONS_MODULE
                ):
                    return True
            return False
        """
        ).body[0]

        with self.assertAddsMessages(
            MessageTest(
                "consider-using-any-or-all",
                node=node,
                args="any(ancestor.name in ('Exception', 'BaseException') and ancestor.root().name == EXCEPTIONS_MODULE for ancestor in itertools.chain([node], ancestors))",
            )
        ):
            self.checker.visit_for(node)

    def test_emit_all_for_any_all(self) -> None:
        """Case where we expect an all statement because of negation in the condition"""
        node = astroid.extract_node(
            """
        def is_from_decorator(items):
            for item in items:
                if not(item % 2 == 0 and (item % 3 == 0 or item > 15)):
                    return False
            return True
        """
        ).body[0]

        with self.assertAddsMessages(
            MessageTest(
                "consider-using-any-or-all",
                node=node,
                args="all(item % 2 == 0 and (item % 3 == 0 or item > 15) for item in items)",
            )
        ):
            self.checker.visit_for(node)

    def test_emit_not_all_for_any_all(self) -> None:
        """Case where we expect a not all statement because of negation in the condition"""
        node = astroid.extract_node(
            """
        def is_from_decorator(node):
            for ancestor in itertools.chain([node], ancestors):
                if not (
                    ancestor.name in ("Exception", "BaseException")
                    and ancestor.root().name == EXCEPTIONS_MODULE
                ):
                    return True
            return False
        """
        ).body[0]

        with self.assertAddsMessages(
            MessageTest(
                "consider-using-any-or-all",
                node=node,
                args="not all(ancestor.name in ('Exception', 'BaseException') and ancestor.root().name == EXCEPTIONS_MODULE for ancestor in itertools.chain([node], ancestors))",
            )
        ):
            self.checker.visit_for(node)

    def test_no_pattern(self) -> None:
        """Do not emit if the for loop does not have the pattern we are looking for"""
        node = astroid.extract_node(
            """
        def no_suggestion_if_not_if():
            for x in range(1):
                var = x
                return var
        """
        ).body[0]

        with self.assertNoMessages():
            self.checker.visit_for(node)

    def test_other_return(self) -> None:
        """Do not emit if the if-statement does not return a bool"""
        node = astroid.extract_node(
            """
        def no_suggestion_if_not_bool(item):
            for parent in item.parents():
                if isinstance(parent, str):
                    return "True"
            return "False"
        """
        ).body[0]

        with self.assertNoMessages():
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
