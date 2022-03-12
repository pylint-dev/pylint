# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

# pylint: disable=redefined-outer-name

from typing import Callable, Optional

import pytest

from pylint.constants import PY38_PLUS
from pylint.interfaces import HIGH, INFERENCE, Confidence
from pylint.message import Message
from pylint.testutils.output_line import MalformedOutputLineException, OutputLine
from pylint.typing import MessageLocationTuple


@pytest.fixture()
def message() -> Callable:
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


def test_output_line_from_message(message: Callable) -> None:
    """Test that the OutputLine NamedTuple is instantiated correctly with from_msg."""
    expected_column = 2 if PY38_PLUS else 0

    output_line = OutputLine.from_msg(message())
    assert output_line.symbol == "missing-docstring"
    assert output_line.lineno == 1
    assert output_line.column == expected_column
    assert output_line.end_lineno == 1
    assert output_line.end_column == 3
    assert output_line.object == "obj"
    assert output_line.msg == "msg"
    assert output_line.confidence == "HIGH"

    output_line_with_end = OutputLine.from_msg(message(), True)
    assert output_line_with_end.symbol == "missing-docstring"
    assert output_line_with_end.lineno == 1
    assert output_line_with_end.column == expected_column
    assert output_line_with_end.end_lineno == 1
    assert output_line_with_end.end_column == 3
    assert output_line_with_end.object == "obj"
    assert output_line_with_end.msg == "msg"
    assert output_line_with_end.confidence == "HIGH"

    output_line_without_end = OutputLine.from_msg(message(), False)
    assert output_line_without_end.symbol == "missing-docstring"
    assert output_line_without_end.lineno == 1
    assert output_line_without_end.column == expected_column
    assert output_line_without_end.end_lineno is None
    assert output_line_without_end.end_column is None
    assert output_line_without_end.object == "obj"
    assert output_line_without_end.msg == "msg"
    assert output_line_without_end.confidence == "HIGH"


@pytest.mark.parametrize("confidence", [HIGH, INFERENCE])
def test_output_line_to_csv(confidence: Confidence, message: Callable) -> None:
    """Test that the OutputLine NamedTuple is instantiated correctly with from_msg
    and then converted to csv.
    """
    output_line = OutputLine.from_msg(message(confidence), True)
    csv = output_line.to_csv()
    expected_column = "2" if PY38_PLUS else "0"
    assert csv == (
        "missing-docstring",
        "1",
        expected_column,
        "1",
        "3",
        "obj",
        "msg",
        confidence.name,
    )

    output_line_without_end = OutputLine.from_msg(message(confidence), False)
    csv = output_line_without_end.to_csv()
    expected_column = "2" if PY38_PLUS else "0"
    assert csv == (
        "missing-docstring",
        "1",
        expected_column,
        "None",
        "None",
        "obj",
        "msg",
        confidence.name,
    )


def test_output_line_from_csv_error() -> None:
    """Test that errors are correctly raised for incorrect OutputLine's."""
    # Test a csv-string which does not have a number for line and column
    with pytest.raises(
        MalformedOutputLineException,
        match="msg-symbolic-name:42:27:MyClass.my_function:The message",
    ):
        OutputLine.from_csv("'missing-docstring', 'line', 'column', 'obj', 'msg'", True)
    # Test a tuple which does not have a number for line and column
    with pytest.raises(
        MalformedOutputLineException, match="symbol='missing-docstring' ?"
    ):
        csv = ("missing-docstring", "line", "column", "obj", "msg")
        OutputLine.from_csv(csv, True)
    # Test a csv-string that is too long
    with pytest.raises(
        MalformedOutputLineException,
        match="msg-symbolic-name:42:27:MyClass.my_function:The message",
    ):
        OutputLine.from_csv(
            "'missing-docstring', 1, 2, 'obj', 'msg', 'func', 'message', 'conf', 'too_long'",
            True,
        )


@pytest.mark.parametrize(
    "confidence,expected_confidence", [[None, "UNDEFINED"], ["INFERENCE", "INFERENCE"]]
)
def test_output_line_from_csv_deprecated(
    confidence: Optional[str], expected_confidence: str
) -> None:
    """Test that the OutputLine NamedTuple is instantiated correctly with from_csv.
    Test OutputLine's of length 5 or 6.
    """
    if confidence:
        proper_csv = [
            "missing-docstring",
            "1",
            "2",
            "obj",
            "msg",
            confidence,
        ]
    else:
        proper_csv = ["missing-docstring", "1", "2", "obj", "msg"]
    with pytest.warns(DeprecationWarning) as records:
        output_line = OutputLine.from_csv(proper_csv, True)
        assert len(records) == 1

    expected_column = 2 if PY38_PLUS else 0
    assert output_line == OutputLine(
        symbol="missing-docstring",
        lineno=1,
        column=expected_column,
        end_lineno=None,
        end_column=None,
        object="obj",
        msg="msg",
        confidence=expected_confidence,
    )


def test_output_line_from_csv() -> None:
    """Test that the OutputLine NamedTuple is instantiated correctly with from_csv.
    Test OutputLine of length 8.
    """
    proper_csv = [
        "missing-docstring",
        "1",
        "2",
        "1",
        "None",
        "obj",
        "msg",
        "HIGH",
    ]
    expected_column = 2 if PY38_PLUS else 0

    output_line = OutputLine.from_csv(proper_csv)
    assert output_line == OutputLine(
        symbol="missing-docstring",
        lineno=1,
        column=expected_column,
        end_lineno=1,
        end_column=None,
        object="obj",
        msg="msg",
        confidence="HIGH",
    )
    output_line_with_end = OutputLine.from_csv(proper_csv, True)
    assert output_line_with_end == OutputLine(
        symbol="missing-docstring",
        lineno=1,
        column=expected_column,
        end_lineno=1,
        end_column=None,
        object="obj",
        msg="msg",
        confidence="HIGH",
    )
    output_line_without_end = OutputLine.from_csv(proper_csv, False)
    assert output_line_without_end == OutputLine(
        symbol="missing-docstring",
        lineno=1,
        column=expected_column,
        end_lineno=None,
        end_column=None,
        object="obj",
        msg="msg",
        confidence="HIGH",
    )
