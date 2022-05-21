# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Test for the 'pylint-config generate' command."""


import warnings

import pytest
from pytest import CaptureFixture, MonkeyPatch

from pylint.lint.run import _PylintConfigRun as Run


def test_generate_interactive_exitcode(monkeypatch: MonkeyPatch) -> None:
    """Check that we exit correctly based on different parameters."""
    # Monkeypatch everything we don't want to check in this test
    monkeypatch.setattr(
        "pylint.config._pylint_config.utils.get_and_validate_format", lambda: "toml"
    )

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="NOTE:.*", category=UserWarning)
        with pytest.raises(SystemExit) as ex:
            Run(["generate", "--interactive"])
        assert ex.value.code == 0

        Run(["generate", "--interactive"], exit=False)


def test_format_of_output(
    monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]
) -> None:
    """Check that we output the correct format."""
    # Set the answers needed for the input() calls
    answers = iter(["T", "toml", "TOML", "I", "INI", "TOMLINI", "exit()"])
    monkeypatch.setattr("builtins.input", lambda x: next(answers))

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="NOTE:.*", category=UserWarning)
        # Check 'T'
        Run(["generate", "--interactive"], exit=False)
        captured = capsys.readouterr()
        assert "[tool.pylint.main]" in captured.out

        # Check 'toml'
        Run(["generate", "--interactive"], exit=False)
        captured = capsys.readouterr()
        assert "[tool.pylint.main]" in captured.out

        # Check 'TOML'
        Run(["generate", "--interactive"], exit=False)
        captured = capsys.readouterr()
        assert "[tool.pylint.main]" in captured.out

        # Check 'I'
        Run(["generate", "--interactive"], exit=False)
        captured = capsys.readouterr()
        assert "[MAIN]" in captured.out

        # Check 'INI'
        Run(["generate", "--interactive"], exit=False)
        captured = capsys.readouterr()
        assert "[MAIN]" in captured.out

        # Check 'TOMLINI' and then 'exit()'
        with pytest.raises(SystemExit):
            Run(["generate", "--interactive"], exit=False)
