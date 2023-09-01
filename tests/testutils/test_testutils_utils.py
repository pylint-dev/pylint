# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import os
import sys
from pathlib import Path

import pytest

from pylint.testutils.utils import _test_cwd, _test_environ_pythonpath, _test_sys_path


def test__test_sys_path_no_arg() -> None:
    sys_path = sys.path
    with _test_sys_path():
        assert sys.path == sys_path
        new_sys_path = ["new_sys_path"]
        sys.path = new_sys_path
        assert sys.path == new_sys_path
    assert sys.path == sys_path


def test__test_sys_path() -> None:
    sys_path = sys.path
    new_sys_path = [".", "/home"]
    with _test_sys_path(new_sys_path):
        assert sys.path == new_sys_path
        newer_sys_path = ["new_sys_path"]
        sys.path = newer_sys_path
        assert sys.path == newer_sys_path
    assert sys.path == sys_path


def test__test_cwd_no_arg(tmp_path: Path) -> None:
    cwd = os.getcwd()
    with _test_cwd():
        assert os.getcwd() == cwd
        os.chdir(tmp_path)
        assert os.getcwd() == str(tmp_path)
    assert os.getcwd() == cwd


def test__test_cwd(tmp_path: Path) -> None:
    cwd = os.getcwd()
    with _test_cwd(tmp_path):
        assert os.getcwd() == str(tmp_path)
        new_path = tmp_path / "another_dir"
        new_path.mkdir()
        os.chdir(new_path)
        assert os.getcwd() == str(new_path)
    assert os.getcwd() == cwd


@pytest.mark.parametrize("old_pythonpath", ["./oldpath/:", None])
def test__test_environ_pythonpath_no_arg(old_pythonpath: str) -> None:
    real_pythonpath = os.environ.get("PYTHONPATH")
    with _test_environ_pythonpath(old_pythonpath):
        with _test_environ_pythonpath():
            assert os.environ.get("PYTHONPATH") is None
            new_pythonpath = "./whatever/:"
            os.environ["PYTHONPATH"] = new_pythonpath
            assert os.environ.get("PYTHONPATH") == new_pythonpath
        assert os.environ.get("PYTHONPATH") == old_pythonpath
    assert os.environ.get("PYTHONPATH") == real_pythonpath


@pytest.mark.parametrize("old_pythonpath", ["./oldpath/:", None])
def test__test_environ_pythonpath(old_pythonpath: str) -> None:
    real_pythonpath = os.environ.get("PYTHONPATH")
    with _test_environ_pythonpath(old_pythonpath):
        new_pythonpath = "./whatever/:"
        with _test_environ_pythonpath(new_pythonpath):
            assert os.environ.get("PYTHONPATH") == new_pythonpath
            newer_pythonpath = "./something_else/:"
            os.environ["PYTHONPATH"] = newer_pythonpath
            assert os.environ.get("PYTHONPATH") == newer_pythonpath
        assert os.environ.get("PYTHONPATH") == old_pythonpath
    assert os.environ.get("PYTHONPATH") == real_pythonpath
