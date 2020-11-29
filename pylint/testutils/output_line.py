# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import collections

from pylint import interfaces


class Message(
    collections.namedtuple("Message", ["msg_id", "line", "node", "args", "confidence"])
):
    def __new__(cls, msg_id, line=None, node=None, args=None, confidence=None):
        return tuple.__new__(cls, (msg_id, line, node, args, confidence))

    def __eq__(self, other):
        if isinstance(other, Message):
            if self.confidence and other.confidence:
                return super().__eq__(other)
            return self[:-1] == other[:-1]
        return NotImplemented  # pragma: no cover

    __hash__ = None


class OutputLine(
    collections.namedtuple(
        "OutputLine", ["symbol", "lineno", "object", "msg", "confidence"]
    )
):
    @classmethod
    def from_msg(cls, msg):
        return cls(
            msg.symbol,
            msg.line,
            msg.obj or "",
            msg.msg.replace("\r\n", "\n"),
            msg.confidence.name
            if msg.confidence != interfaces.UNDEFINED
            else interfaces.HIGH.name,
        )

    @classmethod
    def from_csv(cls, row):
        confidence = row[4] if len(row) == 5 else interfaces.HIGH.name
        return cls(row[0], int(row[1]), row[2], row[3], confidence)

    def to_csv(self):
        if self.confidence == interfaces.HIGH.name:
            return self[:-1]
        return self
