# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Test for the 'pylint-config generate' command."""


import warnings

import pytest
from pytest import CaptureFixture

from pylint import _run_pylint_config


def test_invocation_of_pylint_config(capsys: CaptureFixture[str]) -> None:
    """Check that the help messages are displayed correctly."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="NOTE:.*", category=UserWarning)
        with pytest.raises(SystemExit) as ex:
            _run_pylint_config([""])
        captured = capsys.readouterr()
        assert captured.err.startswith("usage: pylint-config [options]")
        assert ex.value.code == 2
