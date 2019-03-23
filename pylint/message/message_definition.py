# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import sys

from pylint.message.message_id import MessageId
from pylint.utils import normalize_text


class MessageDefinition:
    def __init__(
        self,
        checker,
        msgid,
        msg,
        description,
        symbol,
        scope,
        minversion=None,
        maxversion=None,
        old_names=None,
    ):
        self.checker = checker
        MessageId.check_msgid(msgid)
        self.message_id = MessageId(msgid, symbol)
        self.msg = msg
        self.description = description
        self.scope = scope
        self.minversion = minversion
        self.maxversion = maxversion
        self.old_names = old_names or []

    @property
    def symbol(self):
        return self.message_id.symbol

    @property
    def msgid(self):
        return self.message_id.msgid

    def __repr__(self):
        return "MessageDefinition:%s (%s)" % (self.symbol, self.msgid)

    def __str__(self):
        return "%s:\n%s %s" % (repr(self), self.msg, self.description)

    def may_be_emitted(self):
        """return True if message may be emitted using the current interpreter"""
        if self.minversion is not None and self.minversion > sys.version_info:
            return False
        if self.maxversion is not None and self.maxversion <= sys.version_info:
            return False
        return True

    def format_help(self, checkerref=False):
        """return the help string for the given message id"""
        desc = self.description
        if checkerref:
            desc += " This message belongs to the %s checker." % self.checker.name
        title = self.msg
        if self.minversion or self.maxversion:
            restr = []
            if self.minversion:
                restr.append("< %s" % ".".join([str(n) for n in self.minversion]))
            if self.maxversion:
                restr.append(">= %s" % ".".join([str(n) for n in self.maxversion]))
            restr = " or ".join(restr)
            if checkerref:
                desc += " It can't be emitted when using Python %s." % restr
            else:
                desc += " This message can't be emitted when using Python %s." % restr
        desc = normalize_text(" ".join(desc.split()), indent="  ")
        if title != "%s":
            title = title.splitlines()[0]
            return ":%s: *%s*\n%s" % (self.message_id, title.rstrip(" "), desc)
        return ":%s:\n%s" % (self.message_id, desc)
