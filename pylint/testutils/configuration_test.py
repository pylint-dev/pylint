# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Utility function for configuration testing."""
import copy
import json
import unittest
from pathlib import Path
from typing import Any, Dict, Tuple, Union

from pylint.lint import Run

USER_SPECIFIC = str(Path(__file__).parent.parent.parent)


def get_expected_or_default(pyproject_toml_path: str, suffix: str, default: Any) -> str:
    def get_path_according_to_suffix() -> Path:
        path = Path(pyproject_toml_path)
        return path.parent / f"{path.stem}.{suffix}"

    expected = default
    expected_result_path = get_path_according_to_suffix()
    if expected_result_path.exists():
        with open(expected_result_path, encoding="utf8") as f:
            expected = f.read()
    return expected


EXPECTED_CONF_APPEND_KEY = "functional_append"
EXPECTED_CONF_REMOVE_KEY = "functional_remove"
EXPECTED_CONF_SPECIAL_KEYS = [EXPECTED_CONF_APPEND_KEY, EXPECTED_CONF_REMOVE_KEY]


def get_expected_configuration(
    configuration_path: str, default_configuration: Dict[str, Any]
) -> Dict[str, Any]:
    """Get the expected parsed configuration of a configuration functional test"""
    result = copy.deepcopy(default_configuration)
    config_as_json = get_expected_or_default(
        configuration_path, suffix="result.json", default="{}"
    )
    to_override = json.loads(config_as_json)
    for key, value in to_override.items():
        if key not in EXPECTED_CONF_SPECIAL_KEYS:
            result[key] = value
    if EXPECTED_CONF_APPEND_KEY in to_override:
        for key, value in to_override[EXPECTED_CONF_APPEND_KEY].items():
            result[key] += value
    if EXPECTED_CONF_REMOVE_KEY in to_override:
        for key, value in to_override[EXPECTED_CONF_REMOVE_KEY].items():
            result[key] -= value
    return result


def get_expected_output(configuration_path: str) -> Tuple[int, str]:
    """Get the expected output of a functional test."""

    def get_relative_path(path: str) -> str:
        """Get the relative path we want without user specific information"""
        return path.replace(USER_SPECIFIC, "")[1:]

    output = get_expected_or_default(configuration_path, suffix="out", default="")
    exit_code = 2 if output else 0
    return exit_code, output.format(
        abspath=configuration_path, relpath=get_relative_path(configuration_path)
    )


def run_using_a_configuration_file(
    configuration_path: Union[Path, str], file_to_lint: str = __file__
) -> Tuple[unittest.mock.Mock, unittest.mock.Mock, Run]:
    """Simulate a run with a configuration without really launching the checks."""
    configuration_path = str(configuration_path)
    args = ["--rcfile", configuration_path, file_to_lint]
    # If we used `pytest.raises(SystemExit)`, the `runner` variable
    # would not be accessible outside the `with` block.
    with unittest.mock.patch("sys.exit") as mocked_exit:
        # Do not actually run checks, that could be slow. Do not mock
        # `Pylinter.check`: it calls `Pylinter.initialize` which is
        # needed to properly set up messages inclusion/exclusion
        # in `_msg_states`, used by `is_message_enabled`.
        check = "pylint.lint.pylinter.check_parallel"
        with unittest.mock.patch(check) as mocked_check_parallel:
            runner = Run(args)
    return mocked_exit, mocked_check_parallel, runner
