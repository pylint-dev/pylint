# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

# pylint: disable=redefined-outer-name

import pytest

from pylint.constants import PY38_PLUS
from pylint.interfaces import HIGH, INFERENCE
from pylint.message import Message
from pylint.testutils.output_line import MalformedOutputLineException, OutputLine


@pytest.fixture()
def message():
    def inner(confidence=HIGH):
        return Message(
            symbol="missing-docstring",
            msg_id="C0123",
            location=[
                "abspath",
                "path",
                "module",
                "obj",
                "line",
                "column",
            ],
            msg="msg",
            confidence=confidence,
        )

    return inner


def test_output_line():
    output_line = OutputLine(
        symbol="missing-docstring",
        lineno=0,
        column=0,
        object="",
        msg="Missing docstring's bad.",
        confidence=HIGH,
    )
    assert output_line.symbol == "missing-docstring"


def test_output_line_from_message(message):
    output_line = OutputLine.from_msg(message())
    assert output_line.symbol == "missing-docstring"
    assert output_line.msg == "msg"


@pytest.mark.parametrize("confidence", [HIGH, INFERENCE])
def test_output_line_to_csv(confidence, message):
    output_line = OutputLine.from_msg(message(confidence))
    csv = output_line.to_csv()
    expected_column = "column" if PY38_PLUS else ""
    assert csv == (
        "missing-docstring",
        "line",
        expected_column,
        "obj",
        "msg",
        confidence.name,
    )


def test_output_line_from_csv_error():
    with pytest.raises(
        MalformedOutputLineException,
        match="msg-symbolic-name:42:27:MyClass.my_function:The message",
    ):
        OutputLine.from_csv("'missing-docstring', 'line', 'column', 'obj', 'msg'")
    with pytest.raises(
        MalformedOutputLineException, match="symbol='missing-docstring' ?"
    ):
        csv = ("missing-docstring", "line", "column", "obj", "msg")
        OutputLine.from_csv(csv)


@pytest.mark.parametrize(
    "confidence,expected_confidence", [[None, "HIGH"], ["INFERENCE", "INFERENCE"]]
)
def test_output_line_from_csv(confidence, expected_confidence):
    proper_csv = (
        "missing-docstring",
        "1",
        "2",
        "obj",
        "msg",
    )
    if confidence is not None:
        proper_csv += (confidence,)
    output_line = OutputLine.from_csv(proper_csv)
    expected_column = "2" if PY38_PLUS else ""
    assert output_line == OutputLine(
        symbol="missing-docstring",
        lineno=1,
        column=expected_column,
        object="obj",
        msg="msg",
        confidence=expected_confidence,
    )
