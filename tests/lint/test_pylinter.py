# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import os
from pathlib import Path
from typing import Any, NoReturn
from unittest import mock
from unittest.mock import patch

from pytest import CaptureFixture

from pylint.lint.pylinter import MANAGER, PyLinter
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
