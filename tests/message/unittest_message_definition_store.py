# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

from contextlib import redirect_stdout
from io import StringIO

import pytest
from pytest import CaptureFixture

from pylint.checkers import BaseChecker
from pylint.exceptions import InvalidMessageError, UnknownMessageError
from pylint.message import MessageDefinition
from pylint.message.message_definition_store import MessageDefinitionStore


@pytest.mark.parametrize(
    "messages,expected",
    [
        (
            {
                "W1234": ("message one", "msg-symbol-one", "msg description"),
                "W4321": ("message two", "msg-symbol-two", "msg description"),
            },
            r"Inconsistent checker part in message id 'W4321' (expected 'x12xx' because we already had ['W1234']).",
        ),
        (
            {
                "W1233": (
                    "message two",
                    "msg-symbol-two",
                    "msg description",
                    {"old_names": [("W1234", "old-symbol")]},
                ),
                "W1234": ("message one", "msg-symbol-one", "msg description"),
            },
            "Message id 'W1234' cannot have both 'msg-symbol-one' and 'old-symbol' as symbolic name.",
        ),
        (
            {
                "W1234": ("message one", "msg-symbol-one", "msg description"),
                "W1235": (
                    "message two",
                    "msg-symbol-two",
                    "msg description",
                    {"old_names": [("W1234", "old-symbol")]},
                ),
            },
            "Message id 'W1234' cannot have both 'msg-symbol-one' and 'old-symbol' as symbolic name.",
        ),
        (
            {
                "W1234": (
                    "message one",
                    "msg-symbol-one",
                    "msg description",
                    {"old_names": [("W1201", "old-symbol-one")]},
                ),
                "W1235": (
                    "message two",
                    "msg-symbol-two",
                    "msg description",
                    {"old_names": [("W1201", "old-symbol-two")]},
                ),
            },
            "Message id 'W1201' cannot have both 'old-symbol-one' and 'old-symbol-two' as symbolic name.",
        ),
        (
            {
                "W1234": ("message one", "msg-symbol", "msg description"),
                "W1235": ("message two", "msg-symbol", "msg description"),
            },
            "Message symbol 'msg-symbol' cannot be used for 'W1234' and 'W1235' at the same time. "
            "If you're creating an 'old_names' use 'old-msg-symbol' as the old symbol.",
        ),
        (
            {
                "W1233": (
                    "message two",
                    "msg-symbol-two",
                    "msg description",
                    {"old_names": [("W1230", "msg-symbol-one")]},
                ),
                "W1234": ("message one", "msg-symbol-one", "msg description"),
            },
            "Message symbol 'msg-symbol-one' cannot be used for 'W1230' and 'W1234' at the same time."
            " If you're creating an 'old_names' use 'old-msg-symbol-one' as the old symbol.",
        ),
        (
            {
                "W1234": ("message one", "msg-symbol-one", "msg description"),
                "W1235": (
                    "message two",
                    "msg-symbol-two",
                    "msg description",
                    {"old_names": [("W1230", "msg-symbol-one")]},
                ),
            },
            "Message symbol 'msg-symbol-one' cannot be used for 'W1230' and 'W1234' at the same time. "
            "If you're creating an 'old_names' use 'old-msg-symbol-one' as the old symbol.",
        ),
        (
            {
                "W1234": (
                    "message one",
                    "msg-symbol-one",
                    "msg description",
                    {"old_names": [("W1230", "old-symbol-one")]},
                ),
                "W1235": (
                    "message two",
                    "msg-symbol-two",
                    "msg description",
                    {"old_names": [("W1231", "old-symbol-one")]},
                ),
            },
            "Message symbol 'old-symbol-one' cannot be used for 'W1230' and 'W1231' at the same time. "
            "If you're creating an 'old_names' use 'old-old-symbol-one' as the old symbol.",
        ),
    ],
)
def test_register_error(empty_store, messages, expected):
    class Checker(BaseChecker):
        name = "checker"
        msgs = messages

    with pytest.raises(InvalidMessageError) as cm:
        empty_store.register_messages_from_checker(Checker())
    assert str(cm.value) == expected


def test_register_error_new_id_duplicate_of_new(
    empty_store: MessageDefinitionStore,
) -> None:
    class CheckerOne(BaseChecker):
        name = "checker_one"
        msgs = {"W1234": ("message one", "msg-symbol-one", "msg description.")}

    class CheckerTwo(BaseChecker):
        name = "checker_two"
        msgs = {"W1234": ("message two", "msg-symbol-two", "another msg description.")}

    empty_store.register_messages_from_checker(CheckerOne())
    test_register_error(
        empty_store,
        CheckerTwo.msgs,
        "Message id 'W1234' cannot have both 'msg-symbol-one' and 'msg-symbol-two' as symbolic name.",
    )


def test_format_help(capsys: CaptureFixture, store: MessageDefinitionStore) -> None:
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


def test_get_msg_display_string(store: MessageDefinitionStore) -> None:
    assert store.get_msg_display_string("W1234") == "'msg-symbol'"
    assert store.get_msg_display_string("E1234") == "'duplicate-keyword-arg'"


def test_check_message_id(store: MessageDefinitionStore) -> None:
    w1234 = store.get_message_definitions("W1234")[0]
    w0001 = store.get_message_definitions("W0001")[0]
    e1234 = store.get_message_definitions("E1234")[0]
    old_symbol = store.get_message_definitions("old-symbol")[0]
    assert isinstance(w1234, MessageDefinition)
    assert isinstance(e1234, MessageDefinition)
    assert w1234 == w0001
    assert w1234 == old_symbol
    with pytest.raises(UnknownMessageError):
        store.get_message_definitions("YB12")


class TestMessageDefinitionStore:
    @staticmethod
    def _compare_messages(
        desc: str, msg: MessageDefinition, checkerref: bool = False
    ) -> None:
        assert desc == msg.format_help(checkerref=checkerref)

    def test_message_help(self, store: MessageDefinitionStore) -> None:
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

    def test_message_help_minmax(self, store: MessageDefinitionStore) -> None:
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


def test_list_messages(store: MessageDefinitionStore) -> None:
    output = StringIO()
    with redirect_stdout(output):
        store.list_messages()
    # cursory examination of the output: we're mostly testing it completes
    assert ":msg-symbol (W1234): *message*" in output.getvalue()


def test_renamed_message_register(store: MessageDefinitionStore) -> None:
    assert store.get_message_definitions("W0001")[0].symbol == "msg-symbol"
    assert store.get_message_definitions("old-symbol")[0].symbol == "msg-symbol"


def test_multiple_child_of_old_name(store: MessageDefinitionStore) -> None:
    """We can define multiple name with the same old name."""

    class FamillyChecker(BaseChecker):
        name = "famillychecker"
        msgs = {
            "W1235": (
                "Child 1",
                "child-one",
                "Child one description.",
                {"old_names": [("C1234", "mother")]},
            ),
            "W1236": (
                "Child 2",
                "child-two",
                "Child two description",
                {"old_names": [("C1234", "mother")]},
            ),
        }

    store.register_messages_from_checker(FamillyChecker())
    mother = store.get_message_definitions("C1234")
    child = store.get_message_definitions("W1235")
    other_child = store.get_message_definitions("W1236")
    assert len(mother) == 2
    assert len(child) == 1
    assert len(other_child) == 1
    assert child[0] in mother
    assert other_child[0] in mother
