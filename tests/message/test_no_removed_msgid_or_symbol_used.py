# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
from typing import TYPE_CHECKING, List, NamedTuple, Tuple

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class DeletedMessage(NamedTuple):
    msgid: str
    symbol: str
    old_names: List[Tuple[str, str]]


OLD_MSGID_SYMBOL_PAIR = [
    DeletedMessage("W1601", "apply-builtin", []),
]


def test_no_removed_msgid_or_symbol_used(linter: "PyLinter") -> None:
    """Tests that we're not using deleted msgid or symbol.

    This would be causing occasional bug, but more than that confusion and inconsistencies
    when searching for the msgid online. See https://github.com/PyCQA/pylint/issues/5729
    """
    for msgid, symbol, old_names in OLD_MSGID_SYMBOL_PAIR:
        linter.msgs_store.message_id_store.register_message_definition(
            msgid, symbol, old_names
        )
