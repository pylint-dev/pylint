# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Unit tests for the config module."""

from __future__ import annotations

import re
import sre_constants

import pytest

from pylint import config
from pylint.checkers import BaseChecker
from pylint.testutils import CheckerTestCase, set_config


def test__regexp_validator_valid() -> None:
    result = config.option._regexp_validator(None, None, "test_.*")
    assert isinstance(result, re.Pattern)
    assert result.pattern == "test_.*"


def test__regexp_validator_invalid() -> None:
    with pytest.raises(sre_constants.error):
        config.option._regexp_validator(None, None, "test_)")


def test__csv_validator_no_spaces() -> None:
    values = ["One", "Two", "Three"]
    result = config.option._csv_validator(None, None, ",".join(values))
    assert isinstance(result, list)
    assert len(result) == 3
    for i, value in enumerate(values):
        assert result[i] == value


def test__csv_validator_spaces() -> None:
    values = ["One", "Two", "Three"]
    result = config.option._csv_validator(None, None, ", ".join(values))
    assert isinstance(result, list)
    assert len(result) == 3
    for i, value in enumerate(values):
        assert result[i] == value


def test__regexp_csv_validator_valid() -> None:
    pattern_strings = ["test_.*", "foo\\.bar", "^baz$"]
    result = config.option._regexp_csv_validator(None, None, ",".join(pattern_strings))
    for i, regex in enumerate(result):
        assert isinstance(regex, re.Pattern)
        assert regex.pattern == pattern_strings[i]


def test__regexp_csv_validator_invalid() -> None:
    pattern_strings = ["test_.*", "foo\\.bar", "^baz)$"]
    with pytest.raises(sre_constants.error):
        config.option._regexp_csv_validator(None, None, ",".join(pattern_strings))


class TestPyLinterOptionSetters(CheckerTestCase):
    """Class to check the set_config decorator for options declared in PyLinter."""

    class Checker(BaseChecker):
        name = "checker"
        msgs: dict[str, tuple[str, ...]] = {}
        options = (("test-opt", {"action": "store_true", "help": "help message"}),)

    CHECKER_CLASS: type = Checker

    @set_config(ignore_paths=".*/tests/.*,.*\\ignore\\.*")
    def test_ignore_paths_with_value(self) -> None:
        """Test ignore-paths option with value."""
        options = self.linter.config.ignore_paths

        assert any(i.match("dir/tests/file.py") for i in options)
        assert any(i.match("dir\\tests\\file.py") for i in options)
        assert any(i.match("dir/ignore/file.py") for i in options)
        assert any(i.match("dir\\ignore\\file.py") for i in options)

    def test_ignore_paths_with_no_value(self) -> None:
        """Test ignore-paths option with no value.
        Compare against actual list to see if validator works.
        """
        options = self.linter.config.ignore_paths

        assert options == []
