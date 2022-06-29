# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import json
import sys
import warnings
from io import StringIO
from itertools import chain

from pylint.lint import Run
from pylint.reporters import JSONReporter
from pylint.testutils._primer.package_to_lint import PackageToLint
from pylint.testutils._primer.primer_command import PackageMessages, PrimerCommand

GITHUB_CRASH_TEMPLATE_LOCATION = "/home/runner/.cache"
CRASH_TEMPLATE_INTRO = "There is a pre-filled template"


class RunCommand(PrimerCommand):
    def run(self) -> None:
        packages: PackageMessages = {}

        for package, data in self.packages.items():
            output = self._lint_package(data)
            packages[package] = output
            print(f"Successfully primed {package}.")

        astroid_errors = []
        other_fatal_msgs = []
        for msg in chain.from_iterable(packages.values()):
            if msg["type"] == "fatal":
                # Remove the crash template location if we're running on GitHub.
                # We were falsely getting "new" errors when the timestamp changed.
                assert isinstance(msg["message"], str)
                if GITHUB_CRASH_TEMPLATE_LOCATION in msg["message"]:
                    msg["message"] = msg["message"].rsplit(CRASH_TEMPLATE_INTRO)[0]
                if msg["symbol"] == "astroid-error":
                    astroid_errors.append(msg)
                else:
                    other_fatal_msgs.append(msg)

        with open(
            self.primer_directory
            / f"output_{'.'.join(str(i) for i in sys.version_info[:3])}_{self.config.type}.txt",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(packages, f)

        # Fail loudly (and fail CI pipelines) if any fatal errors are found,
        # unless they are astroid-errors, in which case just warn.
        # This is to avoid introducing a dependency on bleeding-edge astroid
        # for pylint CI pipelines generally, even though we want to use astroid main
        # for the purpose of diffing emitted messages and generating PR comments.
        if astroid_errors:
            warnings.warn(f"Fatal errors traced to astroid:  {astroid_errors}")
        assert not other_fatal_msgs, other_fatal_msgs

    def _lint_package(self, data: PackageToLint) -> list[dict[str, str | int]]:
        # We want to test all the code we can
        enables = ["--enable-all-extensions", "--enable=all"]
        # Duplicate code takes too long and is relatively safe
        # TODO: Find a way to allow cyclic-import and compare output correctly
        disables = ["--disable=duplicate-code,cyclic-import"]
        arguments = data.pylint_args + enables + disables
        output = StringIO()
        reporter = JSONReporter(output)
        Run(arguments, reporter=reporter, exit=False)
        return json.loads(output.getvalue())
