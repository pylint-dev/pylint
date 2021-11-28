# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, Union

import pytest
from pytest import LogCaptureFixture

from pylint.testutils.primer import PackageToLint

PRIMER_DIRECTORY = Path(".pylint_primer_tests/").resolve()


def get_packages_to_lint_from_json(
    json_path: Union[Path, str]
) -> Dict[str, PackageToLint]:
    result: Dict[str, PackageToLint] = {}
    with open(json_path, encoding="utf8") as f:
        for name, package_data in json.load(f).items():
            result[name] = PackageToLint(**package_data)
    return result


PACKAGE_TO_LINT_JSON = Path(__file__).parent / "packages_to_lint.json"
PACKAGES_TO_LINT = get_packages_to_lint_from_json(PACKAGE_TO_LINT_JSON)
"""Dictionary of external packages used during the primer test"""


class TestPrimer:
    @staticmethod
    @pytest.mark.primer_external
    @pytest.mark.parametrize("package", PACKAGES_TO_LINT.values(), ids=PACKAGES_TO_LINT)
    def test_primer_external_packages_no_crash(
        package: PackageToLint,
        caplog: LogCaptureFixture,
    ) -> None:
        __tracebackhide__ = True  # pylint: disable=unused-variable
        TestPrimer._primer_test(package, caplog)

    @staticmethod
    def _primer_test(package: PackageToLint, caplog: LogCaptureFixture) -> None:
        """Runs pylint over external packages to check for crashes and fatal messages

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
            command = ["pylint"] + enables + disables + package.pylint_args
            logging.info("Launching primer:\n%s", " ".join(command))
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as ex:
            msg = f"Encountered {{}} during primer test for {package}"
            assert ex.returncode != 32, msg.format("a crash")
            assert ex.returncode % 2 == 0, msg.format("a message of category 'fatal'")
