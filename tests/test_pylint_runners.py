# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt
# pylint: disable=missing-module-docstring, missing-function-docstring

from __future__ import annotations

import os
import sys
from collections.abc import Callable
from unittest.mock import patch

import pytest
from py._path.local import LocalPath  # type: ignore[import]

from pylint import run_epylint, run_pylint, run_pyreverse, run_symilar


@pytest.mark.parametrize(
    "runner", [run_epylint, run_pylint, run_pyreverse, run_symilar]
)
def test_runner(runner: Callable, tmpdir: LocalPath) -> None:
    filepath = os.path.abspath(__file__)
    testargs = ["", filepath]
    with tmpdir.as_cwd():
        with patch.object(sys, "argv", testargs):
            with pytest.raises(SystemExit) as err:
                runner()
            assert err.value.code == 0


@pytest.mark.parametrize(
    "runner", [run_epylint, run_pylint, run_pyreverse, run_symilar]
)
def test_runner_with_arguments(runner: Callable, tmpdir: LocalPath) -> None:
    """Check the runners with arguments as parameter instead of sys.argv."""
    filepath = os.path.abspath(__file__)
    testargs = [filepath]
    with tmpdir.as_cwd():
        with pytest.raises(SystemExit) as err:
            runner(testargs)
        assert err.value.code == 0
