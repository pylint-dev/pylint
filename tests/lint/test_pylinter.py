# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import os
from io import StringIO
from pathlib import Path
from typing import Any, NoReturn
from unittest import mock
from unittest.mock import patch

from pytest import CaptureFixture

from pylint.lint.pylinter import MANAGER, PyLinter
from pylint.reporters import MultiReporter
from pylint.reporters.text import ColorizedTextReporter, TextReporter
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


def test_pass_fail_on_config_to_color_reporter_direct() -> None:
    """Test that fail_on_symbols are passed to a direct ColorizedTextReporter."""
    linter = PyLinter()
    reporter = ColorizedTextReporter(StringIO())
    linter.set_reporter(reporter)
    linter.fail_on_symbols = ["missing-function-docstring"]
    linter.pass_fail_on_config_to_color_reporter()
    assert reporter.fail_on_symbols == ["missing-function-docstring"]


def test_pass_fail_on_config_to_color_reporter_non_colorized() -> None:
    """Test that a non-colorized reporter is not affected."""
    linter = PyLinter()
    reporter = TextReporter(StringIO())
    linter.set_reporter(reporter)
    linter.fail_on_symbols = ["missing-function-docstring"]
    # Should not raise any error even though TextReporter has no set_fail_on_symbols
    linter.pass_fail_on_config_to_color_reporter()


def test_pass_fail_on_config_to_color_reporter_multi_reporter() -> None:
    """Regression test: fail_on_symbols must be passed to ColorizedTextReporter
    instances inside a MultiReporter (not to the MultiReporter itself).

    See: https://github.com/pylint-dev/pylint/issues/XXXX
    """
    linter = PyLinter()
    colorized_reporter1 = ColorizedTextReporter(StringIO())
    colorized_reporter2 = ColorizedTextReporter(StringIO())
    multi_reporter = MultiReporter(
        [colorized_reporter1, colorized_reporter2],
        close_output_files=lambda: None,
    )
    linter.set_reporter(multi_reporter)
    linter.fail_on_symbols = ["missing-function-docstring"]
    # Must not raise AttributeError by calling set_fail_on_symbols on MultiReporter
    linter.pass_fail_on_config_to_color_reporter()
    assert colorized_reporter1.fail_on_symbols == ["missing-function-docstring"]
    assert colorized_reporter2.fail_on_symbols == ["missing-function-docstring"]


def test_pass_fail_on_config_to_color_reporter_multi_reporter_mixed() -> None:
    """Test that only ColorizedTextReporter instances inside MultiReporter receive
    fail_on_symbols; non-colorized reporters are skipped without error.
    """
    linter = PyLinter()
    colorized_reporter = ColorizedTextReporter(StringIO())
    text_reporter = TextReporter(StringIO())
    multi_reporter = MultiReporter(
        [colorized_reporter, text_reporter],
        close_output_files=lambda: None,
    )
    linter.set_reporter(multi_reporter)
    linter.fail_on_symbols = ["missing-function-docstring"]
    # Must not raise AttributeError for the non-colorized TextReporter
    linter.pass_fail_on_config_to_color_reporter()
    assert colorized_reporter.fail_on_symbols == ["missing-function-docstring"]
