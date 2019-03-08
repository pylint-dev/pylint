# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import io

import astroid

from pylint.message import MessagesStore, MessageDefinition
from pylint.checkers.utils import check_messages, get_node_last_lineno
from pylint.exceptions import InvalidMessageError
import pytest


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
