# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

import sys
from unittest import mock

import pytest

from pylint.checkers import BaseChecker
from pylint.constants import WarningScope
from pylint.exceptions import InvalidMessageError
from pylint.message import MessageDefinition


@pytest.mark.parametrize(
    "msgid,expected",
    [
        ("Q1234", "Bad message type Q in 'Q1234'"),
        ("W12345", "Invalid message id 'W12345'"),
    ],
)
def test_create_invalid_message_type(msgid, expected):
    checker_mock = mock.Mock(name="Checker")
    checker_mock.name = "checker"

    with pytest.raises(InvalidMessageError) as invalid_message_error:
        MessageDefinition.check_msgid(msgid)
    with pytest.raises(InvalidMessageError) as other_invalid_message_error:
        MessageDefinition(checker_mock, msgid, "msg", "descr", "symbol", "scope")
    assert str(invalid_message_error.value) == expected
    assert str(other_invalid_message_error.value) == expected


class FalseChecker(BaseChecker):
    name = "FalseChecker"
    msgs = {
        "W1234": ("message one", "msg-symbol-one", "msg description"),
        "W1235": (
            "message two",
            "msg-symbol-two",
            "msg description",
            {"old_names": [("W1230", "msg-symbol-one")]},
        ),
    }


class TestMessagesDefinition:
    @staticmethod
    def assert_with_fail_msg(msg: MessageDefinition, expected: bool = True) -> None:
        fail_msg = (
            f"With minversion='{msg.minversion}' and maxversion='{msg.maxversion}',"
            f" and the python interpreter being {sys.version_info} "
            "the message should{}be emitable"
        )
        if expected:
            assert msg.may_be_emitted(), fail_msg.format(" ")
        else:
            assert not msg.may_be_emitted(), fail_msg.format(" not ")

    @staticmethod
    def get_message_definition() -> MessageDefinition:
        kwargs = {"minversion": None, "maxversion": None}
        return MessageDefinition(
            FalseChecker(),
            "W1234",
            "message",
            "description",
            "msg-symbol",
            WarningScope.NODE,
            **kwargs,
        )

    def test_may_be_emitted(self) -> None:
        major = sys.version_info.major
        minor = sys.version_info.minor
        msg = self.get_message_definition()
        self.assert_with_fail_msg(msg, expected=True)
        msg.minversion = (major, minor - 1)
        msg.maxversion = (major, minor + 1)
        self.assert_with_fail_msg(msg, expected=True)
        msg.minversion = (major, minor + 1)
        self.assert_with_fail_msg(msg, expected=False)
        msg.minversion = (major, minor - 1)
        self.assert_with_fail_msg(msg, expected=True)
        msg.maxversion = (major, minor - 1)
        self.assert_with_fail_msg(msg, expected=False)

    def test_repr(self) -> None:
        msg = self.get_message_definition()
        repr_str = str([msg, msg])
        assert "W1234" in repr_str
        assert "msg-symbol" in repr_str
        expected = "[MessageDefinition:msg-symbol-one (W1234), MessageDefinition:msg-symbol-two (W1235)]"
        assert str(FalseChecker().messages) == expected

    def test_str(self) -> None:
        msg = self.get_message_definition()
        str_msg = str(msg)
        assert "W1234" in str_msg
        assert "msg-symbol" in str_msg
        expected = """MessageDefinition:msg-symbol-one (W1234):
message one msg description"""
        assert str(FalseChecker().messages[0]) == expected

    def test_format_help(self) -> None:
        msg = self.get_message_definition()
        major = sys.version_info.major
        minor = sys.version_info.minor
        msg.minversion = (major, minor - 1)
        msg.maxversion = (major, minor + 1)
        format_str_checker_ref = msg.format_help(checkerref=False)
        format_str = msg.format_help(checkerref=True)
        assert str(minor - 1) in format_str
        assert str(major + 1) in format_str_checker_ref
        expected_format_help = """:msg-symbol-one (W1234): *message one*
  msg description"""
        assert FalseChecker().messages[0].format_help() == expected_format_help
