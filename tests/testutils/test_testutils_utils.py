# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import os
import sys
from pathlib import Path

from pylint.testutils.utils import _test_cwd, _test_sys_path


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
