# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import os
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from pytest import CaptureFixture

from pylint.interfaces import CONFIDENCE_LEVEL_NAMES
from pylint.lint import Run as LintRun
from pylint.testutils import create_files
from pylint.testutils._run import _Run as Run
from pylint.testutils.configuration_test import run_using_a_configuration_file

HERE = Path(__file__).parent.absolute()
REGRTEST_DATA_DIR = HERE / ".." / "regrtest_data"
EMPTY_MODULE = REGRTEST_DATA_DIR / "empty.py"


def check_configuration_file_reader(
    runner: LintRun,
    expected_disabled: set[str] | None = None,
    expected_jobs: int = 10,
    expected_reports_truthey: bool = True,
) -> None:
    """Check that what we initialized the linter with what was expected."""
    if expected_disabled is None:
        # "logging-not-lazy" and "logging-format-interpolation"
        expected_disabled = {"W1201", "W1202"}
    for msgid in expected_disabled:
        assert not runner.linter.is_message_enabled(msgid)
    assert runner.linter.config.jobs == expected_jobs
    assert bool(runner.linter.config.reports) == expected_reports_truthey


def test_can_read_toml_env_variable(tmp_path: Path, file_to_lint_path: str) -> None:
    """We can read and open a properly formatted toml file."""
    config_file = tmp_path / "pyproject.toml"
    config_file.write_text(
        """
[tool.pylint."messages control"]
disable = "logging-not-lazy,logging-format-interpolation"
jobs = "10"
reports = "yes"
"""
    )
    env_var = "tmp_path_env"
    os.environ[env_var] = str(config_file)
    mock_exit, _, runner = run_using_a_configuration_file(
        f"${env_var}", file_to_lint_path
    )
    mock_exit.assert_called_once_with(0)
    check_configuration_file_reader(runner)


def test_unknown_message_id(capsys: CaptureFixture) -> None:
    """Check that we correctly raise a message on an unknown id."""
    Run([str(EMPTY_MODULE), "--disable=12345"], exit=False)
    output = capsys.readouterr()
    assert "Command line:1:0: W0012: Unknown option value for '--disable'" in output.out


def test_unknown_option_name(capsys: CaptureFixture) -> None:
    """Check that we correctly raise a message on an unknown option."""
    with pytest.raises(SystemExit):
        Run([str(EMPTY_MODULE), "--unknown-option=yes"], exit=False)
    output = capsys.readouterr()
    assert "usage: pylint" in output.err
    assert "Unrecognized option" in output.err


def test_unknown_short_option_name(capsys: CaptureFixture) -> None:
    """Check that we correctly raise a message on an unknown short option."""
    with pytest.raises(SystemExit):
        Run([str(EMPTY_MODULE), "-Q"], exit=False)
    output = capsys.readouterr()
    assert "usage: pylint" in output.err
    assert "Unrecognized option" in output.err


def test_unknown_confidence(capsys: CaptureFixture) -> None:
    """Check that we correctly error an unknown confidence value."""
    with pytest.raises(SystemExit):
        Run([str(EMPTY_MODULE), "--confidence=UNKNOWN_CONFIG"], exit=False)
    output = capsys.readouterr()
    assert "argument --confidence: UNKNOWN_CONFIG should be in" in output.err


def test_empty_confidence() -> None:
    """An empty confidence value indicates all errors should be emitted."""
    r = Run([str(EMPTY_MODULE), "--confidence="], exit=False)
    assert r.linter.config.confidence == CONFIDENCE_LEVEL_NAMES


def test_unknown_yes_no(capsys: CaptureFixture) -> None:
    """Check that we correctly error on an unknown yes/no value."""
    with pytest.raises(SystemExit):
        Run([str(EMPTY_MODULE), "--reports=maybe"], exit=False)
    output = capsys.readouterr()
    assert "Invalid yn value 'maybe', should be in " in output.err


def test_unknown_py_version(capsys: CaptureFixture) -> None:
    """Check that we correctly error on an unknown python-version."""
    with pytest.raises(SystemExit):
        Run([str(EMPTY_MODULE), "--py-version=the-newest"], exit=False)
    output = capsys.readouterr()
    assert "the-newest has an invalid format, should be a version string." in output.err


def test_regex_error(capsys: CaptureFixture) -> None:
    """Check that we correctly error when an an option is passed whose value is an invalid regular expression."""
    with pytest.raises(SystemExit):
        Run(
            [str(EMPTY_MODULE), r"--function-rgx=[\p{Han}a-z_][\p{Han}a-z0-9_]{2,30}$"],
            exit=False,
        )
    output = capsys.readouterr()

    assertString = (
        r"Error in provided regular expression: [\p{Han}a-z_][\p{Han}a-z0-9_]{2,30}$ "
        r"beginning at index 1: bad escape \p"
    )
    assert assertString in output.err


def test_csv_regex_error(capsys: CaptureFixture) -> None:
    """Check that we correctly error when an option is passed and one
    of its comma-separated regular expressions values is an invalid regular expression.
    """
    with pytest.raises(SystemExit):
        Run(
            [str(EMPTY_MODULE), r"--bad-names-rgx=(foo{1,3})"],
            exit=False,
        )
    output = capsys.readouterr()
    assert (
        r"Error in provided regular expression: (foo{1 beginning at index 0: missing ), unterminated subpattern"
        in output.err
    )


def test_short_verbose(capsys: CaptureFixture) -> None:
    """Check that we correctly handle the -v flag."""
    Run([str(EMPTY_MODULE), "-v"], exit=False)
    output = capsys.readouterr()
    assert "Using config file" in output.err


def test_argument_separator() -> None:
    """Check that we support using '--' to separate argument types.

    Reported in https://github.com/PyCQA/pylint/issues/7003.
    """
    runner = Run(["--", str(EMPTY_MODULE)], exit=False)
    assert not runner.linter.stats.by_msg


def test_clear_cache_post_run() -> None:
    modname = "changing.py"
    with TemporaryDirectory() as tmp_dir:
        create_files([modname], tmp_dir)
        module = tmp_dir + os.sep + modname
        # Run class does not produce the wanted failure
        # must use LintRun to get pylint.lint.Run
        run_before_edit = LintRun([module, "--clear-cache-post-run=y"], exit=False)
        with open(module, mode="a", encoding="utf-8") as f:
            f.write("undefined\n")
        run_after_edit = LintRun([module, "--clear-cache-post-run=y"], exit=False)

    assert not run_before_edit.linter.stats.by_msg
    assert run_after_edit.linter.stats.by_msg
