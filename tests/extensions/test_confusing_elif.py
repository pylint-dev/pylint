# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Tests for the pylint checker in :mod:`pylint.extensions.confusing_elif
"""

import astroid

from pylint.extensions.confusing_elif import ConfusingConsecutiveElifChecker
from pylint.testutils import CheckerTestCase

MSG_ID_CONFUSING_CONSECUTIVE_ELIF = "confusing-consecutive-elif"


class TestConfusingConsecutiveElifChecker(CheckerTestCase):
    """Tests for pylint.extensions.confusing_elif.ConfusingConsecutiveElifChecker"""

    CHECKER_CLASS = ConfusingConsecutiveElifChecker

    def test_not_triggered_if_outer_block_does_not_have_elif(self) -> None:
        """
        Given an if construct without an elif
        When the body of the if ends with an if
        Then no message shall be triggered.
        """
        example_code = """
        def foo(a, b, c):
            result = None
            if a > b: #@
                if a > 0:
                    result = a
                elif a < 0:
                    result = 0
            else:
                result = c
            return result
        """
        if_node_to_test = astroid.extract_node(example_code)
        with self.assertNoMessages():
            self.checker.visit_if(if_node_to_test)

    def test_not_triggered_if_outer_block_continues_with_if(self) -> None:
        """
        Given an if construct which continues with a new if construct
        When the body of the first if ends with an if expression
        Then no message shall be triggered.
        """
        example_code = """
        def foo(a, b, c):
            result = None
            if a > b: #@
                if a > 0:
                    result = a
                elif a < 0:
                    result = 0
            if b > c:
                result = c
            return result
        """
        if_node_to_test = astroid.extract_node(example_code)
        with self.assertNoMessages():
            self.checker.visit_if(if_node_to_test)
