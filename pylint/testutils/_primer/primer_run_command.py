# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import json
import sys
import warnings
from io import StringIO

from pylint.lint import Run
from pylint.message import Message
from pylint.reporters import JSONReporter
from pylint.reporters.json_reporter import OldJsonExport
from pylint.testutils._primer.package_to_lint import PackageToLint
from pylint.testutils._primer.primer_command import PrimerCommand

GITHUB_CRASH_TEMPLATE_LOCATION = "/home/runner/.cache"
CRASH_TEMPLATE_INTRO = "There is a pre-filled template"


class RunCommand(PrimerCommand):
    def run(self) -> None:
        packages: dict[str, list[OldJsonExport]] = {}
        astroid_errors: list[Message] = []
        other_fatal_msgs: list[Message] = []
        for package, data in self.packages.items():
            messages, p_astroid_errors, p_other_fatal_msgs = self._lint_package(
                package, data
            )
            astroid_errors += p_astroid_errors
            other_fatal_msgs += p_other_fatal_msgs
            packages[package] = messages
        plural = "s" if len(other_fatal_msgs) > 1 else ""
        assert not other_fatal_msgs, (
            f"We encountered {len(other_fatal_msgs)} fatal error message{plural}"
            " that can't be attributed to bleeding edge astroid alone (see log)."
        )
        path = (
            self.primer_directory
            / f"output_{'.'.join(str(i) for i in sys.version_info[:3])}_{self.config.type}.txt"
        )
        print(f"Writing result in {path}")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(packages, f)

    def _filter_astroid_errors(
        self, messages: list[OldJsonExport]
    ) -> tuple[list[Message], list[Message]]:
        """This is to avoid introducing a dependency on bleeding-edge astroid."""
        astroid_errors = []
        other_fatal_msgs = []
        for raw_message in messages:
            message = JSONReporter.deserialize(raw_message)
            if message.category == "fatal":
                if GITHUB_CRASH_TEMPLATE_LOCATION in message.msg:
                    # Remove the crash template location if we're running on GitHub.
                    # We were falsely getting "new" errors when the timestamp changed.
                    message.msg = message.msg.rsplit(CRASH_TEMPLATE_INTRO)[0]
                if message.symbol == "astroid-error":
                    astroid_errors.append(message)
                else:
                    other_fatal_msgs.append(message)
        return astroid_errors, other_fatal_msgs

    def _lint_package(
        self, package_name: str, data: PackageToLint
    ) -> tuple[list[OldJsonExport], list[Message], list[Message]]:
        # We want to test all the code we can
        enables = ["--enable-all-extensions", "--enable=all"]
        # Duplicate code takes too long and is relatively safe
        # TODO: Find a way to allow cyclic-import and compare output correctly
        disables = ["--disable=duplicate-code,cyclic-import"]
        arguments = data.pylint_args + enables + disables
        output = StringIO()
        reporter = JSONReporter(output)
        print(f"Running 'pylint {', '.join(arguments)}'")
        pylint_exit_code = -1
        try:
            Run(arguments, reporter=reporter)
        except SystemExit as e:
            pylint_exit_code = int(e.code)
        readable_messages: str = output.getvalue()
        messages: list[OldJsonExport] = json.loads(readable_messages)
        astroid_errors: list[Message] = []
        other_fatal_msgs: list[Message] = []
        if pylint_exit_code % 2 == 0:
            print(f"Successfully primed {package_name}.")
        else:
            print(
                f"Encountered fatal errors while priming {package_name} !\n{readable_messages}"
            )
            astroid_errors, other_fatal_msgs = self._filter_astroid_errors(messages)
            if astroid_errors:
                warnings.warn(f"Fatal errors traced to astroid: {astroid_errors}")
        return messages, astroid_errors, other_fatal_msgs
