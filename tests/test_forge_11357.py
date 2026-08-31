"""Regression test for IndexError with missing Generator arguments.

See: https://github.com/pylint-dev/pylint/issues/11357
"""
import pytest
from pylint.testutils import CheckerTestCase, MessageTest, set_config
from pylint.extensions.typing import TypingChecker
import astroid


class TestTypingCheckerEmptyGenerator(CheckerTestCase):
    """Test that empty Generator subscript doesn't crash."""

    CHECKER_CLASS = TypingChecker

    @set_config()
    def test_empty_generator_subscript_no_crash(self):
        """Test that Generator[()] does not cause an IndexError."""
        code = """
from collections.abc import Generator

Generator[()]
"""
        module = astroid.parse(code)
        # This should not raise IndexError
        self.walk(module)
