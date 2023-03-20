# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import os
from pathlib import Path
from typing import Any, NoReturn
from unittest import mock
from unittest.mock import patch

from pytest import CaptureFixture

from pylint.lint.pylinter import PyLinter
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
