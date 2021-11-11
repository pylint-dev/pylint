# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""
This launch the configuration functional tests. This permit to test configuration
files by providing a file with the appropriate extension in the ``tests/config/functional``
directory.

Let's say you have a regression_list_crash.toml file to test. Then if there is an error in the conf,
add ``regression_list_crash.out`` alongside your file with the expected output of pylint in it. Use
``{relpath}`` and ``{abspath}`` for the path of the file. The exit code will have to be 2 (error)
if this file exists.

You must also define a ``regression_list_crash.result.json`` if you want to check the parsed configuration.
This file will be loaded as a dict and will override the default value of the default pylint
configuration. If you need to append or remove a value use the special key ``"functional_append"``
and ``"functional_remove":``. Check the existing code for examples.
"""

# pylint: disable=redefined-outer-name
import logging
from pathlib import Path
from typing import Any, Dict

import pytest
from _pytest.capture import CaptureFixture
from _pytest.logging import LogCaptureFixture

from pylint.testutils.configuration_test import (
    get_expected_configuration,
    get_expected_output,
    run_using_a_configuration_file,
)

HERE = Path(__file__).parent
FUNCTIONAL_DIR = HERE / "functional"
# We use string then recast to path so we can use -k in pytest.
# Otherwise we get 'configuration_path0' as a test name. The path is relative to the functional
# directory because otherwise the string would be very lengthy.
CONFIGURATION_PATHS = [
    str(path.relative_to(FUNCTIONAL_DIR))
    for ext in ("toml", "ini", "cfg")
    for path in FUNCTIONAL_DIR.rglob(f"*.{ext}")
]
FILE_TO_LINT = str(HERE / "file_to_lint.py")


@pytest.fixture()
def default_configuration(tmp_path: Path) -> Dict[str, Any]:
    empty_pylintrc = tmp_path / "pylintrc"
    empty_pylintrc.write_text("")
    mock_exit, _, runner = run_using_a_configuration_file(
        str(empty_pylintrc), FILE_TO_LINT
    )
    mock_exit.assert_called_once_with(0)
    return runner.linter.config.__dict__


@pytest.mark.parametrize("configuration_path", CONFIGURATION_PATHS)
def test_functional_config_loading(
    configuration_path: str,
    default_configuration: Dict[str, Any],
    capsys: CaptureFixture,
    caplog: LogCaptureFixture,
):
    """Functional tests for configurations."""
    caplog.set_level(logging.INFO)
    configuration_path = str(FUNCTIONAL_DIR / configuration_path)
    msg = f"Wrong result with configuration {configuration_path}"
    expected_code, expected_output = get_expected_output(configuration_path)
    expected_loaded_configuration = get_expected_configuration(
        configuration_path, default_configuration
    )
    mock_exit, _, runner = run_using_a_configuration_file(
        configuration_path, FILE_TO_LINT
    )
    mock_exit.assert_called_once_with(expected_code)
    out, err = capsys.readouterr()
    # rstrip() applied so we can have a final newline in the expected test file
    assert expected_output.rstrip() == out.rstrip(), msg
    assert sorted(expected_loaded_configuration.keys()) == sorted(
        runner.linter.config.__dict__.keys()
    ), msg
    for key in expected_loaded_configuration:
        key_msg = f"{msg} for key '{key}':"
        expected_value = expected_loaded_configuration[key]
        if isinstance(expected_value, list):
            assert sorted(expected_value) == sorted(
                runner.linter.config.__dict__[key]
            ), key_msg
        else:
            assert expected_value == runner.linter.config.__dict__[key], key_msg
    assert not err, msg
