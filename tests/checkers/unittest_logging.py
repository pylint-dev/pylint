# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the logging checker."""

from __future__ import annotations

import astroid
from astroid import nodes

from pylint.checkers.logging import LoggingChecker
from pylint.testutils import CheckerTestCase


class TestLoggingChecker(CheckerTestCase):
    """Tests for LoggingChecker."""

    CHECKER_CLASS = LoggingChecker

    def _check_code(self, code: str) -> None:
        """Helper to properly check a code snippet with the logging checker."""
        module = astroid.parse(code)
        self.checker.visit_module(module)
        # Walk the entire AST tree
        for node in module.nodes_of_class((nodes.Import, nodes.ImportFrom)):
            if isinstance(node, nodes.Import):
                self.checker.visit_import(node)
            else:
                self.checker.visit_importfrom(node)
        for node in module.nodes_of_class(nodes.Call):
            self.checker.visit_call(node)

    def test_logging_unsupported_format_without_args(self) -> None:
        """Test that unsupported format chars are not reported without args.

        According to Python docs, no formatting is performed when no args are supplied.
        This test verifies the fix for issue #10752.
        """
        with self.assertNoMessages():
            self._check_code(
                """
import logging
logging.warning("%badformat")
            """
            )

    def test_logging_original_issue_10752(self) -> None:
        """Test the exact case from issue #10752."""
        with self.assertNoMessages():
            self._check_code(
                """
import logging
logging.error("%test")
            """
            )

    def test_logging_invalid_format_specifier_without_args(self) -> None:
        """Test invalid format specifiers without args don't trigger unsupported-format."""
        with self.assertNoMessages():
            self._check_code(
                """
import logging
logging.info("%z - invalid but no args so no formatting")
            """
            )

    def test_logging_multiple_invalid_format_without_args(self) -> None:
        """Test multiple invalid format chars without args."""
        with self.assertNoMessages():
            self._check_code(
                """
import logging
logging.warning("%q %z %k - all invalid but no args")
            """
            )

    def test_logging_valid_format_with_args(self) -> None:
        """Test that valid format strings with args don't trigger warnings."""
        with self.assertNoMessages():
            self._check_code(
                """
import logging
logging.info("User %s logged in", "john")
            """
            )

    def test_logging_unsupported_format_with_args_still_caught(self) -> None:
        """Test that unsupported format chars ARE reported when args are provided."""
        self._check_code(
            """
import logging
logging.error("%test", 123)
        """
        )
        # Check that at least one message was added
        messages = self.linter.release_messages()
        assert len(messages) > 0
        assert any(msg.msg_id == "logging-unsupported-format" for msg in messages)

    def test_logging_mixed_invalid_format_with_args_still_caught(self) -> None:
        """Test that invalid format chars are still caught when args provided."""
        self._check_code(
            """
import logging
logging.error("Value: %s, Invalid: %z", "test", "value")
        """
        )
        # Check that unsupported-format message was added
        messages = self.linter.release_messages()
        assert len(messages) > 0
        assert any(msg.msg_id == "logging-unsupported-format" for msg in messages)
