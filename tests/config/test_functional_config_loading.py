# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""This launches the configuration functional tests. This permits to test configuration
files by providing a file with the appropriate extension in the ``tests/config/functional``
directory.

Let's say you have a regression_list_crash.toml file to test. Then, if there is an error in the
conf, add an empty ``regression_list_crash.2.out`` alongside your file, where ``2`` is the
expected exit code. Its content is the expected output of pylint, a golden master handled by
pytest-remaster: run the test and it writes the output there, with ``{abspath}`` and
``{relpath}`` in place of the path of the configuration file.

You must also define a ``regression_list_crash.result.json`` if you want to check the parsed
configuration. This file will be loaded as a dict and will override the default value of the
default pylint configuration. If you need to append or remove a value use the special key
``"functional_append"`` and ``"functional_remove":``. Check the existing code for examples.
"""

# pylint: disable=redefined-outer-name
import logging
import warnings
from pathlib import Path

import pytest
from pytest import CaptureFixture, LogCaptureFixture
from pytest_remaster import GoldenMaster

from pylint.testutils.configuration_test import (
    PylintConfiguration,
    get_expected_configuration,
    get_expected_output,
    run_using_a_configuration_file,
)

HERE = Path(__file__).parent
USER_SPECIFIC_PATH = HERE.parent.parent
FUNCTIONAL_DIR = HERE / "functional"
# We use string then recast to path, so we can use -k in pytest.
# Otherwise, we get 'configuration_path0' as a test name. The path is relative to the functional
# directory because otherwise the string would be very lengthy.
ACCEPTED_CONFIGURATION_EXTENSIONS = ("toml", "ini", "cfg")
CONFIGURATION_PATHS = [
    str(path.relative_to(FUNCTIONAL_DIR))
    for ext in ACCEPTED_CONFIGURATION_EXTENSIONS
    for path in FUNCTIONAL_DIR.rglob(f"*.{ext}")
    if (str_path := str(path))
    # The enable/disable all tests are not practical with this framework.
    # They require manually listing ~400 messages, which will
    # require constant updates.
    and "enable_all" not in str_path and "disable_all" not in str_path
]


def _as_expected_output(output: str, configuration_path: str) -> str:
    """Turn pylint's output into the content of an ``.out`` file.

    The ``.out`` files are read with ``str.format``, so braces are doubled and
    the paths of the configuration file become ``{abspath}`` and ``{relpath}``.
    """
    relpath = str(Path(configuration_path).relative_to(USER_SPECIFIC_PATH))
    output = output.replace("{", "{{").replace("}", "}}")
    output = output.replace(configuration_path, "{abspath}").replace(
        relpath, "{relpath}"
    )
    return output.rstrip() + "\n"


def _check_output(
    golden_master: GoldenMaster,
    configuration_path: str,
    expected_code: int,
    output: str,
) -> None:
    path = Path(configuration_path)
    expected_path = path.parent / f"{path.stem}.{expected_code}.out"
    if output or expected_path.exists():
        golden_master.check(
            _as_expected_output(output, configuration_path), expected_path
        )


@pytest.fixture()
def default_configuration(
    tmp_path: Path, file_to_lint_path: str
) -> PylintConfiguration:
    empty_pylintrc = tmp_path / "pylintrc"
    empty_pylintrc.write_text("")
    runner = run_using_a_configuration_file(str(empty_pylintrc), file_to_lint_path)
    assert runner.linter.msg_status == 0
    return runner.linter.config.__dict__


@pytest.mark.parametrize("configuration_path", CONFIGURATION_PATHS)
def test_functional_config_loading(
    configuration_path: str,
    default_configuration: PylintConfiguration,
    file_to_lint_path: str,
    capsys: CaptureFixture[str],
    caplog: LogCaptureFixture,
    golden_master: GoldenMaster,
) -> None:
    """Functional tests for configurations."""
    # logging is helpful to see what's expected and why. The output of the
    # program is checked during the test so printing messes with the result.
    caplog.set_level(logging.INFO)
    configuration_path = str(FUNCTIONAL_DIR / configuration_path)
    msg = f"Wrong result with configuration {configuration_path}"
    expected_code, _ = get_expected_output(configuration_path, USER_SPECIFIC_PATH)
    expected_loaded_configuration = get_expected_configuration(
        configuration_path, default_configuration
    )
    runner = None  # The runner can fail to init if conf is bad enough.
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", message="The use of 'MASTER'.*", category=UserWarning
        )
        try:
            runner = run_using_a_configuration_file(
                configuration_path, file_to_lint_path
            )
            assert runner.linter.msg_status == expected_code
        except SystemExit as e:
            # Case where the conf exit with an argparse error
            assert e.code == expected_code
            out, err = capsys.readouterr()
            assert out == ""
            _check_output(golden_master, configuration_path, expected_code, err)
            return

    out, err = capsys.readouterr()
    _check_output(golden_master, configuration_path, expected_code, out)
    assert sorted(expected_loaded_configuration.keys()) == sorted(
        runner.linter.config.__dict__.keys()
    ), msg
    for key, expected_value in expected_loaded_configuration.items():
        key_msg = f"{msg} for key '{key}':"
        if isinstance(expected_value, list):
            assert sorted(expected_value) == sorted(
                runner.linter.config.__dict__[key]
            ), key_msg
        else:
            assert expected_value == runner.linter.config.__dict__[key], key_msg
    assert not err, msg
