# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

# pylint: disable=redefined-outer-name

from __future__ import annotations

from typing import Protocol

import pytest

from pylint.interfaces import HIGH, INFERENCE, Confidence
from pylint.message import Message
from pylint.testutils.output_line import OutputLine
from pylint.typing import MessageLocationTuple


class _MessageCallable(Protocol):
    def __call__(self, confidence: Confidence = HIGH) -> Message: ...


@pytest.fixture()
def message() -> _MessageCallable:
    def inner(confidence: Confidence = HIGH) -> Message:
        return Message(
            symbol="missing-docstring",
            msg_id="C0123",
            location=MessageLocationTuple(
                "abspath", "path", "module", "obj", 1, 2, 1, 3
            ),
            msg="msg",
            confidence=confidence,
        )

    return inner


def test_output_line() -> None:
    """Test that the OutputLine NamedTuple is instantiated correctly."""
    output_line = OutputLine(
        symbol="missing-docstring",
        lineno=1,
        column=2,
        end_lineno=1,
        end_column=4,
        object="",
        msg="Missing docstring's bad.",
        confidence=HIGH.name,
    )
    assert output_line.symbol == "missing-docstring"
    assert output_line.lineno == 1
    assert output_line.column == 2
    assert output_line.end_lineno == 1
    assert output_line.end_column == 4
    assert output_line.object == ""
    assert output_line.msg == "Missing docstring's bad."
    assert output_line.confidence == "HIGH"


def test_output_line_from_message(message: _MessageCallable) -> None:
    """Test that the OutputLine NamedTuple is instantiated correctly with from_msg."""
    output_line = OutputLine.from_msg(message())
    assert output_line.symbol == "missing-docstring"
    assert output_line.lineno == 1
    assert output_line.column == 2
    assert output_line.end_lineno == 1
    assert output_line.end_column == 3
    assert output_line.object == "obj"
    assert output_line.msg == "msg"
    assert output_line.confidence == "HIGH"


@pytest.mark.parametrize("confidence", [HIGH, INFERENCE])
def test_output_line_to_csv(confidence: Confidence, message: _MessageCallable) -> None:
    """Test that the OutputLine NamedTuple is instantiated correctly with from_msg
    and then converted to csv.
    """
    output_line = OutputLine.from_msg(message(confidence))
    csv = output_line.to_csv()
    assert csv == (
        "missing-docstring",
        "1",
        "2",
        "1",
        "3",
        "obj",
        "msg",
        confidence.name,
    )


def test_output_line_from_csv() -> None:
    """Test that the OutputLine NamedTuple is instantiated correctly with from_csv.
    Test OutputLine of length 8.
    """
    proper_csv = ["missing-docstring", "1", "2", "1", "None", "obj", "msg", "HIGH"]

    output_line = OutputLine.from_csv(proper_csv)
    assert output_line == OutputLine(
        symbol="missing-docstring",
        lineno=1,
        column=2,
        end_lineno=1,
        end_column=None,
        object="obj",
        msg="msg",
        confidence="HIGH",
    )
