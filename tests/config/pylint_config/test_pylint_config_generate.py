# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Test for the 'pylint-config generate' command."""


import os
import tempfile
import warnings
from pathlib import Path

import pytest
from pytest import CaptureFixture, MonkeyPatch

from pylint.lint.run import _PylintConfigRun as Run


def test_generate_interactive_exitcode(monkeypatch: MonkeyPatch) -> None:
    """Check that we exit correctly based on different parameters."""
    # Monkeypatch everything we don't want to check in this test
    monkeypatch.setattr(
        "pylint.config._pylint_config.utils.get_and_validate_format", lambda: "toml"
    )
    monkeypatch.setattr(
        "pylint.config._pylint_config.utils.get_minimal_setting", lambda: False
    )
    monkeypatch.setattr(
        "pylint.config._pylint_config.utils.get_and_validate_output_file",
        lambda: (False, Path()),
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
    # Monkeypatch everything we don't want to check in this test
    monkeypatch.setattr(
        "pylint.config._pylint_config.utils.get_minimal_setting", lambda: False
    )
    monkeypatch.setattr(
        "pylint.config._pylint_config.utils.get_and_validate_output_file",
        lambda: (False, Path()),
    )

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


def test_writing_to_output_file(
    monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]
) -> None:
    """Check that we can write to an output file."""
    # Monkeypatch everything we don't want to check in this test
    monkeypatch.setattr(
        "pylint.config._pylint_config.utils.get_and_validate_format", lambda: "toml"
    )
    monkeypatch.setattr(
        "pylint.config._pylint_config.utils.get_minimal_setting", lambda: False
    )

    # Set up a temporary file to write to
    tempfile_name = Path(tempfile.gettempdir()) / "CONFIG"
    if tempfile_name.exists():
        os.remove(tempfile_name)

    # Set the answers needed for the input() calls
    answers = iter(
        [
            # Don't write to file
            "no",
            # Write to file
            "yes",
            str(tempfile_name),
            # Don't overwrite file
            "yes",
            str(tempfile_name),
            "misspelled-no",
            "no",
            # Don't overwrite file with default
            "yes",
            str(tempfile_name),
            "",
            # Overwrite file
            "yes",
            str(tempfile_name),
            "yes",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda x: next(answers))

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="NOTE:.*", category=UserWarning)
        # Check no writing to file
        Run(["generate", "--interactive"], exit=False)
        captured = capsys.readouterr()
        assert "[tool.pylint.main]" in captured.out

        # Test writing to file
        assert not tempfile_name.exists()
        Run(["generate", "--interactive"], exit=False)
        captured = capsys.readouterr()
        assert tempfile_name.exists()

        last_modified = tempfile_name.stat().st_mtime

        # Test not overwriting file
        Run(["generate", "--interactive"], exit=False)
        captured = capsys.readouterr()
        assert last_modified == tempfile_name.stat().st_mtime

        # Test not overwriting file with default value
        Run(["generate", "--interactive"], exit=False)
        captured = capsys.readouterr()
        assert last_modified == tempfile_name.stat().st_mtime

        # Test overwriting
        Run(["generate", "--interactive"], exit=False)
        captured = capsys.readouterr()
        assert last_modified != tempfile_name.stat().st_mtime


def test_writing_minimal_file(
    monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]
) -> None:
    """Check that we can write a minimal file."""
    # Monkeypatch everything we don't want to check in this test
    monkeypatch.setattr(
        "pylint.config._pylint_config.utils.get_and_validate_format", lambda: "toml"
    )
    monkeypatch.setattr(
        "pylint.config._pylint_config.utils.get_and_validate_output_file",
        lambda: (False, Path()),
    )

    # Set the answers needed for the input() calls
    answers = iter(["no", "yes"])
    monkeypatch.setattr("builtins.input", lambda x: next(answers))

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="NOTE:.*", category=UserWarning)
        # Check not minimal has comments
        Run(["generate", "--interactive"], exit=False)
        captured = capsys.readouterr()
        assert any(line.startswith("#") for line in captured.out.splitlines())

        # Check minimal doesn't have comments and no default values
        Run(
            [
                "--load-plugins=pylint.extensions.docparams",
                "--accept-no-return-doc=y",
                "generate",
                "--interactive",
            ],
            exit=False,
        )
        captured = capsys.readouterr()
        assert not any(i.startswith("#") for i in captured.out.split("\n"))
        assert "accept-no-return-doc" not in captured.out
