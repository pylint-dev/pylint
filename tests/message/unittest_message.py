# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

from pylint.message import Message


def test_new_message(message_definitions):
    def build_message(message_definition, location_value):
        return Message(
            symbol=message_definition.symbol,
            msg_id=message_definition.msgid,
            location=[
                location_value["abspath"],
                location_value["path"],
                location_value["module"],
                location_value["obj"],
                location_value["line"],
                location_value["column"],
            ],
            msg=message_definition.msg,
            confidence="high",
        )

    template = "{path}:{line}:{column}: {msg_id}: {msg} ({symbol})"
    for message_definition in message_definitions:
        if message_definition.msgid == "E1234":
            e1234_message_definition = message_definition
        if message_definition.msgid == "W1234":
            w1234_message_definition = message_definition
    e1234_location_values = {
        "abspath": "1",
        "path": "2",
        "module": "3",
        "obj": "4",
        "line": "5",
        "column": "6",
    }
    w1234_location_values = {
        "abspath": "7",
        "path": "8",
        "module": "9",
        "obj": "10",
        "line": "11",
        "column": "12",
    }
    expected = (
        "2:5:6: E1234: Duplicate keyword argument %r in %s call (duplicate-keyword-arg)"
    )
    e1234 = build_message(e1234_message_definition, e1234_location_values)
    w1234 = build_message(w1234_message_definition, w1234_location_values)
    assert e1234.format(template) == expected
    assert w1234.format(template) == "8:11:12: W1234: message (msg-symbol)"
