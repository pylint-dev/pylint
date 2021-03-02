# pylint: disable=missing-module-docstring, missing-function-docstring, protected-access
import unittest.mock
from io import StringIO

from test_self import _patch_streams

import pylint.lint


def run_with_config_file(config_file, args):
    """Initialize and runs pylint with the given configuration filei and args.

    Returns tuple of (runner, exit_code)
    """
    # prepend args with the rcfile loader
    args = [
        "--rcfile",
        str(config_file).strip(),
    ] + args
    out = StringIO()
    # If we used `pytest.raises(SystemExit)`, the `runner` variable
    # would not be accessible outside the `with` block.
    with unittest.mock.patch("sys.exit") as mocked_exit:
        with _patch_streams(out):
            runner = pylint.lint.Run(args)
    exit_code = mocked_exit.call_args[0][0]
    return runner, exit_code, out.getvalue()


def check_null_runner_with_config_file(config_file, args):
    """Initialize pylint with the given configuration file, but doesn't run checks

    Do not actually run checks, that could be slow. Do not mock
    `Pylinter.check`: it calls `Pylinter.initialize` which is
    needed to properly set up messages inclusion/exclusion
    in `_msg_states`, used by `is_message_enabled`.

    Returns tuple of (runner, exit_code, stdout)
    """
    with unittest.mock.patch("pylint.lint.pylinter.check_parallel"):
        return run_with_config_file(config_file, args)


def check_configuration_file_reader(config_file):
    """Initialize pylint with the given configuration file and check that
    what we initialized the linter with what was expected.

    Returns the runner
    """
    runner, exit_code, _ = check_null_runner_with_config_file(config_file, [])

    # "logging-not-lazy" and "logging-format-interpolation"
    expected_disabled = {"W1201", "W1202"}
    for msgid in expected_disabled:
        assert not runner.linter.is_message_enabled(msgid)
    assert runner.linter.config.jobs == 10
    assert runner.linter.config.reports

    # For the config tests we check that the config parsed properly
    assert exit_code == 0

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
