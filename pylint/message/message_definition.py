# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

import sys
from typing import List, Optional, Tuple

from pylint.constants import MSG_TYPES
from pylint.exceptions import InvalidMessageError
from pylint.utils import normalize_text


class MessageDefinition:
    def __init__(
        self,
        checker,  # BaseChecker
        msgid: str,
        msg: str,
        description: str,
        symbol: str,
        scope: str,
        minversion: Optional[Tuple[int, int, int, str, int]] = None,
        maxversion: Optional[Tuple[int, int, int, str, int]] = None,
        old_names: List[Tuple[str, str]] = None,
    ):
        self.checker_name = checker.name
        self.check_msgid(msgid)
        self.msgid = msgid
        self.symbol = symbol
        self.msg = msg
        self.description = description
        self.scope = scope
        self.minversion = minversion
        self.maxversion = maxversion
        self.old_names: List[Tuple[str, str]] = []
        if old_names:
            for old_msgid, old_symbol in old_names:
                self.check_msgid(old_msgid)
                self.old_names.append(
                    (old_msgid, old_symbol),
                )

    @staticmethod
    def check_msgid(msgid: str) -> None:
        if len(msgid) != 5:
            raise InvalidMessageError(f"Invalid message id {msgid!r}")
        if msgid[0] not in MSG_TYPES:
            raise InvalidMessageError(f"Bad message type {msgid[0]} in {msgid!r}")

    def __repr__(self):
        return f"MessageDefinition:{self.symbol} ({self.msgid})"

    def __str__(self):
        return f"{repr(self)}:\n{self.msg} {self.description}"

    def may_be_emitted(self) -> bool:
        """return True if message may be emitted using the current interpreter"""
        if self.minversion is not None and self.minversion > sys.version_info:
            return False
        if self.maxversion is not None and self.maxversion <= sys.version_info:
            return False
        return True

    def format_help(self, checkerref: bool = False) -> str:
        """return the help string for the given message id"""
        desc = self.description
        if checkerref:
            desc += " This message belongs to the %s checker." % self.checker_name
        title = self.msg
        if self.minversion or self.maxversion:
            restr = []
            if self.minversion:
                restr.append("< %s" % ".".join(str(n) for n in self.minversion))
            if self.maxversion:
                restr.append(">= %s" % ".".join(str(n) for n in self.maxversion))
            restriction = " or ".join(restr)
            if checkerref:
                desc += " It can't be emitted when using Python %s." % restriction
            else:
                desc += (
                    " This message can't be emitted when using Python %s." % restriction
                )
        msg_help = normalize_text(" ".join(desc.split()), indent="  ")
        message_id = f"{self.symbol} ({self.msgid})"
        if title != "%s":
            title = title.splitlines()[0]
            return ":{}: *{}*\n{}".format(message_id, title.rstrip(" "), msg_help)
        return f":{message_id}:\n{msg_help}"
