""" Profiles basic -jX functionality """
# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 Frank Harrison <frank@doublethefish.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

# pylint: disable=protected-access,missing-function-docstring,no-self-use

import os
import pprint

import pytest

from pylint.lint import Run
from pylint.testutils import GenericTestReporter as Reporter


def _get_py_files(scanpath):
    assert os.path.exists(scanpath), "Dir not found %s" % scanpath

    filepaths = []
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
def test_run(tmp_path, name, git_repo):
    """Runs pylint against external sources"""
    checkoutdir = tmp_path / name
    checkoutdir.mkdir()
    os.system(f"git clone --depth=1 {git_repo} {checkoutdir}")
    filepaths = _get_py_files(scanpath=str(checkoutdir))
    print("Have %d files" % len(filepaths))

    runner = Run(filepaths, reporter=Reporter(), do_exit=False)

    print(
        "Had %d files with %d messages"
        % (len(filepaths), len(runner.linter.reporter.messages))
    )
    pprint.pprint(runner.linter.reporter.messages)
