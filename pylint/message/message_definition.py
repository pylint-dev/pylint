# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import sys

from pylint.exceptions import InvalidMessageError
from pylint.message.constants import MSG_TYPES
from pylint.utils.normalize_text import normalize_text


class MessageDefinition:
    def __init__(
        self,
        checker,
        msgid,
        msg,
        descr,
        symbol,
        scope,
        minversion=None,
        maxversion=None,
        old_names=None,
    ):
        self.checker = checker
        if len(msgid) != 5:
            raise InvalidMessageError("Invalid message id %r" % msgid)
        if not msgid[0] in MSG_TYPES:
            raise InvalidMessageError("Bad message type %s in %r" % (msgid[0], msgid))
        self.msgid = msgid
        self.msg = msg
        self.descr = descr
        self.symbol = symbol
        self.scope = scope
        self.minversion = minversion
        self.maxversion = maxversion
        self.old_names = old_names or []

    def __repr__(self):
        return "MessageDefinition:{}".format(self.__dict__)

    def may_be_emitted(self):
        """return True if message may be emitted using the current interpreter"""
        if self.minversion is not None and self.minversion > sys.version_info:
            return False
        if self.maxversion is not None and self.maxversion <= sys.version_info:
            return False
        return True

    def format_help(self, checkerref=False):
        """return the help string for the given message id"""
        desc = self.descr
        if checkerref:
            desc += " This message belongs to the %s checker." % self.checker.name
        title = self.msg
        if self.symbol:
            msgid = "%s (%s)" % (self.symbol, self.msgid)
        else:
            msgid = self.msgid
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

            return ":%s: *%s*\n%s" % (msgid, title.rstrip(" "), desc)
        return ":%s:\n%s" % (msgid, desc)
