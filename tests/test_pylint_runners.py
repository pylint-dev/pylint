# pylint: disable=missing-module-docstring, missing-function-docstring
import os
import sys
from typing import Callable
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
