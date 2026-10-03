# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from pylint.lint import PyLinter
from pylint.message._deleted_message_ids import DELETED_MESSAGES_IDS


def test_no_removed_msgid_or_symbol_used(linter: PyLinter) -> None:
    """Tests that we're not using deleted msgid or symbol.

    This could cause occasional bugs, but more importantly confusion and inconsistencies
    when searching for old msgids online. See https://github.com/pylint-dev/pylint/issues/5729
    """
    for deleted_messages in DELETED_MESSAGES_IDS.values():
        for msgid, symbol, old_names in deleted_messages:
            linter.msgs_store.message_id_store.register_message_definition(
                msgid, symbol, old_names
            )
