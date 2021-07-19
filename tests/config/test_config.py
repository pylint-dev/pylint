import os
from pathlib import Path
from typing import Optional, Set

<<<<<<< HEAD
=======
import pytest

import pylint.lint
>>>>>>> Adding check for dict
from pylint.lint.run import Run
from pylint.testutils.configuration_test import run_using_a_configuration_file


def check_configuration_file_reader(
    runner: Run,
    expected_disabled: Optional[Set[str]] = None,
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


def test_toml_with_empty_list_for_plugins(tmp_path):
    # This would check that there is no crash for when empty lists
    # passed as plugins , refer #4580
    config_file = tmp_path / "pyproject.toml"
    config_file.write_text(
        """
[tool.pylint]
disable = "logging-not-lazy,logging-format-interpolation"
load-plugins = []
"""
    )
    with pytest.raises(AttributeError):
        check_configuration_file_reader(config_file)


def test_toml_with_invalid_data_for_imports(tmp_path):
    # This would test config with invalid data for imports section
    # refer #4580
    config_file = tmp_path / "pyproject.toml"
    config_file.write_text(
        """
[tool.pylint."imports"]
disable = [
    "logging-not-lazy",
    "logging-format-interpolation",
]
preferred-modules = { "a"="b" }
"""
    )
    with pytest.raises(AttributeError):
        check_configuration_file_reader(config_file)


def test_toml_with_invalid_data_for_basic(tmp_path):
    # This would test config with invalid data for basic section
    # refer #4580
    config_file = tmp_path / "pyproject.toml"
    config_file.write_text(
        """
[tool.pylint."basic"]
disable = [
    "logging-not-lazy",
    "logging-format-interpolation",
]
name-group = { "a"="b" }
"""
    )
    with pytest.raises(AttributeError):
        check_configuration_file_reader(config_file)
