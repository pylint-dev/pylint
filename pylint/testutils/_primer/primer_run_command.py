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
from pylint.message import Message
from pylint.reporters import JSONReporter
from pylint.testutils._primer.package_to_lint import PackageToLint
from pylint.testutils._primer.primer_command import PackageMessages, PrimerCommand

GITHUB_CRASH_TEMPLATE_LOCATION = "/home/runner/.cache"
CRASH_TEMPLATE_INTRO = "There is a pre-filled template"


class RunCommand(PrimerCommand):
    def run(self) -> None:
        packages: PackageMessages = {}

        for package, data in self.packages.items():
            packages[package] = self._lint_package(data)
            print(f"Successfully primed {package}.")

        astroid_errors = []
        other_fatal_msgs = []
        for msg in chain.from_iterable(packages.values()):
            if msg.category == "fatal":
                if GITHUB_CRASH_TEMPLATE_LOCATION in msg.msg:
                    # Remove the crash template location if we're running on GitHub.
                    # We were falsely getting "new" errors when the timestamp changed.
                    msg.msg = msg.msg.rsplit(CRASH_TEMPLATE_INTRO)[0]
                if msg.symbol == "astroid-error":
                    astroid_errors.append(msg)
                else:
                    other_fatal_msgs.append(msg)

        with open(
            self.primer_directory
            / f"output_{'.'.join(str(i) for i in sys.version_info[:3])}_{self.config.type}.txt",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                {
                    p: [JSONReporter.serialize(m) for m in msgs]
                    for p, msgs in packages.items()
                },
                f,
            )

        # Fail loudly (and fail CI pipelines) if any fatal errors are found,
        # unless they are astroid-errors, in which case just warn.
        # This is to avoid introducing a dependency on bleeding-edge astroid
        # for pylint CI pipelines generally, even though we want to use astroid main
        # for the purpose of diffing emitted messages and generating PR comments.
        if astroid_errors:
            warnings.warn(f"Fatal errors traced to astroid:  {astroid_errors}")
        assert not other_fatal_msgs, other_fatal_msgs

    def _lint_package(self, data: PackageToLint) -> list[Message]:
        # We want to test all the code we can
        enables = ["--enable-all-extensions", "--enable=all"]
        # Duplicate code takes too long and is relatively safe
        # TODO: Find a way to allow cyclic-import and compare output correctly
        disables = ["--disable=duplicate-code,cyclic-import"]
        arguments = data.pylint_args + enables + disables
        output = StringIO()
        reporter = JSONReporter(output)
        Run(arguments, reporter=reporter, exit=False)
        return [JSONReporter.deserialize(m) for m in json.loads(output.getvalue())]
