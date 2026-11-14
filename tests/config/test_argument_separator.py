# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the command line argument separator."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from pylint.lint import Run
from pylint.lint.run import _PylintConfigRun

BASE_ARGS = [
    "--rcfile=pylintrc",
    "--persistent=no",
    "--disable=all",
    "--enable=undefined-variable",
    "--reports=no",
    "--score=no",
]


@pytest.fixture(name="working_directory")
def fixture_working_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Use an empty configuration in an isolated working directory."""
    (tmp_path / "pylintrc").write_text("", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _run(*args: str) -> Run:
    return Run([*BASE_ARGS, *args], exit=False)


@pytest.mark.parametrize(
    "filename",
    [
        "-example.py",
        "--version",
        "--help",
        "--rcfile",
        "--rcfile=missing",
        "--output",
        "--load-plugins",
        "--init-hook",
        "--enable=all",
        "--",
    ],
)
def test_file_after_separator(
    working_directory: Path, filename: str, capsys: pytest.CaptureFixture[str]
) -> None:
    (working_directory / filename).write_text("missing()\n", encoding="utf-8")
    runner = _run("--", filename)
    assert runner.linter.config.files == [filename]
    assert runner.linter.msg_status == 2
    captured = capsys.readouterr()
    assert "Undefined variable 'missing'" in captured.out
    assert not captured.err


@pytest.mark.parametrize("filename", ["-example.py", "--version"])
def test_cli_file_after_separator(working_directory: Path, filename: str) -> None:
    (working_directory / filename).write_text("missing()\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "pylint", *BASE_ARGS, "--", filename],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "Undefined variable 'missing'" in result.stdout
    assert not result.stderr


def test_options_between_files(working_directory: Path) -> None:
    for filename in ("first.py", "second.py"):
        (working_directory / filename).write_text("missing()\n", encoding="utf-8")
    runner = _run("first.py", "--max-line-length=90", "second.py")
    assert runner.linter.config.files == ["first.py", "second.py"]
    assert runner.linter.config.max_line_length == 90
    assert runner.linter.stats.by_msg == {"undefined-variable": 2}


def test_unknown_option_before_separator(
    working_directory: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (working_directory / "-example.py").write_text("", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        _run("--unknown-option", "--", "-example.py")
    assert exc.value.code == 32
    stderr = capsys.readouterr().err
    assert "Unrecognized option found: unknown-option" in stderr
    assert "example.py" not in stderr


@pytest.mark.parametrize("config_format", ["rc", "toml"])
def test_separator_inputs_override_configured_files(
    working_directory: Path, config_format: str
) -> None:
    for filename in ("ignored.py", "first.py", "-second.py", "-third.py"):
        (working_directory / filename).write_text("missing()\n", encoding="utf-8")
    if config_format == "rc":
        config_file = "pylintrc"
        config = "[MAIN]\nfiles=ignored.py\n"
    else:
        config_file = "pyproject.toml"
        config = '[tool.pylint.main]\nfiles=["ignored.py"]\n'
    (working_directory / config_file).write_text(config, encoding="utf-8")
    runner = _run(f"--rcfile={config_file}", "first.py", "--", "-*.py")
    assert runner.linter.config.files[0] == "first.py"
    assert set(runner.linter.config.files) == {"first.py", "-second.py", "-third.py"}
    assert runner.linter.stats.by_msg == {"undefined-variable": 3}


@pytest.mark.parametrize("from_config", [False, True])
def test_empty_separator_keeps_inputs(
    working_directory: Path, from_config: bool
) -> None:
    (working_directory / "example.py").write_text("missing()\n", encoding="utf-8")
    args: tuple[str, ...]
    if from_config:
        (working_directory / "pylintrc").write_text(
            "[MAIN]\nfiles=example.py\n", encoding="utf-8"
        )
        args = ("--",)
    else:
        args = ("example.py", "--")
    runner = _run(*args)
    assert runner.linter.config.files == ["example.py"]
    assert runner.linter.msg_status == 2


@pytest.mark.usefixtures("working_directory")
def test_empty_separator_without_inputs(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        _run("--")
    assert exc.value.code == 32
    assert "No files to lint" in capsys.readouterr().out


@pytest.mark.usefixtures("working_directory")
def test_missing_file_after_separator(capsys: pytest.CaptureFixture[str]) -> None:
    runner = _run("--enable=fatal", "--", "-missing.py")
    assert runner.linter.config.files == ["-missing.py"]
    assert runner.linter.stats.by_msg == {"fatal": 1}
    assert runner.linter.msg_status == 1
    captured = capsys.readouterr()
    assert "F0001" in captured.out
    assert not captured.err


@pytest.mark.usefixtures("working_directory")
def test_version_before_separator(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        _run("--version", "--", "-example.py")
    assert exc.value.code == 0
    assert capsys.readouterr().out.startswith("pylint ")


@pytest.mark.usefixtures("working_directory")
@pytest.mark.parametrize("separator", [False, True])
def test_pylint_config_subcommand(
    separator: bool, capsys: pytest.CaptureFixture[str]
) -> None:
    args = ["--rcfile=pylintrc", "generate"]
    if separator:
        args.append("--")
    with pytest.warns(UserWarning, match="experimental"):
        with pytest.raises(SystemExit) as exc:
            _PylintConfigRun(args)
    assert exc.value.code == 32
    assert "--interactive" in capsys.readouterr().out
