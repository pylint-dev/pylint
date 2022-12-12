# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt


import pytest
from _pytest.capture import CaptureFixture

from pylint import run_pylint


def test_run_pylint_with_invalid_argument(capsys: CaptureFixture[str]) -> None:
    """Check that appropriate exit code is used with invalid argument."""
    with pytest.raises(SystemExit) as ex:
        run_pylint(["--never-use-this"])
    captured = capsys.readouterr()
    assert captured.err.startswith("usage: pylint [options]")
    assert ex.value.code == 32
