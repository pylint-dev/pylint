# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from pathlib import Path

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


def test_run_pylint_with_invalid_argument_in_config(
    capsys: CaptureFixture[str], tmp_path: Path
) -> None:
    """Check that appropriate exit code is used with an ambiguous
    argument in a config file.
    """
    test_file = tmp_path / "testpylintrc"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("[MASTER]\nno=")

    with pytest.raises(SystemExit) as ex:
        run_pylint(["--rcfile", f"{test_file}"])
    captured = capsys.readouterr()
    assert captured.err.startswith("usage: pylint [options]")
    assert ex.value.code == 32
