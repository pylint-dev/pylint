# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

from pylint.constants import MSG_TYPES
from pylint.exceptions import InvalidMessageError


class MessageId:
    def __init__(self, msgid, symbol):
        self.msgid = msgid
        self.symbol = symbol

    def __str__(self):
        return "%s (%s)" % (self.symbol, self.msgid)

    def __hash__(self):
        return "{}-{}".format(self.msgid, self.symbol).__hash__()

    def __eq__(self, other):
        return self.msgid == other.msgid and self.symbol == other.symbol

    @staticmethod
    def check_msgid(msgid: str) -> None:
        """This is a static method used in MessageDefinition and not the
        MessageId constructor for performance reasons."""
        if len(msgid) != 5:
            raise InvalidMessageError("Invalid message id %r" % msgid)
        if msgid[0] not in MSG_TYPES:
            raise InvalidMessageError("Bad message type %s in %r" % (msgid[0], msgid))
