# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import pytest

from pylint.exceptions import InvalidMessageError
from pylint.message import MessageId


@pytest.fixture
def msgid():
    return "W1234"


@pytest.fixture
def symbol():
    return "msg-symbol"


@pytest.fixture
def message_id(msgid, symbol):
    return MessageId(msgid, symbol)


@pytest.mark.parametrize(
    "msgid,expected",
    [
        ("Q1234", "Bad message type Q in 'Q1234'"),
        ("W12345", "Invalid message id 'W12345'"),
    ],
)
def test_create_invalid_message_type(msgid, expected):
    with pytest.raises(InvalidMessageError) as cm:
        MessageId.check_msgid(msgid)
    assert str(cm.value) == expected


def test_hash_and_eq(message_id):
    """MessageId should be hashable"""
    dict_ = {}
    message_id_2 = MessageId("W1235", "msg-symbol-2")
    dict_[message_id] = 1
    dict_[message_id_2] = 2
    assert dict_[message_id] != dict_[message_id_2]
    assert message_id != message_id_2


def test_str(message_id, msgid, symbol):
    result = str(message_id)
    assert msgid in result
    assert symbol in result
