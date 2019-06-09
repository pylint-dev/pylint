# Copyright (c) 2006-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2013 buck@yelp.com <buck@yelp.com>
# Copyright (c) 2014-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Brett Cannon <brett@python.org>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Moises Lopez <moylop260@vauxoo.com>
# Copyright (c) 2017-2018 Bryce Guinta <bryce.paul.guinta@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

from typing import Any

from pylint.config import OptionsProviderMixIn
from pylint.exceptions import InvalidMessageError
from pylint.interfaces import UNDEFINED
from pylint.message import build_message_definition


class BaseChecker(OptionsProviderMixIn):

    # checker name (you may reuse an existing one)
    name = None  # type: str
    # options level (0 will be displaying in --help, 1 in --long-help)
    level = 1
    # ordered list of options to control the ckecker behaviour
    options = ()  # type: Any
    # messages issued by this checker
    msgs = {}  # type: Any
    # reports issued by this checker
    reports = ()  # type: Any
    # mark this checker as enabled or not.
    enabled = True

    def __init__(self, linter=None):
        """checker instances should have the linter as argument

        :param ILinter linter: is an object implementing ILinter."""
        if self.name is not None:
            self.name = self.name.lower()
        OptionsProviderMixIn.__init__(self)
        self.linter = linter

    def __gt__(self, other):
        """Permit to sort a list of Checker by name."""
        return "{}{}".format(self.name, self.msgs).__gt__(
            "{}{}".format(other.name, other.msgs)
        )

    def __repr__(self):
        status = "Checker" if self.enabled else "Disabled checker"
        msgids = [id for id in self.msgs]
        return "{} '{}' responsible for {}".format(status, self.name, ", ".join(msgids))

    def add_message(
        self,
        msgid,
        line=None,
        node=None,
        args=None,
        confidence=UNDEFINED,
        col_offset=None,
    ):
        self.linter.add_message(msgid, line, node, args, confidence, col_offset)

    def check_consistency(self) -> None:
        """Check the consistency of msgid.

        msg ids for a checker should be a string of len 4, where the two first
        characters are the checker id and the two last the msg id in this
        checker.

        :raises InvalidMessageError: If the checker id in the messages are not
        always the same. """
        checker_id = None
        existing_ids = []
        for message in self.messages:
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

    @property
    def messages(self) -> list:
        return [
            build_message_definition(self, msgid, msg_tuple)
            for msgid, msg_tuple in sorted(self.msgs.items())
        ]

    # dummy methods implementing the IChecker interface

    def get_message_definition(self, msgid):
        for message_definition in self.messages:
            if message_definition.msgid == msgid:
                return message_definition
        error_msg = "MessageDefinition for '{}' does not exists. ".format(msgid)
        error_msg += "Choose from {}.".format([m.msgid for m in self.messages])
        raise InvalidMessageError(error_msg)

    def open(self):
        """called before visiting project (i.e set of modules)"""

    def close(self):
        """called after visiting project (i.e set of modules)"""


class BaseTokenChecker(BaseChecker):
    """Base class for checkers that want to have access to the token stream."""

    def process_tokens(self, tokens):
        """Should be overridden by subclasses."""
        raise NotImplementedError()
