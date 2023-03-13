# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import json
import logging
import subprocess
from pathlib import Path

import pytest
from pytest import LogCaptureFixture

from pylint.testutils._primer import PackageToLint

PRIMER_DIRECTORY = (Path("tests") / ".pylint_primer_tests/").resolve()


def get_packages_to_lint_from_json(json_path: Path | str) -> dict[str, PackageToLint]:
    with open(json_path, encoding="utf8") as f:
        return {
            name: PackageToLint(**package_data)
            for name, package_data in json.load(f).items()
        }


PACKAGE_TO_LINT_JSON_BATCH_ONE = (
    Path(__file__).parent / "packages_to_lint_batch_one.json"
)
PACKAGES_TO_LINT_BATCH_ONE = get_packages_to_lint_from_json(
    PACKAGE_TO_LINT_JSON_BATCH_ONE
)
"""Dictionary of external packages used during the primer test in batch one."""


class TestPrimer:
    @staticmethod
    @pytest.mark.primer_external_batch_one
    @pytest.mark.parametrize(
        "package", PACKAGES_TO_LINT_BATCH_ONE.values(), ids=PACKAGES_TO_LINT_BATCH_ONE
    )
    def test_primer_external_packages_no_crash_batch_one(
        package: PackageToLint,
        caplog: LogCaptureFixture,
    ) -> None:
        __tracebackhide__ = True  # pylint: disable=unused-variable
        TestPrimer._primer_test(package, caplog)

    @staticmethod
    def _primer_test(package: PackageToLint, caplog: LogCaptureFixture) -> None:
        """Runs pylint over external packages to check for crashes and fatal messages.

        We only check for crashes (bit-encoded exit code 32) and fatal messages
        (bit-encoded exit code 1). We assume that these external repositories do not
        have any fatal errors in their code so that any fatal errors are pylint false
        positives
        """
        caplog.set_level(logging.INFO)
        package.lazy_clone()

        try:
            # We want to test all the code we can
            enables = ["--enable-all-extensions", "--enable=all"]
            # Duplicate code takes too long and is relatively safe
            disables = ["--disable=duplicate-code"]
            command = ["pylint", *enables, *disables, *package.pylint_args]
            logging.info("Launching primer:\n%s", " ".join(command))
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as ex:
            msg = f"Encountered {{}} during primer test for {package}"
            assert ex.returncode != 32, msg.format("a crash")
            assert ex.returncode % 2 == 0, msg.format("a message of category 'fatal'")
