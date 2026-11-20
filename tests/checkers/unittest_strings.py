# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import astroid
import pytest

from pylint.checkers import strings
from pylint.interfaces import UNDEFINED
from pylint.testutils import CheckerTestCase, MessageTest

TEST_TOKENS = (
    '"X"',
    "'X'",
    "'''X'''",
    '"""X"""',
    'r"X"',
    "R'X'",
    'u"X"',
    "F'X'",
    'f"X"',
    "F'X'",
    'fr"X"',
    'Fr"X"',
    'fR"X"',
    'FR"X"',
    'rf"X"',
    'rF"X"',
    'Rf"X"',
    'RF"X"',
)


def test_str_eval() -> None:
    for token in TEST_TOKENS:
        assert strings.str_eval(token) == "X"


class TestStringFormatChecker(CheckerTestCase):
    """Argument counting of ``str.format`` with explicit positions."""

    CHECKER_CLASS = strings.StringFormatChecker

    @pytest.mark.parametrize(
        "code, message",
        [
            ('"{1}".format(20)', "too-few-format-args"),
            ('"{2}".format(20)', "too-few-format-args"),
            ('"{0} {2}".format(1, 2)', "too-few-format-args"),
            ('"{3} {0}".format(1, 2, 3)', "too-few-format-args"),
            ('"{1.real}".format(20)', "too-few-format-args"),
            ('"{1[0]}".format([1])', "too-few-format-args"),
            ('"{0:>{2}}".format(42, 24)', "too-few-format-args"),
            ('"{1} {a}".format(5, a=2)', "too-few-format-args"),
            ('"{0} {2}".format(1, 2, 3, 4)', "too-many-format-args"),
        ],
    )
    def test_explicit_positions_are_counted_by_highest_index(
        self, code: str, message: str
    ) -> None:
        node = astroid.extract_node(code)
        with self.assertAddsMessages(
            MessageTest(
                message,
                node=node,
                line=1,
                col_offset=0,
                end_line=1,
                end_col_offset=len(code),
                confidence=UNDEFINED,
            )
        ):
            self.checker.visit_call(node)

    @pytest.mark.parametrize(
        "code",
        [
            '"{0}".format(20)',
            '"{1}".format(20, 21)',
            '"{2} {0}".format(1, 2, 3)',
            '"{0} {1} {0}".format(1, 2)',
            '"{1.real}".format(20, 21)',
            '"{0:>{1}}".format(42, 24)',
            '"{1} {a}".format(5, 6, a=2)',
            '"{1}".format(*args)',
        ],
    )
    def test_explicit_positions_with_enough_arguments(self, code: str) -> None:
        node = astroid.extract_node(code)
        with self.assertNoMessages():
            self.checker.visit_call(node)
