# pylint: disable=missing-module-docstring, missing-function-docstring
import os
import sys
from unittest.mock import patch

import pytest

from pylint import run_epylint, run_pylint, run_pyreverse, run_symilar


@pytest.mark.parametrize(
    "runner", [run_epylint, run_pylint, run_pyreverse, run_symilar]
)
def test_runner(runner, tmpdir):
    filepath = os.path.abspath(__file__)
    testargs = ["", filepath]
    with tmpdir.as_cwd():
        with patch.object(sys, "argv", testargs):
            with pytest.raises(SystemExit) as err:
                runner()
            assert err.value.code == 0
