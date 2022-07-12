# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import sys

from pylint.testutils.utils import _test_sys_path


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
