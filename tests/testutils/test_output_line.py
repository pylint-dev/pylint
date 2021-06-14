# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

# pylint: disable=redefined-outer-name

import pytest

from pylint.interfaces import HIGH
from pylint.message import Message
from pylint.testutils.output_line import MalformedOutputLineException, OutputLine


@pytest.fixture()
def message():
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
        confidence=HIGH,
    )


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
    output_line = OutputLine.from_msg(message)
    assert output_line.symbol == "missing-docstring"
    assert output_line.msg == "msg"


def test_output_line_to_csv(message):
    output_line = OutputLine.from_msg(message)
    csv = output_line.to_csv()
    assert csv == ("missing-docstring", "line", "column", "obj", "msg")


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
    "confidence,expected", [[None, "HIGH"], ["INFERENCE", "INFERENCE"]]
)
def test_output_line_from_csv(confidence, expected):
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
    assert output_line == OutputLine(
        symbol="missing-docstring",
        lineno=1,
        column="2",
        object="obj",
        msg="msg",
        confidence=expected,
    )
