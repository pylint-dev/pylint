# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import io
import os
import sys
import warnings
from pathlib import Path
from typing import Any, NoReturn
from unittest import mock
from unittest.mock import patch

import pytest
from pytest import CaptureFixture

from pylint.lint.pylinter import (
    FORCE_COLOR,
    MANAGER,
    NO_COLOR,
    PY_COLORS,
    WARN_BOTH_COLOR_SET,
    PyLinter,
    _handle_force_color_no_color,
)
from pylint.reporters.text import ColorizedTextReporter, TextReporter
from pylint.utils import FileState

COLORIZED_REPORTERS = "colorized_reporters"
TEXT_REPORTERS = "text_reporters"
STDOUT_TEXT = "stdout"


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


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    if metafunc.function.__name__ != test_handle_force_color_no_color.__name__:
        return

    if (
        TEXT_REPORTERS not in metafunc.fixturenames
        or COLORIZED_REPORTERS not in metafunc.fixturenames
    ):
        warnings.warn(
            f"Missing fixture {TEXT_REPORTERS} or {COLORIZED_REPORTERS} in"
            f" {test_handle_force_color_no_color.function.__name__}??",
            stacklevel=2,
        )
        return

    parameters = []

    reporter_combinations = [
        ("file", STDOUT_TEXT),
        ("file",),
        (STDOUT_TEXT,),
        ("",),
    ]

    for tr in list(reporter_combinations):
        for cr in list(reporter_combinations):
            tr = tuple(t for t in tr if t)
            cr = tuple(t for t in cr if t)

            total_reporters = len(tr) + len(cr)
            unique_reporters = len(set(tr + cr))

            if total_reporters == 0:
                continue

            if unique_reporters != total_reporters:
                continue

            parameters.append((tuple(tr), tuple(cr)))

    metafunc.parametrize(
        f"{TEXT_REPORTERS}, {COLORIZED_REPORTERS}", parameters, ids=repr
    )


@pytest.mark.parametrize(
    "no_color",
    [True, False],
    ids=lambda no_color: f"{no_color=}",
)
@pytest.mark.parametrize(
    "py_colors",
    [True, False],
    ids=lambda py_colors: f"{py_colors=}",
)
@pytest.mark.parametrize(
    "force_color",
    [True, False],
    ids=lambda force_color: f"{force_color=}",
)
def test_handle_force_color_no_color(
    monkeypatch: pytest.MonkeyPatch,
    recwarn: pytest.WarningsRecorder,
    no_color: bool,
    py_colors: bool,
    force_color: bool,
    text_reporters: tuple[str],
    colorized_reporters: tuple[str],
) -> None:
    monkeypatch.setenv(NO_COLOR, "1" if no_color else "")
    monkeypatch.setenv(FORCE_COLOR, "1" if force_color else "")
    monkeypatch.setenv(PY_COLORS, "1" if py_colors else "")

    force_color = force_color or py_colors

    if STDOUT_TEXT in text_reporters or STDOUT_TEXT in colorized_reporters:
        monkeypatch.setattr(sys, STDOUT_TEXT, io.TextIOWrapper(io.BytesIO()))

    reporters = []
    for reporter, group in (
        (TextReporter, text_reporters),
        (ColorizedTextReporter, colorized_reporters),
    ):
        for name in group:
            if name == STDOUT_TEXT:
                reporters.append(reporter())
            if name == "file":
                reporters.append(reporter(io.TextIOWrapper(io.BytesIO())))

    _handle_force_color_no_color(reporters)

    if no_color and force_color:
        # Both NO_COLOR and FORCE_COLOR are set; expecting a warning.
        both_color_warning = [
            idx
            for idx, w in enumerate(recwarn.list)
            if WARN_BOTH_COLOR_SET in str(w.message)
        ]
        assert len(both_color_warning) == 1
        recwarn.list.pop(both_color_warning[0])

    if no_color:
        # No ColorizedTextReporter expected to be connected to stdout.
        assert all(
            not isinstance(rep, ColorizedTextReporter)
            for rep in reporters
            if rep.out.buffer is sys.stdout.buffer
        )

        if STDOUT_TEXT in colorized_reporters:
            assert len(recwarn.list) == 1  # expect a warning for overriding stdout
        else:
            assert len(recwarn.list) == 0  # no warning expected
    elif force_color:
        # No TextReporter expected to be connected to stdout.
        # pylint: disable=unidiomatic-typecheck # Want explicit type check.
        assert all(
            type(rep) is not TextReporter
            for rep in reporters
            if rep.out.buffer is sys.stdout.buffer
        )

        if STDOUT_TEXT in text_reporters:
            assert len(recwarn.list) == 1  # expect a warning for overriding stdout
        else:
            assert len(recwarn.list) == 0  # no warning expected
    else:
        assert len(recwarn.list) == 0  # no warning expected
