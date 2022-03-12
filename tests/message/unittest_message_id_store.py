# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

from pathlib import Path
from typing import Dict, ValuesView

import pytest

from pylint import lint
from pylint.exceptions import InvalidMessageError, UnknownMessageError
from pylint.message.message_definition import MessageDefinition
from pylint.message.message_id_store import MessageIdStore

EMPTY_FILE = str(Path(__file__).parent.parent.resolve() / "regrtest_data" / "empty.py")


def test_len_str(msgid_store: MessageIdStore, msgids: Dict[str, str]) -> None:
    assert len(msgid_store) == len(msgids)
    str_result = str(msgid_store)
    assert "MessageIdStore: [" in str_result
    assert "  - W1234 (warning-symbol)" in str_result
    assert "  - W1235 (warning-symbol-two)" in str_result
    assert "  - C1234 (convention-symbol)" in str_result
    assert "  - E1234 (error-symbol)" in str_result
    assert "]" in str_result


def test_get_message_ids(msgid_store: MessageIdStore, msgids: Dict[str, str]) -> None:
    """We can get message id even with capitalization problem."""
    msgid = list(msgids.keys())[0]
    msgids_result = msgid_store.get_active_msgids(msgid.lower())
    assert len(msgids_result) == 1
    assert msgid == msgids_result[0]


def test_get_message_ids_not_existing(empty_msgid_store: MessageIdStore) -> None:
    with pytest.raises(UnknownMessageError) as error:
        w9876 = "W9876"
        empty_msgid_store.get_active_msgids(w9876)
    assert w9876 in str(error.value)


def test_register_message_definitions(
    empty_msgid_store: MessageIdStore,
    message_definitions: ValuesView[MessageDefinition],
) -> None:
    number_of_msgid = len(message_definitions)
    for message_definition in message_definitions:
        empty_msgid_store.register_message_definition(
            message_definition.msgid,
            message_definition.symbol,
            message_definition.old_names,
        )
        if message_definition.old_names:
            number_of_msgid += len(message_definition.old_names)
    assert len(empty_msgid_store) == number_of_msgid


def test_add_msgid_and_symbol(empty_msgid_store: MessageIdStore) -> None:
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
    with pytest.raises(UnknownMessageError):
        empty_msgid_store.get_symbol("C1234")
    with pytest.raises(UnknownMessageError):
        empty_msgid_store.get_msgid("not-exist")


def test_duplicate_symbol(empty_msgid_store: MessageIdStore) -> None:
    empty_msgid_store.add_msgid_and_symbol("W1234", "warning-symbol")
    with pytest.raises(InvalidMessageError) as error:
        empty_msgid_store.check_msgid_and_symbol("W1234", "other-symbol")
    assert (
        "Message id 'W1234' cannot have both 'other-symbol' and 'warning-symbol' as symbolic name."
        in str(error.value)
    )


def test_duplicate_msgid(msgid_store: MessageIdStore) -> None:
    msgid_store.add_msgid_and_symbol("W1234", "warning-symbol")
    with pytest.raises(InvalidMessageError) as error:
        msgid_store.check_msgid_and_symbol("W1235", "warning-symbol")
    assert (
        "Message symbol 'warning-symbol' cannot be used for 'W1234' and 'W1235'"
        in str(error.value)
    )


def test_exclusivity_of_msgids() -> None:
    """Test to see if all checkers have an exclusive message id prefix."""
    err_msg = (
        "{} has the same prefix ('{}') as the '{}' checker. Please make sure the prefix "
        "is unique for each checker. You can use 'script/get_unused_message_id_category.py' "
        "to get an unique id."
    )

    runner = lint.Run(
        ["--enable-all-extensions", EMPTY_FILE],
        exit=False,
    )

    # Some pairs are hard-coded as they are pre-existing and non-exclusive
    # and we don't want to rename them for backwards compatibility
    checker_id_pairs = {
        "00": ("master", "miscellaneous"),
        "01": (
            "basic",
            "refactoring",
            "consider_ternary_expression",
            "while_used",
            "docstyle",
            "deprecated_builtins",
        ),
        "02": ("classes", "refactoring", "multiple_types"),
        "03": ("classes", "format"),
        "04": ("imports", "spelling"),
        "05": ("consider-using-any-or-all", "miscellaneous"),
        "07": ("exceptions", "broad_try_clause", "overlap-except"),
        "12": ("design", "logging"),
        "17": ("async", "refactoring"),
        "20": ("compare-to-zero", "refactoring"),
    }

    for msgid, definition in runner.linter.msgs_store._messages_definitions.items():
        if msgid[1:3] in checker_id_pairs:
            assert (
                definition.checker_name in checker_id_pairs[msgid[1:3]]
            ), err_msg.format(msgid, msgid[1:3], checker_id_pairs[msgid[1:3]][0])
        else:
            checker_id_pairs[msgid[1:3]] = (definition.checker_name,)
