# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

from typing import ValuesView

from pylint.interfaces import HIGH
from pylint.message import Message
from pylint.message.message_definition import MessageDefinition
from pylint.typing import MessageLocationTuple


def test_new_message(message_definitions: ValuesView[MessageDefinition]) -> None:
    def build_message(
        message_definition_: MessageDefinition, location_value: MessageLocationTuple
    ) -> Message:
        return Message(
            symbol=message_definition_.symbol,
            msg_id=message_definition_.msgid,
            location=location_value,
            msg=message_definition_.msg,
            confidence=HIGH,
        )

    template = "{path}:{line}:{column}: {msg_id}: {msg} ({symbol})"
    for message_definition in message_definitions:
        if message_definition.msgid == "E1234":
            e1234_message_definition = message_definition
        if message_definition.msgid == "W1234":
            w1234_message_definition = message_definition
    e1234_location_values = MessageLocationTuple(
        abspath="1",
        path="2",
        module="3",
        obj="4",
        line=5,
        column=6,
        end_line=5,
        end_column=9,
    )
    w1234_location_values = MessageLocationTuple(
        abspath="7",
        path="8",
        module="9",
        obj="10",
        line=11,
        column=12,
        end_line=11,
        end_column=14,
    )
    expected = (
        "2:5:6: E1234: Duplicate keyword argument %r in %s call (duplicate-keyword-arg)"
    )
    e1234 = build_message(e1234_message_definition, e1234_location_values)
    w1234 = build_message(w1234_message_definition, w1234_location_values)
    assert e1234.format(template) == expected
    assert w1234.format(template) == "8:11:12: W1234: message (msg-symbol)"
