# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

from typing import Any, NamedTuple, Optional, Sequence, Tuple, Union

from astroid import nodes

from pylint.constants import PY38_PLUS
from pylint.interfaces import HIGH, UNDEFINED, Confidence
from pylint.message.message import Message
from pylint.testutils.constants import UPDATE_OPTION


class MessageTest(NamedTuple):
    """Used to test messages produced by pylint. Class name cannot start with Test as pytest doesn't allow constructors in test classes."""

    msg_id: str
    line: Optional[int] = None
    node: Optional[nodes.NodeNG] = None
    args: Any = None
    confidence: Optional[Confidence] = None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, MessageTest):
            if self.confidence and other.confidence:
                return NamedTuple.__eq__(self, other)
            # pylint: disable-next=unsubscriptable-object
            return tuple(self[:-1]) == tuple(other[:-1])
        return NotImplemented  # pragma: no cover


class MalformedOutputLineException(Exception):
    def __init__(
        self,
        row: Union[Sequence[str], str],
        exception: Exception,
    ) -> None:
        example = "msg-symbolic-name:42:27:MyClass.my_function:The message"
        other_example = "msg-symbolic-name:7:42::The message"
        expected = [
            "symbol",
            "line",
            "column",
            "MyClass.myFunction, (or '')",
            "Message",
            "confidence",
        ]
        reconstructed_row = ""
        i = 0
        try:
            for i, column in enumerate(row):
                reconstructed_row += f"\t{expected[i]}='{column}' ?\n"
            for missing in expected[i + 1 :]:
                reconstructed_row += f"\t{missing}= Nothing provided !\n"
        except IndexError:
            pass
        raw = ":".join(row)
        msg = f"""\
{exception}

Expected '{example}' or '{other_example}' but we got '{raw}':
{reconstructed_row}

Try updating it with: 'python tests/test_functional.py {UPDATE_OPTION}'"""
        super().__init__(msg)


class OutputLine(NamedTuple):
    symbol: str
    lineno: int
    column: int
    object: str
    msg: str
    confidence: str

    @classmethod
    def from_msg(cls, msg: Message) -> "OutputLine":
        column = cls._get_column(msg.column)
        return cls(
            msg.symbol,
            msg.line,
            column,
            msg.obj or "",
            msg.msg.replace("\r\n", "\n"),
            msg.confidence.name if msg.confidence != UNDEFINED else HIGH.name,
        )

    @staticmethod
    def _get_column(column: str) -> int:
        if not PY38_PLUS:
            # We check the column only for the new better ast parser introduced in python 3.8
            return 0  # pragma: no cover
        return int(column)

    @classmethod
    def from_csv(cls, row: Union[Sequence[str], str]) -> "OutputLine":
        try:
            if isinstance(row, Sequence):
                column = cls._get_column(row[2])
                if len(row) == 5:
                    return cls(row[0], int(row[1]), column, row[3], row[4], HIGH.name)
                if len(row) == 6:
                    return cls(row[0], int(row[1]), column, row[3], row[4], row[5])
            raise IndexError
        except Exception as e:
            raise MalformedOutputLineException(row, e) from e

    def to_csv(self) -> Tuple[str, str, str, str, str, str]:
        return tuple(str(i) for i in self)  # type: ignore # pylint: disable=not-an-iterable
