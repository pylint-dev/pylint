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
from linecache import getline
from typing import TYPE_CHECKING, TextIO

from pylint.message import Message
from pylint.reporters.base_reporter import BaseReporter

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter
    from pylint.reporters.ureports.nodes import Section


class JUnitReporter(BaseReporter):
    """Report messages in JUnit XML format.

    Each linted module is represented as a ``<testsuite>`` element. Every
    Pylint message for that module becomes a failing ``<testcase>`` so CI
    systems can report messages independently. Modules with no messages produce
    a passing testcase.

    Usage::

        pylint --output-format=junit mypackage/
    """

    name = "junit"
    extension = "xml"

    def __init__(self, output: TextIO | None = None) -> None:
        super().__init__(output)
        self._testsuites: dict[str, ET.Element] = {}
        self._failure_counts: defaultdict[str, int] = defaultdict(int)
        # Maps each linted module to its file path, in lint order. Used to emit
        # a passing testcase for modules that turn out to have no messages.
        self._linted_modules: dict[str, str] = {}

    def on_set_current_module(self, module: str, filepath: str | None) -> None:
        """Record each linted module so clean ones get a passing testcase.

        Pylint walks modules in two passes (collection then checking), so the
        decision of whether a module is "clean" cannot be made here: its
        messages have not been handled yet. We only record the module and defer
        the passing-testcase logic to ``display_messages``.
        """
        if filepath is None:
            return
        suite_name = module or filepath
        # Pylint reports an ``__init__.py`` here as ``pkg.__init__``, but the
        # messages raised in that file carry ``pkg`` as their module. Normalise
        # so the module and its messages are routed to the same testsuite.
        suite_name = suite_name.removesuffix(".__init__")
        self._linted_modules[suite_name] = filepath
        self._get_testsuite(suite_name)

    def handle_message(self, msg: Message) -> None:
        """Add a failing testcase for a Pylint message."""
        super().handle_message(msg)
        suite_name = msg.module or msg.path or msg.abspath or "pylint"
        testsuite_el = self._get_testsuite(suite_name)
        file_path = msg.path or msg.abspath
        source_line = getline(msg.abspath or msg.path, msg.line).strip()
        stdout_line = f"{file_path}:{msg.line}:{msg.column}:{source_line}"
        stderr_line = f"{msg.msg_id}:{msg.msg}\n{stdout_line}"
        testcase_el = ET.SubElement(
            testsuite_el,
            "testcase",
            name=f"{suite_name}:{msg.line}:{msg.column}",
            classname="pylint",
            file=file_path,
            line=str(msg.line),
        )
        # ``class`` is a Python keyword, so it cannot be passed as a kwarg.
        # pylint-junit exposes the message category under this attribute.
        testcase_el.set("class", msg.category)
        failure_el = ET.SubElement(
            testcase_el,
            "failure",
            type=msg.category,
            message=msg.symbol,
        )
        failure_el.text = stderr_line
        ET.SubElement(testcase_el, "system-out").text = stdout_line
        ET.SubElement(testcase_el, "system-err").text = stderr_line
        self._failure_counts[suite_name] += 1

    def display_messages(self, layout: Section | None) -> None:
        """Build and write JUnit XML from collected messages."""
        for suite_name, filepath in self._linted_modules.items():
            if not self._failure_counts[suite_name]:
                self._add_success_testcase(suite_name, filepath)
        testsuites_el = ET.Element("testsuites")
        total_tests = 0
        total_failures = 0
        for suite_name, testsuite_el in self._testsuites.items():
            tests = len(testsuite_el.findall("testcase"))
            if tests == 0:
                # No testcase was routed here (e.g. a module-name mismatch sent
                # its messages elsewhere); skip rather than emit an empty suite.
                continue
            failures = self._failure_counts[suite_name]
            total_tests += tests
            total_failures += failures
            testsuite_el.set("tests", str(tests))
            testsuite_el.set("errors", "0")
            testsuite_el.set("failures", str(failures))
            testsuite_el.set("skipped", "0")
            testsuite_el.set("disabled", "0")
            testsuite_el.set("time", "0")
            testsuites_el.append(testsuite_el)
        testsuites_el.set("tests", str(total_tests))
        testsuites_el.set("errors", "0")
        testsuites_el.set("failures", str(total_failures))
        testsuites_el.set("disabled", "0")
        testsuites_el.set("time", "0")
        tree = ET.ElementTree(testsuites_el)
        ET.indent(tree, space="  ")
        tree.write(self.out, encoding="unicode", xml_declaration=True)
        print(file=self.out)

    def _get_testsuite(self, name: str) -> ET.Element:
        if name not in self._testsuites:
            self._testsuites[name] = ET.Element("testsuite", name=name)
        return self._testsuites[name]

    def _add_success_testcase(self, suite_name: str, filepath: str) -> None:
        testsuite_el = self._get_testsuite(suite_name)
        stdout_line = f"All checks passed for: {filepath}"
        testcase_el = ET.SubElement(
            testsuite_el,
            "testcase",
            name=f"{suite_name}:0:0",
            classname="pylint",
            file=filepath,
        )
        ET.SubElement(testcase_el, "system-out").text = stdout_line

    def display_reports(self, layout: Section) -> None:
        """Don't do anything in this reporter."""

    def _display(self, layout: Section) -> None:
        """Do nothing."""


def register(linter: PyLinter) -> None:
    linter.register_reporter(JUnitReporter)
