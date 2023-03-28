# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""JSON reporter."""

from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING, Optional

from pylint.interfaces import UNDEFINED, Confidence
from pylint.message import Message
from pylint.reporters.base_reporter import BaseReporter
from pylint.typing import MessageLocationTuple

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter
    from pylint.reporters.ureports.nodes import Section

# Since message-id is an invalid name we need to use the alternative syntax
OldJsonExport = TypedDict(
    "OldJsonExport",
    {
        "type": str,
        "module": str,
        "obj": str,
        "line": int,
        "column": int,
        "endLine": Optional[int],
        "endColumn": Optional[int],
        "path": str,
        "symbol": str,
        "message": str,
        "message-id": str,
    },
)


class JSONExport(OldJsonExport):
    confidence: Confidence
    abspath: str


class BaseJSONReporter(BaseReporter):
    """Report messages and layouts in JSON."""

    name = "json"
    extension = "json"

    def display_messages(self, layout: Section | None) -> None:
        """Launch layouts display."""
        json_dumpable = [self.serialize(message) for message in self.messages]
        print(json.dumps(json_dumpable, indent=4), file=self.out)

    def display_reports(self, layout: Section) -> None:
        """Don't do anything in this reporter."""

    def _display(self, layout: Section) -> None:
        """Do nothing."""

    @staticmethod
    def serialize(message: Message) -> OldJsonExport:
        raise NotImplementedError

    @staticmethod
    def deserialize(message_as_json: OldJsonExport) -> Message:
        raise NotImplementedError


class OldJSONReporter(BaseJSONReporter):

    """TODO: Remove in 4.0."""

    @staticmethod
    def serialize(message: Message) -> OldJsonExport:
        return {
            "type": message.category,
            "module": message.module,
            "obj": message.obj,
            "line": message.line,
            "column": message.column,
            "endLine": message.end_line,
            "endColumn": message.end_column,
            "path": message.path,
            "symbol": message.symbol,
            "message": message.msg or "",
            "message-id": message.msg_id,
        }

    @staticmethod
    def deserialize(message_as_json: OldJsonExport) -> Message:
        return Message(
            msg_id=message_as_json["message-id"],
            symbol=message_as_json["symbol"],
            msg=message_as_json["message"],
            location=MessageLocationTuple(
                abspath=message_as_json["path"],
                path=message_as_json["path"],
                module=message_as_json["module"],
                obj=message_as_json["obj"],
                line=message_as_json["line"],
                column=message_as_json["column"],
                end_line=message_as_json["endLine"],
                end_column=message_as_json["endColumn"],
            ),
            confidence=UNDEFINED,
        )


class JSONReporter(BaseJSONReporter):
    @staticmethod
    def serialize(message: Message) -> JSONExport:
        return {
            "type": message.category,
            "module": message.module,
            "obj": message.obj,
            "line": message.line,
            "column": message.column,
            "endLine": message.end_line,
            "endColumn": message.end_column,
            "path": message.path,
            "symbol": message.symbol,
            "message": message.msg or "",
            "message-id": message.msg_id,
            "confidence": message.confidence,
            "abspath": message.abspath,
        }

    @staticmethod
    def deserialize(message_as_json: JSONExport) -> Message:
        return Message(
            msg_id=message_as_json["message-id"],
            symbol=message_as_json["symbol"],
            msg=message_as_json["message"],
            location=MessageLocationTuple(
                abspath=message_as_json["abspath"],
                path=message_as_json["path"],
                module=message_as_json["module"],
                obj=message_as_json["obj"],
                line=message_as_json["line"],
                column=message_as_json["column"],
                end_line=message_as_json["endLine"],
                end_column=message_as_json["endColumn"],
            ),
            confidence=message_as_json["confidence"],
        )


def register(linter: PyLinter) -> None:
    linter.register_reporter(OldJSONReporter)
    linter.register_reporter(JSONReporter)
