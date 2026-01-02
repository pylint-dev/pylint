# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

# pylint: disable=wrong-spelling-in-comment,wrong-spelling-in-docstring

from __future__ import annotations

import json
import os.path
from textwrap import shorten
from typing import TYPE_CHECKING, Literal, TypedDict
from urllib.parse import quote

import pylint
import pylint.message
from pylint.constants import MSG_TYPES
from pylint.reporters import BaseReporter

if TYPE_CHECKING:
    from pylint.lint import PyLinter
    from pylint.reporters.ureports.nodes import Section


def register(linter: PyLinter) -> None:
    linter.register_reporter(SARIFReporter)


class SARIFReporter(BaseReporter):
    name = "sarif"
    extension = "sarif"
    linter: PyLinter

    def display_reports(self, layout: Section) -> None:
        """Don't do anything in this reporter."""

    def _display(self, layout: Section) -> None:
        """Do nothing."""

    def display_messages(self, layout: Section | None) -> None:
        """Launch layouts display."""
        output: Log = {
            "version": "2.1.0",
            "$schema": "https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/schemas/sarif-schema-2.1.0.json",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "pylint",
                            "fullName": f"pylint {pylint.__version__}",
                            "version": pylint.__version__,
                            # should be versioned but not all versions are kept so...
                            "informationUri": "https://pylint.readthedocs.io/",
                            "rules": [
                                {
                                    "id": m.msgid,
                                    "name": m.symbol,
                                    "deprecatedIds": [
                                        msgid for msgid, _ in m.old_names
                                    ],
                                    "deprecatedNames": [
                                        name for _, name in m.old_names
                                    ],
                                    # per 3.19.19 shortDescription should be a
                                    # single sentence which can't be guaranteed,
                                    # however github requires it...
                                    "shortDescription": {
                                        "text": m.description.split(".", 1)[0]
                                    },
                                    # github requires that this is less than 1024 characters
                                    "fullDescription": {
                                        "text": shorten(
                                            m.description, 1024, placeholder="..."
                                        )
                                    },
                                    "help": {"text": m.format_help()},
                                    "helpUri": f"https://pylint.readthedocs.io/en/stable/user_guide/messages/{MSG_TYPES[m.msgid[0]]}/{m.symbol}.html",
                                    # handle_message only gets the formatted message,
                                    # so to use `messageStrings` we'd need to
                                    # convert the templating and extract the args
                                    # out of the msg
                                }
                                for checker in self.linter.get_checkers()
                                for m in checker.messages
                                if m.symbol in self.linter.stats.by_msg
                            ],
                        }
                    },
                    "results": [self.serialize(message) for message in self.messages],
                }
            ],
        }
        json.dump(output, self.out)

    @staticmethod
    def serialize(message: pylint.message.Message) -> Result:
        region: Region = {
            "startLine": message.line,
            "startColumn": message.column + 1,
            "endLine": message.end_line or message.line,
            "endColumn": (message.end_column or message.column) + 1,
        }

        location: Location = {
            "physicalLocation": {
                "artifactLocation": {
                    "uri": path_to_uri(message.path),
                },
                "region": region,
            },
        }
        if message.obj:
            logical_location: LogicalLocation = {
                "name": message.obj,
                "fullyQualifiedName": f"{message.module}.{message.obj}",
            }
            location["logicalLocations"] = [logical_location]

        return {
            "ruleId": message.msg_id,
            "message": {"text": message.msg},
            "level": CATEGORY_MAP[message.category],
            "locations": [location],
            "partialFingerprints": {
                # encoding the node path seems like it would be useful to dedup alerts?
                "nodePath/v1": "",
            },
        }


def path_to_uri(path: str) -> str:
    """Converts a relative FS path to a relative URI.

    Does not check the validity of the path.

    An alternative would be to use `Path.as_uri` (on concrete path) on both the
    artifact path and a reference path, then create a relative URI from this.
    """
    if os.path.altsep:
        path = path.replace(os.path.altsep, "/")
    if os.path.sep != "/":
        path = path.replace(os.path.sep, "/")
    return quote(path)


CATEGORY_MAP: dict[str, ResultLevel] = {
    "convention": "note",
    "refactor": "note",
    "statement": "note",
    "info": "note",
    "warning": "warning",
    "error": "error",
    "fatal": "error",
}


class Run(TypedDict):
    tool: Tool
    # invocation parameters / environment for the tool
    # invocation: list[Invocations]
    results: list[Result]
    # originalUriBaseIds: dict[str, ArtifactLocation]


Log = TypedDict(
    "Log",
    {
        "version": Literal["2.1.0"],
        "$schema": Literal[
            "https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/schemas/sarif-schema-2.1.0.json"
        ],
        "runs": list[Run],
    },
)


class Tool(TypedDict):
    driver: Driver


class Driver(TypedDict):
    name: Literal["pylint"]
    # optional but azure wants it
    fullName: str
    version: str
    informationUri: str  # not required but validator wants it
    rules: list[ReportingDescriptor]


class ReportingDescriptorOpt(TypedDict, total=False):
    deprecatedIds: list[str]
    deprecatedNames: list[str]
    messageStrings: dict[str, MessageString]


class ReportingDescriptor(ReportingDescriptorOpt):
    id: str
    # optional but validator really wants it (then complains that it's not pascal cased)
    name: str
    # not required per spec but required by github
    shortDescription: MessageString
    fullDescription: MessageString
    help: MessageString
    helpUri: str


class MarkdownMessageString(TypedDict, total=False):
    markdown: str


class MessageString(MarkdownMessageString):
    text: str


ResultLevel = Literal["none", "note", "warning", "error"]


class ResultOpt(TypedDict, total=False):
    ruleId: str
    ruleIndex: int

    level: ResultLevel


class Result(ResultOpt):
    message: Message
    # not required per spec but required by github
    locations: list[Location]
    partialFingerprints: dict[str, str]


class Message(TypedDict, total=False):
    # needs to have either text or id but it's a PITA to type

    #: plain text message string (can have markdown links but no other formatting)
    text: str
    #: formatted GFM text
    markdown: str
    #: rule id
    id: str
    #: arguments for templated rule messages
    arguments: list[str]


class Location(TypedDict, total=False):
    physicalLocation: PhysicalLocation  # actually required by github
    logicalLocations: list[LogicalLocation]


class PhysicalLocation(TypedDict):
    artifactLocation: ArtifactLocation
    # not required per spec, required by github
    region: Region


class ArtifactLocation(TypedDict, total=False):
    uri: str
    #: id of base URI for resolving relative `uri`
    uriBaseId: str
    description: Message


class LogicalLocation(TypedDict, total=False):
    name: str
    fullyQualifiedName: str
    #: schema is `str` with a bunch of *suggested* terms, of which this is a subset
    kind: Literal[
        "function", "member", "module", "parameter", "returnType", "type", "variable"
    ]


class Region(TypedDict):
    # none required per spec, all required by github
    startLine: int
    startColumn: int
    endLine: int
    endColumn: int
