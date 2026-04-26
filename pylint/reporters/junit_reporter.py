# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""JUnit XML reporter for pylint.

Outputs pylint messages in JUnit XML format, suitable for CI systems
like Azure DevOps, Jenkins, GitHub Actions, and GitLab CI that
consume JUnit XML test reports.

Each module/file is represented as a <testcase>, and pylint messages
are represented as <failure> or <skipped> elements within each testcase.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING

from pylint.interfaces import CONFIDENCE_MAP, UNDEFINED
from pylint.message import Message
from pylint.reporters.base_reporter import BaseReporter
from pylint.typing import MessageLocationTuple

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter
    from pylint.reporters.ureports.nodes import Section


class JUnitReporter(BaseReporter):
    """Report messages in JUnit XML format.

    This reporter produces JUnit-compatible XML output that can be consumed
    by CI systems like Azure DevOps, Jenkins, GitHub Actions, and GitLab CI.

    Each analyzed module becomes a <testcase>, and pylint messages become
    <failure> elements (for errors, warnings, etc.) within those testcases.

    Usage::

        pylint --output-format=junit mymodule.py > pylint-junit.xml
    """

    name = "junit"
    extension = "xml"

    def __init__(self, output: None = None) -> None:
        super().__init__(output)
        self._current_module: str | None = None
        self._current_file: str | None = None
        self._module_messages: dict[str, list[Message]] = {}

    def on_set_current_module(self, module: str, filepath: str | None) -> None:
        """Called when a module starts being analyzed."""
        self._current_module = module
        self._current_file = filepath or module
        if module not in self._module_messages:
            self._module_messages[module] = []

    def handle_message(self, msg: Message) -> None:
        """Handle a new message triggered on the current file."""
        super().handle_message(msg)
        module = msg.module or self._current_module or "unknown"
        if module not in self._module_messages:
            self._module_messages[module] = []
        self._module_messages[module].append(msg)

    def display_messages(self, layout: Section | None) -> None:
        """Build and output JUnit XML from collected messages."""
        testsuites = ET.Element("testsuites")
        testsuite = ET.SubElement(
            testsuites,
            "testsuite",
            {
                "name": "pylint",
                "tests": str(len(self._module_messages)),
                "failures": str(
                    sum(
                        1
                        for msgs in self._module_messages.values()
                        for m in msgs
                        if m.category in ("error", "fatal")
                    )
                ),
                "errors": str(
                    sum(
                        1
                        for msgs in self._module_messages.values()
                        for m in msgs
                        if m.category == "fatal"
                    )
                ),
                "skipped": str(
                    sum(
                        1
                        for msgs in self._module_messages.values()
                        for m in msgs
                        if m.category in ("warning", "refactor", "convention", "info")
                    )
                ),
            },
        )

        for module, msgs in sorted(self._module_messages.items()):
            # Determine the file path for this module
            filepath = msgs[0].path if msgs else module
            testcase = ET.SubElement(
                testsuite,
                "testcase",
                {
                    "classname": module,
                    "name": filepath,
                },
            )

            for msg in msgs:
                self._add_message_element(testcase, msg)

            # If no messages, add a success indicator (empty testcase)
            if not msgs:
                ET.SubElement(
                    testcase,
                    "system-out",
                ).text = f"No issues found in {module}"

        # Pretty-print the XML
        self._write_pretty_xml(testsuites)

    def _add_message_element(self, testcase: ET.Element, msg: Message) -> None:
        """Add a failure or skipped element for a message."""
        # Build location string
        location = f"{msg.path}:{msg.line}:{msg.column}"
        if msg.end_line and msg.end_column:
            location += f"-{msg.end_line}:{msg.end_column}"

        message_text = f"[{msg.msg_id}({msg.symbol})] {msg.msg} at {location}"

        if msg.category in ("error", "fatal"):
            failure = ET.SubElement(
                testcase,
                "failure",
                {
                    "type": msg.category,
                    "message": message_text,
                },
            )
            failure.text = f"""{msg.msg_id}: {msg.symbol}
Message: {msg.msg}
Location: {location}
Module: {msg.module}
Object: {msg.obj or 'N/A'}
Confidence: {msg.confidence.name}"""
        else:
            skipped = ET.SubElement(
                testcase,
                "skipped",
                {
                    "type": msg.category,
                    "message": message_text,
                },
            )
            skipped.text = f"""{msg.msg_id}: {msg.symbol}
Message: {msg.msg}
Location: {location}
Category: {msg.category}
Confidence: {msg.confidence.name}"""

    def _write_pretty_xml(self, element: ET.Element) -> None:
        """Write pretty-printed XML to output."""
        # Use ET.tostring for serialization, then pretty-print
        xml_string = ET.tostring(element, encoding="unicode")
        # Basic pretty-printing: add newlines and indentation
        import re
        # Add XML declaration
        pretty_xml = '<?xml version="1.0" encoding="utf-8"?>\n'
        # Simple indentation-based pretty printing
        indent_level = 0
        in_element = False
        result = []
        i = 0
        while i < len(xml_string):
            char = xml_string[i]
            if char == '<':
                if xml_string[i + 1] == '/':
                    indent_level -= 1
                    result.append('\n' + '  ' * indent_level)
                elif i > 0 and xml_string[i - 1] != '\n':
                    result.append('\n' + '  ' * indent_level)
                result.append(char)
                in_element = True
            elif char == '>' and in_element:
                result.append(char)
                if xml_string[i - 1] != '/' and not (i + 1 < len(xml_string) and xml_string[i + 1:i + 3] == '</'):
                    if i + 1 < len(xml_string) and xml_string[i + 1] == '<' and xml_string[i + 2] != '/':
                        indent_level += 1
                in_element = False
            else:
                result.append(char)
            i += 1

        pretty_xml += ''.join(result).strip()
        print(pretty_xml, file=self.out)

    def display_reports(self, layout: Section) -> None:
        """Don't display additional reports in JUnit output."""

    def _display(self, layout: Section) -> None:
        """Do nothing."""

    @staticmethod
    def serialize(message: Message) -> dict[str, str | int | None]:
        """Serialize a Message to a dictionary."""
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
            "confidence": message.confidence.name,
        }

    @staticmethod
    def deserialize(message_as_json: dict[str, str | int | None]) -> Message:
        """Deserialize a dictionary back to a Message."""
        return Message(
            msg_id=str(message_as_json["message-id"]),
            symbol=str(message_as_json["symbol"]),
            msg=str(message_as_json["message"]),
            location=MessageLocationTuple(
                abspath=str(message_as_json.get("path", "")),
                path=str(message_as_json.get("path", "")),
                module=str(message_as_json.get("module", "")),
                obj=str(message_as_json.get("obj", "")),
                line=int(message_as_json.get("line", 0)),
                column=int(message_as_json.get("column", 0)),
                end_line=message_as_json.get("endLine"),  # type: ignore[arg-type]
                end_column=message_as_json.get("endColumn"),  # type: ignore[arg-type]
            ),
            confidence=CONFIDENCE_MAP.get(
                str(message_as_json.get("confidence", "UNDEFINED")), UNDEFINED
            ),
        )


def register(linter: PyLinter) -> None:
    linter.register_reporter(JUnitReporter)
