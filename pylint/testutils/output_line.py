# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import collections
import sys

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


class MalformedOutputLineException(Exception):
    def __init__(self, row, exception):
        example = "msg-symbolic-name:42:27:MyClass.my_function:The message"
        other_example = "msg-symbolic-name:7:42::The message"
        reconstructed_row = ":".join(row)
        msg = "Expected '{example}' or '{other_example}' but we got '{reconstructed_row}'".format(
            example=example,
            other_example=other_example,
            reconstructed_row=reconstructed_row,
        )
        Exception.__init__(
            self, "{msg}: {exception}".format(msg=msg, exception=exception)
        )


class OutputLine(
    collections.namedtuple(
        "OutputLine", ["symbol", "lineno", "column", "object", "msg", "confidence"]
    )
):
    @classmethod
    def from_msg(cls, msg):
        column = cls.get_column(msg.column)
        return cls(
            msg.symbol,
            msg.line,
            column,
            msg.obj or "",
            msg.msg.replace("\r\n", "\n"),
            msg.confidence.name
            if msg.confidence != interfaces.UNDEFINED
            else interfaces.HIGH.name,
        )

    @classmethod
    def get_column(cls, column):
        if sys.version_info.major == 3 and sys.version_info.minor < 8:
            return ""
        return str(column)

    @classmethod
    def from_csv(cls, row):
        try:
            confidence = row[5] if len(row) == 6 else interfaces.HIGH.name
            column = cls.get_column(row[2])
            return cls(row[0], int(row[1]), column, row[3], row[4], confidence)
        except Exception as e:
            raise MalformedOutputLineException(row, e) from e

    def to_csv(self):
        if self.confidence == interfaces.HIGH.name:
            return self[:-1]
        return self
