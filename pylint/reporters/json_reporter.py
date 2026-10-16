# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""JSON reporter."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, TypedDict

from pylint.interfaces import CONFIDENCE_MAP, UNDEFINED
from pylint.message import Applicability, Edit, Fix, Message
from pylint.reporters.base_reporter import BaseReporter
from pylint.typing import MessageLocationTuple

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
        "endLine": int | None,
        "endColumn": int | None,
        "path": str,
        "symbol": str,
        "message": str,
        "message-id": str,
    },
)


class JSONReporter(BaseReporter):
    """Report messages and layouts in JSON.

    Consider using JSON2Reporter instead, as it is superior and this reporter
    is no longer maintained.
    """

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


class JSONEdit(TypedDict):
    line: int
    column: int
    endLine: int
    endColumn: int
    newText: str


class JSONFix(TypedDict):
    description: str
    applicability: str
    edits: list[JSONEdit]


class _JSONMessageFields(TypedDict):
    type: str
    message: str
    messageId: str
    symbol: str
    confidence: str
    module: str
    path: str
    absolutePath: str
    line: int
    endLine: int | None
    column: int
    endColumn: int | None
    obj: str


class JSONMessage(_JSONMessageFields, total=False):
    fix: JSONFix
    """Only present when the message can be fixed automatically.

    Columns use the same unit as the column of the message.
    """


def _serialize_fix(fix: Fix) -> JSONFix:
    return JSONFix(
        description=fix.description,
        applicability=fix.applicability.value,
        edits=[
            JSONEdit(
                line=edit.line,
                column=edit.col,
                endLine=edit.end_line,
                endColumn=edit.end_col,
                newText=edit.new_text,
            )
            for edit in fix.edits
        ],
    )


def _deserialize_fix(fix_as_json: JSONFix) -> Fix:
    return Fix(
        fix_as_json["description"],
        tuple(
            Edit(
                edit["line"],
                edit["column"],
                edit["endLine"],
                edit["endColumn"],
                edit["newText"],
            )
            for edit in fix_as_json["edits"]
        ),
        Applicability(fix_as_json["applicability"]),
    )


class JSON2Reporter(BaseReporter):
    name = "json2"
    extension = "json2"

    def display_reports(self, layout: Section) -> None:
        """Don't do anything in this reporter."""

    def _display(self, layout: Section) -> None:
        """Do nothing."""

    def display_messages(self, layout: Section | None) -> None:
        """Launch layouts display."""
        output = {
            "messages": [self.serialize(message) for message in self.messages],
            "statistics": self.serialize_stats(),
        }
        print(json.dumps(output, indent=4), file=self.out)

    @staticmethod
    def serialize(message: Message) -> JSONMessage:
        serialized = JSONMessage(
            type=message.category,
            symbol=message.symbol,
            message=message.msg or "",
            messageId=message.msg_id,
            confidence=message.confidence.name,
            module=message.module,
            obj=message.obj,
            line=message.line,
            column=message.column,
            endLine=message.end_line,
            endColumn=message.end_column,
            path=message.path,
            absolutePath=message.abspath,
        )
        if message.fix is not None:
            serialized["fix"] = _serialize_fix(message.fix)
        return serialized

    @staticmethod
    def deserialize(message_as_json: JSONMessage) -> Message:
        return Message(
            msg_id=message_as_json["messageId"],
            symbol=message_as_json["symbol"],
            msg=message_as_json["message"],
            location=MessageLocationTuple(
                abspath=message_as_json["absolutePath"],
                path=message_as_json["path"],
                module=message_as_json["module"],
                obj=message_as_json["obj"],
                line=message_as_json["line"],
                column=message_as_json["column"],
                end_line=message_as_json["endLine"],
                end_column=message_as_json["endColumn"],
            ),
            confidence=CONFIDENCE_MAP[message_as_json["confidence"]],
            fix=(
                _deserialize_fix(message_as_json["fix"])
                if "fix" in message_as_json
                else None
            ),
        )

    def serialize_stats(self) -> dict[str, str | int | dict[str, int]]:
        """Serialize the linter stats into something JSON dumpable."""
        stats = self.linter.stats

        counts_dict = {
            "fatal": stats.fatal,
            "error": stats.error,
            "warning": stats.warning,
            "refactor": stats.refactor,
            "convention": stats.convention,
            "info": stats.info,
        }

        # Calculate score based on the evaluation option
        evaluation = self.linter.config.evaluation
        try:
            note: int = eval(  # pylint: disable=eval-used
                evaluation, {}, {**counts_dict, "statement": stats.statement or 1}
            )
        except Exception as ex:  # pylint: disable=broad-except
            score: str | int = f"An exception occurred while rating: {ex}"
        else:
            score = note

        return {
            "messageTypeCount": counts_dict,
            "modulesLinted": len(stats.by_module),
            "score": score,
        }


def register(linter: PyLinter) -> None:
    linter.register_reporter(JSONReporter)
    linter.register_reporter(JSON2Reporter)
