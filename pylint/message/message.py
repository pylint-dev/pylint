# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE


import collections
from typing import Optional, Tuple, Union
from warnings import warn

from pylint.constants import MSG_TYPES
from pylint.interfaces import Confidence
from pylint.typing import MessageLocationTuple

_MsgBase = collections.namedtuple(
    "_MsgBase",
    [
        "msg_id",
        "symbol",
        "msg",
        "C",
        "category",
        "confidence",
        "abspath",
        "path",
        "module",
        "obj",
        "line",
        "column",
    ],
)


class Message(_MsgBase):
    """This class represent a message to be issued by the reporters"""

    def __new__(
        cls,
        msg_id: str,
        symbol: str,
        location: Union[Tuple[str, str, str, str, int, int], MessageLocationTuple],
        msg: str,
        confidence: Optional[Confidence],
    ):
        if isinstance(location, tuple):
            warn(
                "In pylint 3.0, Messages will only accept a MessageLocationTuple as location parameter",
                DeprecationWarning,
            )
        return _MsgBase.__new__(
            cls,
            msg_id,
            symbol,
            msg,
            msg_id[0],
            MSG_TYPES[msg_id[0]],
            confidence,
            *location
        )

    def format(self, template: str) -> str:
        """Format the message according to the given template.

        The template format is the one of the format method :
        cf. https://docs.python.org/2/library/string.html#formatstrings
        """
        return template.format(**self._asdict())
