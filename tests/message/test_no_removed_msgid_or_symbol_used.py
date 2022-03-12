# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

from pylint.constants import DELETED_MESSAGES
from pylint.lint import PyLinter


def test_no_removed_msgid_or_symbol_used(linter: PyLinter) -> None:
    """Tests that we're not using deleted msgid or symbol.

    This could cause occasional bugs, but more importantly confusion and inconsistencies
    when searching for old msgids online. See https://github.com/PyCQA/pylint/issues/5729
    """
    for msgid, symbol, old_names in DELETED_MESSAGES:
        linter.msgs_store.message_id_store.register_message_definition(
            msgid, symbol, old_names
        )
