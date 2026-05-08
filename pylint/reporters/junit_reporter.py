# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""JUnit XML reporter.

Produces JUnit-compatible XML output for CI/CD integration with
Jenkins, Azure DevOps, GitLab CI, GitHub Actions, and other tools
that consume JUnit XML test results.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import TYPE_CHECKING

from pylint.message import Message
from pylint.reporters.base_reporter import BaseReporter

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter
    from pylint.reporters.ureports.nodes import Section


class JUnitReporter(BaseReporter):
    """Report messages in JUnit XML format.

    Each linted module is represented as a ``<testcase>`` element. Pylint
    messages for that module become ``<failure>`` children of the testcase.
    Modules with no messages produce a passing (empty) testcase.

    Usage::

        pylint --output-format=junit mypackage/
    """

    name = "junit"
    extension = "xml"

    def display_messages(self, layout: Section | None) -> None:
        """Build and write JUnit XML from collected messages."""
        # Group messages by module
        messages_by_module: dict[str, list[Message]] = defaultdict(list)
        for msg in self.messages:
            messages_by_module[msg.module].append(msg)

        # Build XML tree
        testsuites_el = ET.Element("testsuites")
        testsuite_el = ET.SubElement(testsuites_el, "testsuite", name="pylint")

        total_failures = 0
        total_errors = 0
        total_tests = 0

        # Pylint categories that map to JUnit <error> elements.
        # Fatal means pylint itself couldn't process the file;
        # error means a likely bug in the user's code.
        # Everything else (warning, convention, refactor, info)
        # maps to JUnit <failure>.
        error_categories = frozenset({"error", "fatal"})

        # Create a testcase for each module that has messages
        for module_name in sorted(messages_by_module):
            module_messages = messages_by_module[module_name]
            testcase_el = ET.SubElement(
                testsuite_el,
                "testcase",
                name=module_name,
                classname=module_name,
            )
            total_tests += 1

            for msg in module_messages:
                detail_msg = (
                    f"{msg.msg_id}({msg.symbol}): {msg.msg or ''} (line {msg.line})"
                )
                # Use <error> for error/fatal, <failure> for everything else
                if msg.category in error_categories:
                    element_tag = "error"
                    total_errors += 1
                else:
                    element_tag = "failure"
                    total_failures += 1
                result_el = ET.SubElement(
                    testcase_el,
                    element_tag,
                    type=msg.category,
                    message=detail_msg,
                )
                result_el.text = (
                    f"{msg.abspath}:{msg.line}: [{msg.msg_id}({msg.symbol})] "
                    f"{msg.msg or ''}"
                )

        # Set testsuite summary attributes
        testsuite_el.set("tests", str(total_tests))
        testsuite_el.set("errors", str(total_errors))
        testsuite_el.set("failures", str(total_failures))

        # Write XML to output
        tree = ET.ElementTree(testsuites_el)
        ET.indent(tree, space="  ")
        tree.write(self.out, encoding="unicode", xml_declaration=True)
        # Ensure final newline
        print(file=self.out)

    def display_reports(self, layout: Section) -> None:
        """Don't do anything in this reporter."""

    def _display(self, layout: Section) -> None:
        """Do nothing."""


def register(linter: PyLinter) -> None:
    linter.register_reporter(JUnitReporter)
