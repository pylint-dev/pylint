"""Profiles basic -jX functionality."""

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

# pylint: disable=missing-function-docstring

import os
import pprint
from pathlib import Path

import pytest

from pylint.testutils import GenericTestReporter as Reporter
from pylint.testutils._run import _Run as Run


def _get_py_files(scanpath: str) -> list[str]:
    assert os.path.exists(scanpath), f"Dir not found {scanpath}"

    filepaths: list[str] = []
    for dirpath, dirnames, filenames in os.walk(scanpath):
        dirnames[:] = [dirname for dirname in dirnames if dirname != "__pycache__"]
        filepaths.extend(
            [
                os.path.join(dirpath, filename)
                for filename in filenames
                if filename.endswith(".py")
            ]
        )
    return filepaths


@pytest.mark.skipif(
    not os.environ.get("PYTEST_PROFILE_EXTERNAL", False),
    reason="PYTEST_PROFILE_EXTERNAL, not set, assuming not a profile run",
)
@pytest.mark.parametrize(
    "name,git_repo", [("numpy", "https://github.com/numpy/numpy.git")]
)
def test_run(tmp_path: Path, name: str, git_repo: str) -> None:
    """Runs pylint against external sources."""
    checkoutdir = tmp_path / name
    checkoutdir.mkdir()
    os.system(f"git clone --depth=1 {git_repo} {checkoutdir}")
    filepaths = _get_py_files(scanpath=str(checkoutdir))
    print(f"Have {len(filepaths)} files")

    runner = Run(filepaths, reporter=Reporter(), exit=False)

    print(
        f"Had {len(filepaths)} files with {len(runner.linter.reporter.messages)} messages"
    )
    pprint.pprint(runner.linter.reporter.messages)
