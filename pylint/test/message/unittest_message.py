# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import pytest

from pylint.exceptions import InvalidMessageError
from pylint.message import MessageDefinition, MessagesStore


@pytest.fixture
def store():
    return MessagesStore()


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
            "Message symbol 'msg-symbol' cannot be used for 'W1234' and 'W1235' at the same time.",
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
            "Message symbol 'msg-symbol-one' cannot be used for 'W1230' and 'W1234' at the same time.",
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
            "Message symbol 'msg-symbol-one' cannot be used for 'W1234' and 'W1235' at the same time.",
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
            "Message symbol 'old-symbol-one' cannot be used for 'W1230' and 'W1235' at the same time.",
        ),
    ],
)
def test_register_error(store, messages, expected):
    class Checker(object):
        name = "checker"
        msgs = messages

    with pytest.raises(InvalidMessageError) as cm:
        store.register_messages_from_checker(Checker())
    assert str(cm.value) == expected


def test_register_error_new_id_duplicate_of_new(store):
    class CheckerOne(object):
        name = "checker_one"
        msgs = {"W1234": ("message one", "msg-symbol-one", "msg description.")}

    class CheckerTwo(object):
        name = "checker_two"
        msgs = {"W1234": ("message two", "msg-symbol-two", "another msg description.")}

    store.register_messages_from_checker(CheckerOne())
    test_register_error(
        store,
        {"W1234": ("message two", "msg-symbol-two", "another msg description.")},
        "Message id 'W1234' cannot have both 'msg-symbol-one' and 'msg-symbol-two' as symbolic name.",
    )


@pytest.mark.parametrize(
    "msgid,expected",
    [
        ("Q1234", "Bad message type Q in 'Q1234'"),
        ("W12345", "Invalid message id 'W12345'"),
    ],
)
def test_create_invalid_message_type(msgid, expected):
    with pytest.raises(InvalidMessageError) as cm:
        MessageDefinition("checker", msgid, "msg", "descr", "symbol", "scope")
    assert str(cm.value) == expected
