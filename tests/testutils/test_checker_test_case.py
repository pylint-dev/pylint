# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for CheckerTestCase assertion methods."""

from __future__ import annotations

import pytest

from pylint.checkers.base_checker import BaseChecker
from pylint.interfaces import UNDEFINED
from pylint.testutils import CheckerTestCase, MessageTest


class _DummyChecker(BaseChecker):
    """A minimal checker used only for testing the test infrastructure."""

    name = "dummy-for-testcase"
    msgs = {
        "W9901": ("Dummy message A", "dummy-msg-a", "Dummy message A."),
        "W9902": ("Dummy message B", "dummy-msg-b", "Dummy message B."),
    }


_MSG_A = MessageTest("W9901", line=1, node=None, args=None, confidence=UNDEFINED)
_MSG_B = MessageTest("W9902", line=2, node=None, args=None, confidence=UNDEFINED)


class TestCheckerTestCase(CheckerTestCase):
    CHECKER_CLASS = _DummyChecker

    # -- assertAddsMessages scenarios (1-3) -----------------------------------

    def test_assert_adds_messages_success(self) -> None:
        """Scenario 1: expected raised / actual raised."""
        with self.assertAddsMessages(_MSG_A):
            self.linter.add_message("W9901", line=1)

    def test_assert_adds_messages_failure_not_raised(self) -> None:
        """Scenario 2: expected raised / actual not raised."""
        with pytest.raises(AssertionError):
            with self.assertAddsMessages(_MSG_A):
                pass  # nothing emitted

    def test_assert_adds_messages_failure_wrong_message(self) -> None:
        """Scenario 3: expected raised / actual not raised but another one raised."""
        with pytest.raises(AssertionError):
            with self.assertAddsMessages(_MSG_A):
                self.linter.add_message("W9902", line=2)

    # -- assertDoesNotAddMessages scenarios (4-6) -----------------------------

    def test_assert_does_not_add_messages_failure(self) -> None:
        """Scenario 4: expected not raised / actual raised."""
        with pytest.raises(AssertionError):
            with self.assertDoesNotAddMessages(_MSG_A):
                self.linter.add_message("W9901", line=1)

    def test_assert_does_not_add_messages_success(self) -> None:
        """Scenario 5: expected not raised / actual not raised."""
        with self.assertDoesNotAddMessages(_MSG_A):
            pass  # nothing emitted

    def test_assert_does_not_add_messages_success_other_raised(self) -> None:
        """Scenario 6: expected not raised / actual not raised but another one raised."""
        with self.assertDoesNotAddMessages(_MSG_A):
            self.linter.add_message("W9902", line=2)

    # -- additional edge cases ------------------------------------------------

    def test_assert_does_not_add_messages_ignore_position(self) -> None:
        """Position mismatch means no match when ignore_position=False."""
        # Same msg_id but different line: should pass (not a match)
        msg_different_line = MessageTest(
            "W9901", line=99, node=None, args=None, confidence=UNDEFINED
        )
        with self.assertDoesNotAddMessages(msg_different_line):
            self.linter.add_message("W9901", line=1)

    def test_assert_does_not_add_messages_ignore_position_true(self) -> None:
        """With ignore_position=True, position differences are ignored."""
        msg_different_line = MessageTest(
            "W9901", line=99, node=None, args=None, confidence=UNDEFINED
        )
        with pytest.raises(AssertionError):
            with self.assertDoesNotAddMessages(
                msg_different_line, ignore_position=True
            ):
                self.linter.add_message("W9901", line=1)

    def test_assert_does_not_add_messages_multiple_unwanted(self) -> None:
        """Fails when any of several unwanted messages is found."""
        with pytest.raises(AssertionError):
            with self.assertDoesNotAddMessages(_MSG_A, _MSG_B):
                self.linter.add_message("W9902", line=2)
