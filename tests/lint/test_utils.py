# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import unittest.mock
from pathlib import Path, PosixPath

import pytest

from pylint.constants import full_version
from pylint.lint.utils import get_fatal_error_message, prepare_crash_report
from pylint.testutils._run import _Run as Run


def test_prepare_crash_report(tmp_path: PosixPath) -> None:
    exception_content = "Exmessage"
    python_file = tmp_path / "myfile.py"
    python_content = "from shadok import MagicFaucet"
    with open(python_file, "w", encoding="utf8") as f:
        f.write(python_content)
    template_path = None
    try:
        raise ValueError(exception_content)
    except ValueError as ex:
        template_path = prepare_crash_report(
            ex, str(python_file), str(tmp_path / "pylint-crash-%Y.txt")
        )
    assert str(tmp_path) in str(template_path)
    with open(template_path, encoding="utf8") as f:
        template_content = f.read()
    assert python_content in template_content
    assert exception_content in template_content
    assert "in test_prepare_crash_report" in template_content
    assert "raise ValueError(exception_content)" in template_content
    assert "<details open>" in template_content
    assert full_version in template_content


def test_get_fatal_error_message() -> None:
    python_path = "mypath.py"
    crash_path = "crash.txt"
    msg = get_fatal_error_message(python_path, Path(crash_path))
    assert python_path in msg
    assert crash_path in msg
    assert "open an issue" in msg


def test_issue_template_on_fatal_errors(capsys: pytest.CaptureFixture) -> None:
    """Test that we also create an issue template if the offending exception isn't from astroid."""
    with pytest.raises(SystemExit):
        with unittest.mock.patch(
            "astroid.MANAGER.ast_from_file", side_effect=RecursionError()
        ):
            Run([__file__])
    captured = capsys.readouterr()
    assert "Fatal error while checking" in captured.out
    assert "Please open an issue" in captured.out
    assert "Traceback" in captured.err
