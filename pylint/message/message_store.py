# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

from __future__ import print_function

import collections

from pylint.exceptions import InvalidMessageError, UnknownMessageError
from pylint.message.build_message_definition import build_message_def


class MessagesStore:
    """The messages store knows information about every possible message but has
    no particular state during analysis.
    """

    def __init__(self):
        # Primary registry for all active messages (i.e. all messages
        # that can be emitted by pylint for the underlying Python
        # version). It contains the 1:1 mapping from symbolic names
        # to message definition objects.
        # Keys are msg ids, values are a 2-uple with the msg type and the
        # msg itself
        self._messages_definitions = {}
        # Maps alternative names (numeric IDs, deprecated names) to
        # message definitions. May contain several names for each definition
        # object.
        self._alternative_names = {}
        self._msgs_by_category = collections.defaultdict(list)

    @property
    def messages(self):
        """The list of all active messages."""
        return self._messages_definitions.values()

    def add_renamed_message(self, old_id, old_symbol, new_symbol):
        """Register the old ID and symbol for a warning that was renamed.

        This allows users to keep using the old ID/symbol in suppressions.
        """
        message_definition = self.get_message_definitions(new_symbol)[0]
        message_definition.old_names.append((old_id, old_symbol))
        self._register_alternative_name(message_definition, old_id, old_symbol)

    @staticmethod
    def get_checker_message_definitions(checker):
        """Return the list of messages definitions for a checker.

        :param BaseChecker checker:
        :rtype: list
        :return: A list of MessageDefinition.
        """
        message_definitions = []
        for msgid, msg_tuple in sorted(checker.msgs.items()):
            message = build_message_def(checker, msgid, msg_tuple)
            message_definitions.append(message)
        return message_definitions

    def register_messages_from_checker(self, checker):
        """Register all messages from a checker.

        :param BaseChecker checker:
        """
        checker_message_definitions = self.get_checker_message_definitions(checker)
        self._check_checker_consistency(checker_message_definitions)
        for message_definition in checker_message_definitions:
            self.register_message(message_definition)

    def register_message(self, message):
        """Register a MessageDefinition with consistency in mind.

        :param MessageDefinition message: The message definition being added.
        """
        self._check_id_and_symbol_consistency(message.msgid, message.symbol)
        self._check_symbol(message.msgid, message.symbol)
        self._check_msgid(message.msgid, message.symbol)
        for old_name in message.old_names:
            self._check_symbol(message.msgid, old_name[1])
        self._messages_definitions[message.symbol] = message
        self._register_alternative_name(message, message.msgid, message.symbol)
        for old_id, old_symbol in message.old_names:
            self._register_alternative_name(message, old_id, old_symbol)
        self._msgs_by_category[message.msgid[0]].append(message.msgid)

    @staticmethod
    def _check_checker_consistency(messages):
        """Check the msgid consistency in a list of messages definitions.

        msg ids for a checker should be a string of len 4, where the two first
        characters are the checker id and the two last the msg id in this
        checker.

        :param list messages: List of MessageDefinition.
        :raises InvalidMessageError: If the checker id in the messages are not
        always the same
        """
        checker_id = None
        existing_ids = []
        for message in messages:
            if checker_id is not None and checker_id != message.msgid[1:3]:
                error_msg = "Inconsistent checker part in message id "
                error_msg += "'{}' (expected 'x{checker_id}xx' ".format(
                    message.msgid, checker_id=checker_id
                )
                error_msg += "because we already had {existing_ids}).".format(
                    existing_ids=existing_ids
                )
                raise InvalidMessageError(error_msg)
            checker_id = message.msgid[1:3]
            existing_ids.append(message.msgid)

    def _register_alternative_name(self, msg, msgid, symbol):
        """helper for register_message()"""
        self._check_id_and_symbol_consistency(msgid, symbol)
        self._alternative_names[msgid] = msg
        self._alternative_names[symbol] = msg

    def _check_symbol(self, msgid, symbol):
        """Check that a symbol is not already used. """
        other_message = self._messages_definitions.get(symbol)
        if other_message:
            self._raise_duplicate_msg_id(symbol, msgid, other_message.msgid)
        else:
            alternative_msgid = None
        alternative_message = self._alternative_names.get(symbol)
        if alternative_message:
            if alternative_message.symbol == symbol:
                alternative_msgid = alternative_message.msgid
            else:
                for old_msgid, old_symbol in alternative_message.old_names:
                    if old_symbol == symbol:
                        alternative_msgid = old_msgid
                        break
            if msgid != alternative_msgid:
                self._raise_duplicate_msg_id(symbol, msgid, alternative_msgid)

    def _check_msgid(self, msgid, symbol):
        for message in self._messages_definitions.values():
            if message.msgid == msgid:
                self._raise_duplicate_symbol(msgid, symbol, message.symbol)

    def _check_id_and_symbol_consistency(self, msgid, symbol):
        try:
            alternative = self._alternative_names[msgid]
        except KeyError:
            alternative = False
        try:
            if not alternative:
                alternative = self._alternative_names[symbol]
        except KeyError:
            # There is no alternative names concerning this msgid/symbol.
            # So nothing to check
            return None
        old_symbolic_name = None
        old_symbolic_id = None
        for alternate_msgid, alternate_symbol in alternative.old_names:
            if alternate_msgid == msgid or alternate_symbol == symbol:
                old_symbolic_id = alternate_msgid
                old_symbolic_name = alternate_symbol
        if symbol not in (alternative.symbol, old_symbolic_name):
            if msgid == old_symbolic_id:
                self._raise_duplicate_symbol(msgid, symbol, old_symbolic_name)
            else:
                self._raise_duplicate_symbol(msgid, symbol, alternative.symbol)
        return None

    @staticmethod
    def _raise_duplicate_symbol(msgid, symbol, other_symbol):
        """Raise an error when a symbol is duplicated.

        :param str msgid: The msgid corresponding to the symbols
        :param str symbol: Offending symbol
        :param str other_symbol: Other offending symbol
        :raises InvalidMessageError: when a symbol is duplicated.
        """
        symbols = [symbol, other_symbol]
        symbols.sort()
        error_message = "Message id '{msgid}' cannot have both ".format(msgid=msgid)
        error_message += "'{other_symbol}' and '{symbol}' as symbolic name.".format(
            other_symbol=symbols[0], symbol=symbols[1]
        )
        raise InvalidMessageError(error_message)

    @staticmethod
    def _raise_duplicate_msg_id(symbol, msgid, other_msgid):
        """Raise an error when a msgid is duplicated.

        :param str symbol: The symbol corresponding to the msgids
        :param str msgid: Offending msgid
        :param str other_msgid: Other offending msgid
        :raises InvalidMessageError: when a msgid is duplicated.
        """
        msgids = [msgid, other_msgid]
        msgids.sort()
        error_message = "Message symbol '{symbol}' cannot be used for ".format(
            symbol=symbol
        )
        error_message += "'{other_msgid}' and '{msgid}' at the same time.".format(
            other_msgid=msgids[0], msgid=msgids[1]
        )
        raise InvalidMessageError(error_message)

    def get_message_definitions(self, msgid_or_symbol: str) -> list:
        """Returns the Message object for this message.

        :param str msgid_or_symbol: msgid_or_symbol may be either a numeric or symbolic id.
        :raises UnknownMessageError: if the message id is not defined.
        :rtype: List of MessageDefinition
        :return: A message definition corresponding to msgid_or_symbol
        """
        if msgid_or_symbol[1:].isdigit():
            msgid_or_symbol = msgid_or_symbol.upper()
        for source in (self._alternative_names, self._messages_definitions):
            try:
                return [source[msgid_or_symbol]]
            except KeyError:
                pass
        error_msg = "No such message id or symbol '{msgid_or_symbol}'.".format(
            msgid_or_symbol=msgid_or_symbol
        )
        raise UnknownMessageError(error_msg)

    def get_msg_display_string(self, msgid):
        """Generates a user-consumable representation of a message.

        Can be just the message ID or the ID and the symbol.
        """
        message_definitions = self.get_message_definitions(msgid)
        if len(message_definitions) == 1:
            return repr(message_definitions[0].symbol)
        return repr([md.symbol for md in message_definitions])

    def help_message(self, msgids):
        """Display help messages for the given message identifiers"""
        for msgid in msgids:
            try:
                for message_definition in self.get_message_definitions(msgid):
                    print(message_definition.format_help(checkerref=True))
                    print("")
            except UnknownMessageError as ex:
                print(ex)
                print("")
                continue

    def list_messages(self):
        """Output full messages list documentation in ReST format. """
        messages = sorted(self._messages_definitions.values(), key=lambda m: m.msgid)
        for message in messages:
            if not message.may_be_emitted():
                continue
            print(message.format_help(checkerref=False))
        print("")
