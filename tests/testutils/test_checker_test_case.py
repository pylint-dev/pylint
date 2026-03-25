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
            with self.assertDoesNotAddMessages("W9901"):
                self.linter.add_message("W9901", line=1)

    def test_assert_does_not_add_messages_success(self) -> None:
        """Scenario 5: expected not raised / actual not raised."""
        with self.assertDoesNotAddMessages("W9901"):
            pass  # nothing emitted

    def test_assert_does_not_add_messages_success_other_raised(self) -> None:
        """Scenario 6: expected not raised / actual not raised but another one raised."""
        with self.assertDoesNotAddMessages("W9901"):
            self.linter.add_message("W9902", line=2)

    # -- additional edge cases ------------------------------------------------

    def test_assert_does_not_add_messages_no_args_raises(self) -> None:
        """Calling with no arguments must raise TypeError."""
        with pytest.raises(TypeError, match="requires at least one"):
            with self.assertDoesNotAddMessages():
                pass

    def test_assert_does_not_add_messages_multiple_unwanted(self) -> None:
        """Fails when any of the several unwanted message IDs is found."""
        with pytest.raises(AssertionError):
            with self.assertDoesNotAddMessages("W9901", "W9902"):
                self.linter.add_message("W9902", line=2)

    def test_assert_does_not_add_messages_exception_in_body_drains_messages(
        self,
    ) -> None:
        """An exception in the with-block must not leak messages to later tests."""
        with pytest.raises(RuntimeError):
            with self.assertDoesNotAddMessages("W9901"):
                self.linter.add_message("W9901", line=1)
                raise RuntimeError("something went wrong")
        # Messages must have been drained; a subsequent assertNoMessages should pass.
        with self.assertNoMessages():
            pass
