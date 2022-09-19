# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Unit tests for the config module."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from pylint import config
from pylint.checkers import BaseChecker
from pylint.lint import Run as _Run
from pylint.testutils import CheckerTestCase, set_config
from pylint.testutils._run import _Run as Run
from pylint.testutils.utils import _test_cwd
from pylint.typing import MessageDefinitionTuple


def test__regexp_validator_valid() -> None:
    result = config.option._regexp_validator(None, "", "test_.*")
    assert isinstance(result, re.Pattern)
    assert result.pattern == "test_.*"


def test__regexp_validator_invalid() -> None:
    with pytest.raises(re.error):
        config.option._regexp_validator(None, "", "test_)")


def test__csv_validator_no_spaces() -> None:
    values = ["One", "Two", "Three"]
    result = config.option._csv_validator(None, "", ",".join(values))
    assert isinstance(result, list)
    assert len(result) == 3
    for i, value in enumerate(values):
        assert result[i] == value


def test__csv_validator_spaces() -> None:
    values = ["One", "Two", "Three"]
    result = config.option._csv_validator(None, "", ", ".join(values))
    assert isinstance(result, list)
    assert len(result) == 3
    for i, value in enumerate(values):
        assert result[i] == value


def test__regexp_csv_validator_valid() -> None:
    pattern_strings = ["test_.*", "foo\\.bar", "^baz$"]
    result = config.option._regexp_csv_validator(None, "", ",".join(pattern_strings))
    for i, regex in enumerate(result):
        assert isinstance(regex, re.Pattern)
        assert regex.pattern == pattern_strings[i]


def test__regexp_csv_validator_invalid() -> None:
    pattern_strings = ["test_.*", "foo\\.bar", "^baz)$"]
    with pytest.raises(re.error):
        config.option._regexp_csv_validator(None, "", ",".join(pattern_strings))


class TestPyLinterOptionSetters(CheckerTestCase):
    """Class to check the set_config decorator for options declared in PyLinter."""

    class Checker(BaseChecker):
        name = "checker"
        msgs: dict[str, MessageDefinitionTuple] = {}
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


def test_files_can_be_set_in_config(tmp_path: Path) -> None:
    """Test that the files option can be set in a config file."""
    with _test_cwd(tmp_path):
        bad_file = tmp_path / "bad.py"
        bad_file.write_text("1")
        good_file = tmp_path / "good.py"
        good_file.write_text("'''My module docstring'''\n")
        init_file = tmp_path / "__init__.py"
        init_file.write_text("")

        # Test that we run on files set in the config file
        config_file = tmp_path / "pylintrc"
        config_file.write_text("[MASTER]\nfiles=good.py,bad.py")
        runner = Run(["--rcfile", str(config_file)], exit=False)
        assert runner.linter.stats.by_msg
        # Test that we can overrun the configuration file with a command line argument
        runner = Run(["good.py"], exit=False)
        assert not runner.linter.stats.by_msg
        # Or by supplying --files directly
        runner = Run(["--files", "good.py"], exit=False)
        assert not runner.linter.stats.by_msg

        # Test that we can run on the current directory by specifying it
        config_file = tmp_path / "pylintrc"
        config_file.write_text("[MASTER]\nfiles=" + str(tmp_path))
        runner = Run(["--rcfile", str(config_file)], exit=False)
        assert runner.linter.stats.by_msg
        # Test that we can also use just the command 'pylint'. Using _Run
        # makes sure that the --rcfile option doesn't get patched.
        other_runner = _Run([], exit=False)
        assert other_runner.linter.stats.by_msg

    # Test that we can also run on a directory set as files even if it is
    # not our current cwd
    config_file = tmp_path / "pylintrc"
    config_file.write_text("[MASTER]\nfiles=" + str(tmp_path))
    runner = Run(["--rcfile", str(config_file)], exit=False)
    assert runner.linter.stats.by_msg
