# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

from contextlib import redirect_stdout
from io import StringIO

import pytest

from pylint.checkers import BaseChecker
from pylint.exceptions import InvalidMessageError, UnknownMessageError
from pylint.message import MessageDefinition, MessageDefinitionStore


@pytest.fixture
def store():
    store = MessageDefinitionStore()

    class Checker(BaseChecker):
        name = "achecker"
        msgs = {
            "W1234": (
                "message",
                "msg-symbol",
                "msg description.",
                {"old_names": [("W0001", "old-symbol")]},
            ),
            "E1234": (
                "Duplicate keyword argument %r in %s call",
                "duplicate-keyword-arg",
                "Used when a function call passes the same keyword argument multiple times.",
                {"maxversion": (2, 6)},
            ),
        }

    store.register_messages_from_checker(Checker())
    return store


def test_format_help(capsys, store):
    store.help_message([])
    captured = capsys.readouterr()
    assert captured.out == ""
    store.help_message(["W1234", "E1234", "C1234"])
    captured = capsys.readouterr()
    assert (
        captured.out
        == """:msg-symbol (W1234): *message*
  msg description. This message belongs to the achecker checker.

:duplicate-keyword-arg (E1234): *Duplicate keyword argument %r in %s call*
  Used when a function call passes the same keyword argument multiple times.
  This message belongs to the achecker checker. It can't be emitted when using
  Python >= 2.6.

No such message id or symbol 'C1234'.

"""
    )


def test_get_msg_display_string(store):
    assert store.get_msg_display_string("W1234") == "'msg-symbol'"
    assert store.get_msg_display_string("E1234") == "'duplicate-keyword-arg'"


class TestMessageDefinitionStore(object):
    def _compare_messages(self, desc, msg, checkerref=False):
        assert desc == msg.format_help(checkerref=checkerref)

    def test_check_message_id(self, store):
        assert isinstance(store.get_message_definitions("W1234")[0], MessageDefinition)
        with pytest.raises(UnknownMessageError):
            store.get_message_definitions("YB12")

    def test_message_help(self, store):
        message_definition = store.get_message_definitions("W1234")[0]
        self._compare_messages(
            """:msg-symbol (W1234): *message*
  msg description. This message belongs to the achecker checker.""",
            message_definition,
            checkerref=True,
        )
        self._compare_messages(
            """:msg-symbol (W1234): *message*
  msg description.""",
            message_definition,
            checkerref=False,
        )

    def test_message_help_minmax(self, store):
        # build the message manually to be python version independent
        message_definition = store.get_message_definitions("E1234")[0]
        self._compare_messages(
            """:duplicate-keyword-arg (E1234): *Duplicate keyword argument %r in %s call*
  Used when a function call passes the same keyword argument multiple times.
  This message belongs to the achecker checker. It can't be emitted when using
  Python >= 2.6.""",
            message_definition,
            checkerref=True,
        )
        self._compare_messages(
            """:duplicate-keyword-arg (E1234): *Duplicate keyword argument %r in %s call*
  Used when a function call passes the same keyword argument multiple times.
  This message can't be emitted when using Python >= 2.6.""",
            message_definition,
            checkerref=False,
        )

    def test_list_messages(self, store):
        output = StringIO()
        with redirect_stdout(output):
            store.list_messages()
        # cursory examination of the output: we're mostly testing it completes
        assert ":msg-symbol (W1234): *message*" in output.getvalue()

    def test_renamed_message_register(self, store):
        assert "msg-symbol" == store.get_message_definitions("W0001")[0].symbol
        assert "msg-symbol" == store.get_message_definitions("old-symbol")[0].symbol
