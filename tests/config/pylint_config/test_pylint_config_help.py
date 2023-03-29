# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Test for the 'pylint-config generate' command."""


import warnings

import pytest
from pytest import CaptureFixture

from pylint.lint.run import _PylintConfigRun as Run


def test_pylint_config_main_messages(capsys: CaptureFixture[str]) -> None:
    """Check that the help messages are displayed correctly."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="NOTE:.*", category=UserWarning)
        Run([], exit=False)
        captured = capsys.readouterr()
        assert captured.out.startswith("usage: pylint-config [options]")
        assert "--interactive" not in captured.out

        Run(["-h"], exit=False)
        captured_two = capsys.readouterr()
        assert captured_two.out == captured.out

        with pytest.raises(SystemExit):
            Run(["generate", "-h"])
        captured = capsys.readouterr()
        assert captured.out.startswith("usage: pylint-config [options] generate")
        assert "--interactive" in captured.out

        with pytest.raises(SystemExit) as ex:
            Run(["generate"])
        captured_two = capsys.readouterr()
        assert captured_two.out == captured.out
        # This gets auto-raised by argparse to be 0.
        assert ex.value.code == 32

        with pytest.raises(SystemExit) as ex:
            Run(["-h"])
        assert ex.value.code == 32
