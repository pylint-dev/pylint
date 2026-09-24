# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

# pylint: disable=redefined-outer-name,unidiomatic-typecheck

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, NoReturn
from unittest import mock
from unittest.mock import patch

import pytest
from pytest import CaptureFixture

from pylint import reporters
from pylint.lint.pylinter import (
    FORCE_COLOR,
    MANAGER,
    NO_COLOR,
    WARN_BOTH_COLOR_SET,
    WARN_FORCE_COLOR_SET,
    WARN_NO_COLOR_SET,
    PyLinter,
    _read_color_env,
)
from pylint.lint.run import Run
from pylint.reporters import MultiReporter, ReporterWarning
from pylint.reporters.text import (
    ColorizedTextReporter,
    ParseableTextReporter,
    TextReporter,
)
from pylint.utils import FileState


def raise_exception(*args: Any, **kwargs: Any) -> NoReturn:
    raise ValueError


@patch.object(FileState, "iter_spurious_suppression_messages", raise_exception)
def test_crash_in_file(
    linter: PyLinter, capsys: CaptureFixture[str], tmp_path: Path
) -> None:
    linter.crash_file_path = str(tmp_path / "pylint-crash-%Y")
    linter.check([__file__])
    out, err = capsys.readouterr()
    assert not out
    assert not err
    files = os.listdir(tmp_path)
    assert len(files) == 1
    assert "pylint-crash-20" in str(files[0])
    assert any(m.symbol == "fatal" for m in linter.reporter.messages)


def test_crash_during_linting(
    linter: PyLinter, capsys: CaptureFixture[str], tmp_path: Path
) -> None:
    with mock.patch(
        "pylint.lint.PyLinter.check_astroid_module", side_effect=RuntimeError
    ):
        linter.crash_file_path = str(tmp_path / "pylint-crash-%Y")
        linter.check([__file__])
        out, err = capsys.readouterr()
        assert not out
        assert not err
        files = os.listdir(tmp_path)
        assert len(files) == 1
        assert "pylint-crash-20" in str(files[0])
        assert any(m.symbol == "astroid-error" for m in linter.reporter.messages)


def test_open_pylinter_denied_modules(linter: PyLinter) -> None:
    """Test PyLinter open() adds ignored modules to Astroid manager deny list."""
    MANAGER.module_denylist = {"mod1"}
    try:
        linter.config.ignored_modules = ["mod2", "mod3"]
        linter.open()
        assert MANAGER.module_denylist == {"mod1", "mod2", "mod3"}
    finally:
        MANAGER.module_denylist = set()


def test_open_pylinter_prefer_stubs(linter: PyLinter) -> None:
    try:
        linter.config.prefer_stubs = True
        linter.open()
        assert MANAGER.prefer_stubs
    finally:
        MANAGER.prefer_stubs = False


@pytest.fixture
def color_linter() -> PyLinter:
    """A linter with the default reporters registered."""
    linter = PyLinter()
    reporters.initialize(linter)
    return linter


def _load_reporters(linter: PyLinter, reporter_names: str) -> None:
    """Load reporters the way ``Run`` does, reading the color variables first."""
    linter._color_env = _read_color_env()
    linter._load_reporters(reporter_names)


