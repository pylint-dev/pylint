# pylint: disable=missing-module-docstring, missing-function-docstring, protected-access
import os
import unittest.mock
from pathlib import Path
from typing import Optional, Set, Union

import pylint.lint
from pylint.lint.run import Run

def get_runner_from_config_file(
    config_file: Union[str, Path], expected_exit_code: int = 0
) -> Run:
    """Initialize pylint with the given configuration file and return the Run"""
    args = ["--rcfile", str(config_file), __file__]
    # If we used `pytest.raises(SystemExit)`, the `runner` variable
    # would not be accessible outside the `with` block.
    with unittest.mock.patch("sys.exit") as mocked_exit:
        # Do not actually run checks, that could be slow. Do not mock
        # `Pylinter.check`: it calls `Pylinter.initialize` which is
        # needed to properly set up messages inclusion/exclusion
        # in `_msg_states`, used by `is_message_enabled`.
        with unittest.mock.patch("pylint.lint.pylinter.check_parallel"):
            runner = pylint.lint.Run(args)
    mocked_exit.assert_called_once_with(expected_exit_code)
    return runner


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


def test_can_read_ini(tmp_path: Path) -> None:
    # Check that we can read the "regular" INI .pylintrc file
    config_file = tmp_path / ".pylintrc"
    config_file.write_text(
        """
[messages control]
disable = logging-not-lazy,logging-format-interpolation
jobs = 10
reports = yes
"""
    )
    run = get_runner_from_config_file(config_file)
    check_configuration_file_reader(run)


def test_can_read_setup_cfg(tmp_path: Path) -> None:
    # Check that we can read a setup.cfg (which is an INI file where
    # section names are prefixed with "pylint."
    config_file = tmp_path / "setup.cfg"
    config_file.write_text(
        """
[pylint.messages control]
disable = logging-not-lazy,logging-format-interpolation
jobs = 10
reports = yes
"""
    )
    run = get_runner_from_config_file(config_file)
    check_configuration_file_reader(run)


def test_can_read_toml(tmp_path: Path) -> None:
    # Check that we can read a TOML file where lists and integers are
    # expressed as strings.
    config_file = tmp_path / "pyproject.toml"
    config_file.write_text(
        """
[tool.pylint."messages control"]
disable = "logging-not-lazy,logging-format-interpolation"
jobs = "10"
reports = "yes"
"""
    )
    run = get_runner_from_config_file(config_file)
    check_configuration_file_reader(run)


def test_can_read_toml_rich_types(tmp_path: Path) -> None:
    # Check that we can read a TOML file where lists, integers and
    # booleans are expressed as such (and not as strings), using TOML
    # type system.
    config_file = tmp_path / "pyproject.toml"
    config_file.write_text(
        """
[tool.pylint."messages control"]
disable = [
    "logging-not-lazy",
    "logging-format-interpolation",
]
jobs = 10
reports = true
"""
    )
    run = get_runner_from_config_file(config_file)
    check_configuration_file_reader(run)


def test_can_read_toml_env_variable(tmp_path: Path) -> None:
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
    run = get_runner_from_config_file(f"${env_var}")
    check_configuration_file_reader(run)
