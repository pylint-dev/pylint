# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Test for the JSON reporter."""

from __future__ import annotations

import json
from io import StringIO
from typing import Any

import pytest

from pylint import checkers
from pylint.interfaces import UNDEFINED
from pylint.lint import PyLinter
from pylint.message import Message
from pylint.reporters import JSONReporter
from pylint.reporters.ureports.nodes import EvaluationSection
from pylint.typing import MessageLocationTuple

expected_score_message = "Expected score message"


def test_simple_json_output_no_score() -> None:
    """Test JSON reporter with no score."""
    message = {
        "msg": "line-too-long",
        "line": 1,
        "args": (1, 2),
        "end_line": None,
        "end_column": None,
    }
    expected = [
        {
            "type": "convention",
            "module": "0123",
            "obj": "",
            "line": 1,
            "column": 0,
            "endLine": None,
            "endColumn": None,
            "path": "0123",
            "symbol": "line-too-long",
            "message": "Line too long (1/2)",
            "message-id": "C0301",
        }
    ]
    report = get_linter_result(score=False, message=message)
    assert len(report) == 1
    assert json.dumps(report) == json.dumps(expected)


def test_simple_json_output_no_score_with_end_line() -> None:
    """Test JSON reporter with no score with end_line and end_column."""
    message = {
        "msg": "line-too-long",
        "line": 1,
        "args": (1, 2),
        "end_line": 1,
        "end_column": 4,
    }
    expected = [
        {
            "type": "convention",
            "module": "0123",
            "obj": "",
            "line": 1,
            "column": 0,
            "endLine": 1,
            "endColumn": 4,
            "path": "0123",
            "symbol": "line-too-long",
            "message": "Line too long (1/2)",
            "message-id": "C0301",
        }
    ]
    report = get_linter_result(score=False, message=message)
    assert len(report) == 1
    assert json.dumps(report) == json.dumps(expected)


def get_linter_result(score: bool, message: dict[str, Any]) -> list[dict[str, Any]]:
    output = StringIO()
    reporter = JSONReporter(output)
    linter = PyLinter(reporter=reporter)
    checkers.initialize(linter)
    linter.config.persistent = 0
    linter.config.score = score
    linter.open()
    linter.set_current_module("0123")
    linter.add_message(
        message["msg"],
        line=message["line"],
        args=message["args"],
        end_lineno=message["end_line"],
        end_col_offset=message["end_column"],
    )
    # we call those methods because we didn't actually run the checkers
    if score:
        reporter.display_reports(EvaluationSection(expected_score_message))
    reporter.display_messages(None)
    report_result = json.loads(output.getvalue())
    return report_result  # type: ignore[no-any-return]


@pytest.mark.parametrize(
    "message",
    [
        pytest.param(
            Message(
                msg_id="C0111",
                symbol="missing-docstring",
                location=MessageLocationTuple(
                    # abs-path and path must be equal because one of them is removed
                    # in the JsonReporter
                    abspath=__file__,
                    path=__file__,
                    module="unittest_json_reporter",
                    obj="obj",
                    line=1,
                    column=3,
                    end_line=3,
                    end_column=5,
                ),
                msg="This is the actual message",
                confidence=UNDEFINED,
            ),
            id="everything-defined",
        )
    ],
)
def test_serialize_deserialize(message: Message) -> None:
    # TODO: 3.0: Add confidence handling, add path and abs path handling or a new JSONReporter
    json_message = JSONReporter.serialize(message)
    assert message == JSONReporter.deserialize(json_message)
