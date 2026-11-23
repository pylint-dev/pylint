# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the JUnit XML reporter."""

from __future__ import annotations

import platform
from io import StringIO
from pathlib import Path

import pytest
from pytest_remaster import CaseData, GoldenMaster, discover_test_cases

from pylint.interfaces import HIGH
from pylint.message import Message
from pylint.reporters.junit_reporter import JUnitReporter
from pylint.testutils._run import _Run as Run
from pylint.typing import MessageLocationTuple

CASES_DIR = Path(__file__).parent / "junit_data"


@pytest.mark.parametrize(
    "case",
    discover_test_cases(CASES_DIR, is_case=lambda path: path.parent == CASES_DIR),
)
def test_full_output(
    case: CaseData,
    golden_master: GoldenMaster,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Lint each case directory and compare the whole XML with ``expected.xml``."""
    monkeypatch.chdir(case.input)
    Run(["--output-format=junit", "--persistent=no", "."], exit=False)
    golden_master.check(
        capsys.readouterr().out,
        case.expected(suffix=".xml"),
        # PyPy words and positions syntax errors differently from CPython, so
        # ``syntax_error`` has an ``expected.pypy.xml`` override. Remastering
        # rewrites the file that was compared, so each interpreter keeps its own.
        dimensions={"implementation": platform.python_implementation().lower()},
        normalizer=lambda output: output.replace("\\", "/"),
    )


def test_message_without_module(golden_master: GoldenMaster) -> None:
    """A message with an empty module is reported under its path instead.

    A real run always sets the module, so this case cannot be a directory in
    ``junit_data``.
    """
    output = StringIO()
    reporter = JUnitReporter(output)
    reporter.handle_message(
        Message(
            msg_id="C0301",
            symbol="line-too-long",
            location=MessageLocationTuple(
                abspath="standalone.py",
                path="standalone.py",
                module="",
                obj="",
                line=7,
                column=2,
                end_line=None,
                end_column=None,
            ),
            msg="Line too long (100/80)",
            confidence=HIGH,
        )
    )
    reporter.display_messages(None)
    golden_master.check(output.getvalue(), CASES_DIR / "message_without_module.xml")
