# pylint: disable=missing-module-docstring, missing-function-docstring, protected-access
import os
import unittest.mock

import pytest

import pylint.lint
from pylint.config import OptionsManagerMixIn


def check_configuration_file_reader(config_file):
    """Initialize pylint with the given configuration file and check that
    what we initialized the linter with what was expected.
    """
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

    # "logging-not-lazy" and "logging-format-interpolation"
    expected_disabled = {"W1201", "W1202"}
    for msgid in expected_disabled:
        assert not runner.linter.is_message_enabled(msgid)
    assert runner.linter.config.jobs == 10
    assert runner.linter.config.reports

    mocked_exit.assert_called_once_with(0)
    return runner


def test_can_read_ini(tmp_path):
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
    check_configuration_file_reader(config_file)


def test_can_read_setup_cfg(tmp_path):
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
    check_configuration_file_reader(config_file)


def test_can_read_toml(tmp_path):
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
    check_configuration_file_reader(config_file)


def test_can_read_toml_rich_types(tmp_path):
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
    check_configuration_file_reader(config_file)


def test_can_read_env_variable(tmp_path):
    # Check that we can read the "regular" INI .pylintrc file
    # if it has an environment variable.
    config_file = tmp_path / "pyproject.toml"
    config_file.write_text(
        """
[tool.pylint."messages control"]
disable = "logging-not-lazy,logging-format-interpolation"
jobs = "10"
reports = "yes"
"""
    )
    os.environ["tmp_path_env"] = str(tmp_path / "pyproject.toml")
    options_manager_mix_in = OptionsManagerMixIn("", "${tmp_path_env}")
    options_manager_mix_in.read_config_file("${tmp_path_env}")

    def test_read_config_file():
        with pytest.raises(OSError):
            options_manager_mix_in.read_config_file("${tmp_path_en}")

    test_read_config_file()
    options_manager_mix_in.load_config_file()
    section = options_manager_mix_in.cfgfile_parser.sections()[0]
    jobs, jobs_nr = options_manager_mix_in.cfgfile_parser.items(section)[1]
    assert jobs == "jobs"
    assert jobs_nr == "10"
