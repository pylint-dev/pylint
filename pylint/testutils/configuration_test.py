# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Utility functions for configuration testing."""
import copy
import json
import logging
import unittest
from pathlib import Path
from typing import Any, Dict, Tuple, Union
from unittest.mock import Mock

from pylint.lint import Run

USER_SPECIFIC_PATH = Path(__file__).parent.parent.parent
# We use Any in this typing because the configuration contains real objects and constants
# that could be a lot of things.
ConfigurationValue = Any
PylintConfiguration = Dict[str, ConfigurationValue]


def get_expected_or_default(
    tested_configuration_file: str, suffix: str, default: ConfigurationValue
) -> str:
    """Return the expected value from the file if it exists, or the given default."""

    def get_path_according_to_suffix() -> Path:
        path = Path(tested_configuration_file)
        return path.parent / f"{path.stem}.{suffix}"

    expected = default
    expected_result_path = get_path_according_to_suffix()
    if expected_result_path.exists():
        with open(expected_result_path, encoding="utf8") as f:
            expected = f.read()
        # logging is helpful to realize your file is not taken into
        # account after a misspell of the file name. The output of the
        # program is checked during the test so printing messes with the result.
        logging.info("%s exists.", expected_result_path)
    else:
        logging.info("%s not found, using '%s'.", expected_result_path, default)
    return expected


EXPECTED_CONF_APPEND_KEY = "functional_append"
EXPECTED_CONF_REMOVE_KEY = "functional_remove"


def get_expected_configuration(
    configuration_path: str, default_configuration: PylintConfiguration
) -> PylintConfiguration:
    """Get the expected parsed configuration of a configuration functional test"""
    result = copy.deepcopy(default_configuration)
    config_as_json = get_expected_or_default(
        configuration_path, suffix="result.json", default="{}"
    )
    to_override = json.loads(config_as_json)
    for key, value in to_override.items():
        if key == EXPECTED_CONF_APPEND_KEY:
            for fkey, fvalue in value.items():
                result[fkey] += fvalue
        elif key == EXPECTED_CONF_REMOVE_KEY:
            for fkey, fvalue in value.items():
                new_value = []
                for old_value in result[fkey]:
                    if old_value not in fvalue:
                        new_value.append(old_value)
                result[fkey] = new_value
        else:
            result[key] = value
    return result


def get_expected_output(configuration_path: str) -> Tuple[int, str]:
    """Get the expected output of a functional test."""
    output = get_expected_or_default(configuration_path, suffix="out", default="")
    if output:
        # logging is helpful to see what the expected exit code is and why.
        # The output of the program is checked during the test so printing
        # messes with the result.
        logging.info(
            "Output exists for %s so the expected exit code is 2", configuration_path
        )
        exit_code = 2
    else:
        logging.info(".out file does not exists, so the expected exit code is 0")
        exit_code = 0
    return exit_code, output.format(
        abspath=configuration_path,
        relpath=Path(configuration_path).relative_to(USER_SPECIFIC_PATH),
    )


def run_using_a_configuration_file(
    configuration_path: Union[Path, str], file_to_lint: str = __file__
) -> Tuple[Mock, Mock, Run]:
    """Simulate a run with a configuration without really launching the checks."""
    configuration_path = str(configuration_path)
    args = ["--rcfile", configuration_path, file_to_lint]
    # We do not capture the `SystemExit` as then the `runner` variable
    # would not be accessible outside the `with` block.
    with unittest.mock.patch("sys.exit") as mocked_exit:
        # Do not actually run checks, that could be slow. We don't mock
        # `Pylinter.check`: it calls `Pylinter.initialize` which is
        # needed to properly set up messages inclusion/exclusion
        # in `_msg_states`, used by `is_message_enabled`.
        check = "pylint.lint.pylinter.check_parallel"
        with unittest.mock.patch(check) as mocked_check_parallel:
            runner = Run(args)
    return mocked_exit, mocked_check_parallel, runner
