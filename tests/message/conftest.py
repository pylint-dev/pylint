# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE
# pylint: disable=redefined-outer-name


import pytest

from pylint.checkers import BaseChecker
from pylint.message import MessageDefinitionStore, MessageIdStore


@pytest.fixture
def msgid():
    return "W1234"


@pytest.fixture
def symbol():
    return "msg-symbol"


@pytest.fixture
def empty_store():
    return MessageDefinitionStore()


@pytest.fixture
def store():
    store_ = MessageDefinitionStore()

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

    store_.register_messages_from_checker(Checker())
    return store_


@pytest.fixture
def message_definitions(store):
    return store.messages


@pytest.fixture
def msgids():
    return {
        "W1234": "warning-symbol",
        "W1235": "warning-symbol-two",
        "C1234": "convention-symbol",
        "E1234": "error-symbol",
    }


@pytest.fixture
def empty_msgid_store():
    return MessageIdStore()


@pytest.fixture
def msgid_store(msgids):
    msgid_store = MessageIdStore()
    for msgid, symbol in msgids.items():
        msgid_store.add_msgid_and_symbol(msgid, symbol)
    return msgid_store