def test_no_color_disables_colorized_on_stdout(
    color_linter: PyLinter, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(NO_COLOR, "1")
    with pytest.warns(ReporterWarning, match=WARN_NO_COLOR_SET):
        _load_reporters(color_linter, "colorized")
    assert type(color_linter.reporter) is TextReporter


def test_no_color_keeps_text_on_stdout(
    color_linter: PyLinter, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(NO_COLOR, "1")
    _load_reporters(color_linter, "text")
    assert type(color_linter.reporter) is TextReporter


def test_force_color_enables_colorized_on_stdout(
    color_linter: PyLinter, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(FORCE_COLOR, "1")
    with pytest.warns(ReporterWarning, match=WARN_FORCE_COLOR_SET):
        _load_reporters(color_linter, "text")
    assert type(color_linter.reporter) is ColorizedTextReporter


def test_force_color_keeps_colorized_on_stdout(
    color_linter: PyLinter, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(FORCE_COLOR, "1")
    _load_reporters(color_linter, "colorized")
    assert type(color_linter.reporter) is ColorizedTextReporter


def test_force_color_keeps_other_text_formats(
    color_linter: PyLinter, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(FORCE_COLOR, "1")
    with pytest.warns(DeprecationWarning, match="parseable output format"):
        _load_reporters(color_linter, "parseable")
    assert type(color_linter.reporter) is ParseableTextReporter


def test_no_color_wins_over_force_color(
    color_linter: PyLinter, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(NO_COLOR, "1")
    monkeypatch.setenv(FORCE_COLOR, "1")
    with pytest.warns(ReporterWarning) as record:
        _load_reporters(color_linter, "colorized")
    assert [str(w.message) for w in record] == [
        WARN_BOTH_COLOR_SET,
        WARN_NO_COLOR_SET,
    ]
    assert type(color_linter.reporter) is TextReporter


def test_empty_color_variables_are_ignored(
    color_linter: PyLinter, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(NO_COLOR, "")
    monkeypatch.setenv(FORCE_COLOR, "")
    _load_reporters(color_linter, "colorized")
    assert type(color_linter.reporter) is ColorizedTextReporter
    _load_reporters(color_linter, "text")
    assert type(color_linter.reporter) is TextReporter


@pytest.mark.parametrize("env_var", [NO_COLOR, FORCE_COLOR])
def test_color_variables_ignore_reporters_writing_to_a_file(
    color_linter: PyLinter,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    env_var: str,
) -> None:
    monkeypatch.setenv(env_var, "1")
    _load_reporters(
        color_linter,
        f"colorized:{tmp_path / 'colorized.txt'},text:{tmp_path / 'text.txt'}",
    )
    assert isinstance(color_linter.reporter, MultiReporter)
    try:
        assert [type(r) for r in color_linter.reporter._sub_reporters] == [
            ColorizedTextReporter,
            TextReporter,
        ]
    finally:
        color_linter.reporter.close_output_files()


def test_color_variables_only_change_the_stdout_reporter(
    color_linter: PyLinter, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv(NO_COLOR, "1")
    with pytest.warns(ReporterWarning, match=WARN_NO_COLOR_SET):
        _load_reporters(
            color_linter, f"colorized:{tmp_path / 'colorized.txt'},colorized"
        )
    assert isinstance(color_linter.reporter, MultiReporter)
    try:
        assert [type(r) for r in color_linter.reporter._sub_reporters] == [
            ColorizedTextReporter,
            TextReporter,
        ]
    finally:
        color_linter.reporter.close_output_files()


def test_pylinter_api_ignores_color_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(FORCE_COLOR, "1")
    linter = PyLinter()
    reporters.initialize(linter)
    linter._load_reporters("text")
    assert type(linter.reporter) is TextReporter


@pytest.fixture
def unused_import_args(tmp_path: Path) -> list[str]:
    module = tmp_path / "unused.py"
    module.write_text("import os\n", encoding="utf-8")
    return [str(module), "--rcfile=/dev/null", "--disable=all", "--enable=W0611"]


def test_run_force_color_colorizes_the_default_reporter(
    monkeypatch: pytest.MonkeyPatch,
    capsys: CaptureFixture[str],
    unused_import_args: list[str],
) -> None:
    monkeypatch.setenv(FORCE_COLOR, "1")
    with pytest.warns(ReporterWarning, match=WARN_FORCE_COLOR_SET):
        run = Run(unused_import_args, exit=False)
    assert type(run.linter.reporter) is ColorizedTextReporter
    assert "\x1b[" in capsys.readouterr().out


def test_run_color_variables_ignore_output_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: CaptureFixture[str],
    unused_import_args: list[str],
) -> None:
    monkeypatch.setenv(FORCE_COLOR, "1")
    output = tmp_path / "report.txt"
    run = Run([*unused_import_args, f"--output={output}"], exit=False)
    assert type(run.linter.reporter) is TextReporter
    report = output.read_text(encoding="utf-8")
    assert "unused-import" in report
    assert "\x1b[" not in report
    assert capsys.readouterr().out == ""


def test_run_color_variables_ignore_given_reporter(
    monkeypatch: pytest.MonkeyPatch,
    capsys: CaptureFixture[str],
    unused_import_args: list[str],
) -> None:
    monkeypatch.setenv(FORCE_COLOR, "1")
    reporter = TextReporter()
    run = Run(unused_import_args, reporter=reporter, exit=False)
    assert run.linter.reporter is reporter
    assert "\x1b[" not in capsys.readouterr().out
