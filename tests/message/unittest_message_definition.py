# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import sys

from pylint.checkers import BaseChecker
from pylint.constants import WarningScope
from pylint.message import MessageDefinition


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


class TestMessagesDefinition(object):
    def assert_with_fail_msg(self, msg, expected=True):
        fail_msg = "With minversion='{}' and maxversion='{}',".format(
            msg.minversion, msg.maxversion
        )
        fail_msg += " and the python interpreter being {} ".format(sys.version_info)
        fail_msg += "the message should{}be emitable"
        if expected:
            assert msg.may_be_emitted(), fail_msg.format(" ")
        else:
            assert not msg.may_be_emitted(), fail_msg.format(" not ")

    def get_message_definition(self):
        args = [
            FalseChecker(),
            "W1234",
            "message",
            "description",
            "msg-symbol",
            WarningScope.NODE,
        ]
        kwargs = {"minversion": None, "maxversion": None}
        return MessageDefinition(*args, **kwargs)

    def test_may_be_emitted(self):
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

    def test_repr(self):
        msg = self.get_message_definition()
        repr_str = str([msg, msg])
        assert "W1234" in repr_str
        assert "msg-symbol" in repr_str
        expected = "[MessageDefinition:msg-symbol-one (W1234), MessageDefinition:msg-symbol-two (W1235)]"
        assert str(FalseChecker().messages) == expected

    def test_format_help(self):
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
