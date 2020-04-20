# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import pytest

from pylint.exceptions import InvalidMessageError, UnknownMessageError


def test_len_str(msgid_store, msgids):
    assert len(msgid_store) == len(msgids)
    str_result = str(msgid_store)
    assert "MessageIdStore: [" in str_result
    assert "  - W1234 (warning-symbol)" in str_result
    assert "  - W1235 (warning-symbol-two)" in str_result
    assert "  - C1234 (convention-symbol)" in str_result
    assert "  - E1234 (error-symbol)" in str_result
    assert "]" in str_result


def test_get_message_ids(msgid_store, msgids):
    """We can get message id even with capitalization problem."""
    msgid = list(msgids.keys())[0]
    msgids_result = msgid_store.get_active_msgids(msgid.lower())
    assert len(msgids_result) == 1
    assert msgid == msgids_result[0]


def test_get_message_ids_not_existing(empty_msgid_store):
    with pytest.raises(UnknownMessageError) as error:
        w9876 = "W9876"
        empty_msgid_store.get_active_msgids(w9876)
    assert w9876 in str(error.value)


def test_register_message_definitions(empty_msgid_store, message_definitions):
    number_of_msgid = len(message_definitions)
    for message_definition in message_definitions:
        empty_msgid_store.register_message_definition(message_definition)
        if message_definition.old_names:
            number_of_msgid += len(message_definition.old_names)
    assert len(empty_msgid_store) == number_of_msgid


def test_add_msgid_and_symbol(empty_msgid_store):
    empty_msgid_store.add_msgid_and_symbol("E1235", "new-sckiil")
    empty_msgid_store.add_legacy_msgid_and_symbol("C1235", "old-sckiil", "E1235")
    assert len(empty_msgid_store) == 2
    message_ids = empty_msgid_store.get_active_msgids("E1235")
    assert len(message_ids) == 1
    assert message_ids[0] == "E1235"
    message_ids = empty_msgid_store.get_active_msgids("old-sckiil")
    assert len(message_ids) == 1
    assert message_ids[0] == "E1235"
    assert empty_msgid_store.get_symbol("C1235") == "old-sckiil"
    assert empty_msgid_store.get_symbol("E1235") == "new-sckiil"
    assert empty_msgid_store.get_msgid("old-sckiil") == "C1235"
    assert empty_msgid_store.get_msgid("new-sckiil") == "E1235"
    with pytest.raises(KeyError):
        empty_msgid_store.get_symbol("C1234")
    with pytest.raises(KeyError):
        empty_msgid_store.get_msgid("not-exist")


def test_duplicate_symbol(empty_msgid_store):
    empty_msgid_store.add_msgid_and_symbol("W1234", "warning-symbol")
    with pytest.raises(InvalidMessageError) as error:
        empty_msgid_store.check_msgid_and_symbol("W1234", "other-symbol")
    assert (
        "Message id 'W1234' cannot have both 'other-symbol' and 'warning-symbol' as symbolic name."
        in str(error.value)
    )


def test_duplicate_msgid(msgid_store):
    msgid_store.add_msgid_and_symbol("W1234", "warning-symbol")
    with pytest.raises(InvalidMessageError) as error:
        msgid_store.check_msgid_and_symbol("W1235", "warning-symbol")
    assert (
        "Message symbol 'warning-symbol' cannot be used for 'W1234' and 'W1235'"
        in str(error.value)
    )
