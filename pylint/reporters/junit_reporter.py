# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""JUnit XML reporter."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING

from pylint.reporters.base_reporter import BaseReporter

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter
    from pylint.reporters.ureports.nodes import Section
    from pylint.utils import LinterStats


class JUnitReporter(BaseReporter):
    """Report messages in JUnit XML format."""

    name = "junit"
    extension = "xml"

    def __init__(self, output: str | None = None) -> None:
        super().__init__(output)
        self._messages_by_file: dict[str, list[dict]] = {}

    def handle_message(self, msg: object) -> None:
        """Collect a message."""
        # Import here to avoid circular imports
        from pylint.message import Message

        if not isinstance(msg, Message):
            return
        msg_data = {
            "line": msg.line,
            "column": msg.column,
            "end_line": msg.end_line,
            "end_column": msg.end_column,
            "symbol": msg.symbol,
            "msg_id": msg.msg_id,
            "category": msg.category,
            "msg": msg.msg or "",
            "path": msg.path,
        }
        self._messages_by_file.setdefault(msg.path, []).append(msg_data)

    def display_messages(self, layout: Section | None) -> None:
        """Nothing to display mid-run."""

    def _display(self, layout: Section) -> None:
        """Nothing to display."""

    def on_close(
        self,
        stats: LinterStats,
        previous_stats: LinterStats | None,
    ) -> None:
        """Output JUnit XML on close."""
        testsuites = ET.Element("testsuites")
        total_tests = 0

        for filepath, messages in self._messages_by_file.items():
            testsuite = ET.SubElement(testsuites, "testsuite")
            testsuite.set("name", filepath)
            testsuite.set("tests", str(len(messages)))
            testsuite.set(
                "failures",
                str(
                    sum(
                        1
                        for m in messages
                        if m["category"]
                        in ("error", "warning", "refactor", "convention")
                    )
                ),
            )
            testsuite.set(
                "errors", str(sum(1 for m in messages if m["category"] == "fatal"))
            )
            testsuite.set("skipped", "0")

            for msg in messages:
                testcase = ET.SubElement(testsuite, "testcase")
                testcase.set("classname", filepath)
                testcase.set("name", f"{msg['symbol']} ({msg['msg_id']})")
                testcase.set("line", str(msg["line"]))

                if msg["category"] in (
                    "error",
                    "warning",
                    "refactor",
                    "convention",
                    "fatal",
                ):
                    failure = ET.SubElement(testcase, "failure")
                    failure.set("type", msg["category"])
                    failure.set("message", msg["msg"])
                    location = f"{filepath}:{msg['line']}:{msg['column']}"
                    failure.text = f"{location} {msg['symbol']}: {msg['msg']}"

            total_tests += len(messages)

        testsuites.set("tests", str(total_tests))
        testsuites.set(
            "failures",
            str(
                sum(
                    1
                    for msgs in self._messages_by_file.values()
                    for m in msgs
                    if m["category"] in ("error", "warning", "refactor", "convention")
                )
            ),
        )

        tree = ET.ElementTree(testsuites)
        ET.indent(tree, space="  ")
        tree.write(self.out, encoding="unicode", xml_declaration=True)


def register(linter: PyLinter) -> None:
    linter.register_reporter(JUnitReporter)
