# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Unittest for the function-redefined."""

import re

import astroid

from pylint.checkers.base.basic_error_checker import BasicErrorChecker
from pylint.testutils import CheckerTestCase, MessageTest


class TestBasicErrorCheckerRedef(CheckerTestCase):
    CHECKER_CLASS = BasicErrorChecker  # Assign the checker

    def test_function_redefined_with_leading_underscore(self) -> None:
        # Use two separate code snippets for two functions

        self.checker.linter.config.dummy_variables_rgx = re.compile(
            r"_$"
        )  # or any regex pattern

        code = """
def _my_func():  #@
    return 1

def _my_func():  #@
    return 2
"""

        # Extract each function node separately
        nodes = astroid.extract_node(code)
        func1, func2 = nodes

        # Assert that 'function-redefined' message is triggered for second function
        with self.assertAddsMessages(
            MessageTest(
                msg_id="function-redefined",
                node=func2,
                args=("function", func1.fromlineno),
            ),
            ignore_position=True,
        ):
            # Visit both function definitions
            self.checker.visit_functiondef(func1)
            self.checker.visit_functiondef(func2)
