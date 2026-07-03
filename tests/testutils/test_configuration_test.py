# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import logging
from pathlib import Path

from pytest import LogCaptureFixture

from pylint.testutils.configuration_test import get_expected_output

HERE = Path(__file__).parent
USER_SPECIFIC_PATH = HERE.parent.parent
DATA_DIRECTORY = HERE / "data"


def test_get_expected_output(caplog: LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    exit_code, _ = get_expected_output(DATA_DIRECTORY / "t.toml", USER_SPECIFIC_PATH)
    assert "Too much .out files" in str(caplog.text)
    assert exit_code == -1
    exit_code, _ = get_expected_output(DATA_DIRECTORY / "u.toml", USER_SPECIFIC_PATH)
    assert exit_code == -1
    assert "Wrong format for .out file name" in str(caplog.text)
    exit_code, _ = get_expected_output(DATA_DIRECTORY / "v.toml", USER_SPECIFIC_PATH)
    assert exit_code == 0
    assert ".out file does not exists" in str(caplog.text)
