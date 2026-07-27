# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Unittest for the base checker."""

import unittest

import astroid

from pylint.checkers.base.comparison_checker import ComparisonChecker
from pylint.testutils import CheckerTestCase, MessageTest


class TestNoSix(unittest.TestCase):
    @unittest.skip("too many dependencies need six :(")
    def test_no_six(self) -> None:
        try:
            has_six = True
        except ImportError:
            has_six = False

        self.assertFalse(has_six, "pylint must be able to run without six")


class TestComparisonChecker(CheckerTestCase):
    CHECKER_CLASS = ComparisonChecker

    def test_attribute_comparison_with_itself(self) -> None:
        node = astroid.extract_node("obj.child.value != obj.child.value")

        with self.assertAddsMessages(
            MessageTest(
                "comparison-with-itself",
                node=node,
                args=("obj.child.value != obj.child.value",),
            ),
            ignore_position=True,
        ):
            self.checker.visit_compare(node)

    def test_non_identical_attribute_comparisons(self) -> None:
        expressions = (
            "obj.left == obj.right",
            "left.value == right.value",
            "factory().value == factory().value",
        )

        for expression in expressions:
            node = astroid.extract_node(expression)
            with self.assertNoMessages():
                self.checker.visit_compare(node)
