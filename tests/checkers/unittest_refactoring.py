# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import os

import astroid
import pytest
from astroid import nodes

from pylint.checkers.refactoring.recommendation_checker import RecommendationChecker
from pylint.reporters.text import TextReporter
from pylint.testutils import CheckerTestCase
from pylint.testutils._run import _Run as Run

PARENT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
REGR_DATA = os.path.join(PARENT_DIR, "regrtest_data")


@pytest.mark.timeout(8)
def test_process_tokens() -> None:
    with pytest.raises(SystemExit) as cm:
        Run(
            [os.path.join(REGR_DATA, "very_long_line.py"), "--disable=C"],
            reporter=TextReporter(),
        )
    assert cm.value.code == 0


@pytest.mark.timeout(60)
def test_issue_5724() -> None:
    """Regression test for parsing of pylint disable pragma's."""
    with pytest.raises(SystemExit) as cm:
        Run(
            [
                os.path.join(REGR_DATA, "issue_5724.py"),
                "--enable=missing-final-newline",
                "--disable=C",
            ],
            reporter=TextReporter(),
        )
    assert cm.value.code == 0


class TestConsiderUsingDictItems(CheckerTestCase):
    """Non-name loop targets must not crash ``consider-using-dict-items``.

    The ``other[index]`` subscript in each body is required to reach the code
    path that crashed: the checker only inspects bodies that subscript a name.
    https://github.com/pylint-dev/pylint/issues/11173
    """

    CHECKER_CLASS = RecommendationChecker

    def test_attribute_target_does_not_crash(self) -> None:
        node = astroid.extract_node("""
        D = {"a": 1}
        def run(obj, other, index):
            for obj.key in D:  #@
                print(other[index])
        """)
        with self.assertNoMessages():
            self.checker.visit_for(node)

    def test_subscript_target_does_not_crash(self) -> None:
        node = astroid.extract_node("""
        D = {"a": 1}
        def run(target, other, index):
            for target[0] in D:  #@
                print(other[index])
        """)
        with self.assertNoMessages():
            self.checker.visit_for(node)

    def test_comprehension_attribute_target_does_not_crash(self) -> None:
        node = astroid.extract_node("""
        D = {"a": 1}
        def run(obj, other, index):
            return [other[index] for obj.key in D]  #@
        """)
        comprehension = next(node.nodes_of_class(nodes.Comprehension))
        with self.assertNoMessages():
            self.checker.visit_comprehension(comprehension)
