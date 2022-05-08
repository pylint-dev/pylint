# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from typing import TYPE_CHECKING

from pylint import exceptions
from pylint.constants import MSG_TYPES, MSG_TYPES_LONG
from pylint.message import MessageDefinition
from pylint.typing import ManagedMessage

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter


class _MessageStateHandler:
    """Class that handles message disabling & enabling and processing of inline pragma's."""

    def __init__(self, linter: PyLinter) -> None:
        self.linter = linter
        self._msgs_state: dict[str, bool] = {}

    def _set_one_msg_status(
        self, scope: str, msg: MessageDefinition, line: int | None, enable: bool
    ) -> None:
        """Set the status of an individual message."""
        if scope == "module":
            assert isinstance(line, int)  # should always be int inside module scope

            self.linter.file_state.set_msg_status(msg, line, enable)
            if not enable and msg.symbol != "locally-disabled":
                self.linter.add_message(
                    "locally-disabled", line=line, args=(msg.symbol, msg.msgid)
                )
        else:
            msgs = self._msgs_state
            msgs[msg.msgid] = enable

    def _get_messages_to_set(
        self, msgid: str, enable: bool, ignore_unknown: bool = False
    ) -> list[MessageDefinition]:
        """Do some tests and find the actual messages of which the status should be set."""
        message_definitions: list[MessageDefinition] = []
        if msgid == "all":
            for _msgid in MSG_TYPES:
                message_definitions.extend(
                    self._get_messages_to_set(_msgid, enable, ignore_unknown)
                )
            return message_definitions

        # msgid is a category?
        category_id = msgid.upper()
        if category_id not in MSG_TYPES:
            category_id_formatted = MSG_TYPES_LONG.get(category_id)
        else:
            category_id_formatted = category_id
        if category_id_formatted is not None:
            for _msgid in self.linter.msgs_store._msgs_by_category[
                category_id_formatted
            ]:
                message_definitions.extend(
                    self._get_messages_to_set(_msgid, enable, ignore_unknown)
                )
            return message_definitions

        # msgid is a checker name?
        if msgid.lower() in self.linter._checkers:
            for checker in self.linter._checkers[msgid.lower()]:
                for _msgid in checker.msgs:
                    message_definitions.extend(
                        self._get_messages_to_set(_msgid, enable, ignore_unknown)
                    )
            return message_definitions

        # msgid is report id?
        if msgid.lower().startswith("rp"):
            if enable:
                self.linter.enable_report(msgid)
            else:
                self.linter.disable_report(msgid)
            return message_definitions

        try:
            # msgid is a symbolic or numeric msgid.
            message_definitions = self.linter.msgs_store.get_message_definitions(msgid)
        except exceptions.UnknownMessageError:
            if not ignore_unknown:
                raise
        return message_definitions

    def _set_msg_status(
        self,
        msgid: str,
        enable: bool,
        scope: str = "package",
        line: int | None = None,
        ignore_unknown: bool = False,
    ) -> None:
        """Do some tests and then iterate over message definitions to set state."""
        assert scope in {"package", "module"}

        message_definitions = self._get_messages_to_set(msgid, enable, ignore_unknown)

        for message_definition in message_definitions:
            self._set_one_msg_status(scope, message_definition, line, enable)

        # sync configuration object
        self.linter.config.enable = []
        self.linter.config.disable = []
        for msgid_or_symbol, is_enabled in self._msgs_state.items():
            symbols = [
                m.symbol
                for m in self.linter.msgs_store.get_message_definitions(msgid_or_symbol)
            ]
            if is_enabled:
                self.linter.config.enable += symbols
            else:
                self.linter.config.disable += symbols

    def _register_by_id_managed_msg(
        self, msgid_or_symbol: str, line: int | None, is_disabled: bool = True
    ) -> None:
        """If the msgid is a numeric one, then register it to inform the user
        it could furnish instead a symbolic msgid.
        """
        if msgid_or_symbol[1:].isdigit():
            try:
                symbol = self.linter.msgs_store.message_id_store.get_symbol(
                    msgid=msgid_or_symbol
                )
            except exceptions.UnknownMessageError:
                return
            managed = ManagedMessage(
                self.linter.current_name, msgid_or_symbol, symbol, line, is_disabled
            )
            self.linter._by_id_managed_msgs.append(managed)
