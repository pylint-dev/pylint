# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""JUnit XML reporter for pylint."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING

from pylint.reporters.base_reporter import BaseReporter

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter
    from pylint.reporters.ureports.nodes import Section


class JUnitReporter(BaseReporter):
    """Report messages in JUnit XML format."""

    name = "junit"
    extension = "xml"

    def __init__(self, output=None):
        super().__init__(output)
        self._messages_by_module: dict[str, list] = {}

    def handle_message(self, msg) -> None:
        self.messages.append(msg)
        module = msg.module or "__main__"
        self._messages_by_module.setdefault(module, []).append(msg)

    def display_messages(self, layout: Section | None) -> None:
        testsuites = ET.Element("testsuites")
        testsuites.set("name", "pylint")

        total_tests = 0
        total_failures = 0
        total_errors = 0

        for module, msgs in sorted(self._messages_by_module.items()):
            testsuite = ET.SubElement(testsuites, "testsuite")
            testsuite.set("name", module)
            testsuite.set("tests", str(len(msgs)))
            failures = sum(
                1 for m in msgs if m.category in ("warning", "error", "fatal")
            )
            errors = sum(1 for m in msgs if m.category == "fatal")
            testsuite.set("failures", str(failures))
            testsuite.set("errors", str(errors))
            testsuite.set("time", "0.0")

            for msg in msgs:
                testcase = ET.SubElement(testsuite, "testcase")
                testcase.set("classname", module)
                testcase.set("name", f"{msg.msg_id} ({msg.symbol})")
                testcase.set("time", "0.0")
                if msg.category in (
                    "warning",
                    "error",
                    "fatal",
                    "convention",
                    "refactor",
                    "info",
                ):
                    failure = ET.SubElement(testcase, "failure")
                    failure.set("message", msg.msg or "")
                    failure.set("type", msg.category)
                    location = f"{msg.path}:{msg.line}:{msg.column}"
                    failure.text = f"{location} - {msg.msg or ''}"

            total_tests += len(msgs)
            total_failures += failures
            total_errors += errors

        testsuites.set("tests", str(total_tests))
        testsuites.set("failures", str(total_failures))
        testsuites.set("errors", str(total_errors))

        xml_bytes = ET.tostring(testsuites, encoding="UTF-8", xml_declaration=True)
        self.out.write(xml_bytes.decode("UTF-8") + "\n")

    def display_reports(self, layout: Section) -> None:
        pass

    def _display(self, layout: Section) -> None:
        pass


def register(linter: PyLinter) -> None:
    linter.register_reporter(JUnitReporter)
