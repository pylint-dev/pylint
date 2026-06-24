# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from pathlib import Path

from pylint.testutils._primer import PackageToLint
from pylint.testutils._primer.primer_configuration import (
    get_argument_parser,
    get_packages_to_prime_from_json,
)
from pylint.testutils._primer.primer_prepare_command import PrepareCommand
from pylint.testutils._primer.pyreverse_primer_command import PyreversePrimerCommand
from pylint.testutils._primer.pyreverse_primer_compare_command import CompareCommand
from pylint.testutils._primer.pyreverse_primer_run_command import RunCommand
from pylint.testutils._primer.pyreverse_primer_target import PyreversePrimerTarget


class PyreversePrimer:
    """Main class to handle pyreverse primer snapshots."""

    def __init__(
        self,
        primer_directory: Path,
        packages_path: Path,
    ) -> None:
        self.primer_directory = primer_directory
        self._argument_parser = get_argument_parser(
            "Pylint Pyreverse Primer", with_batches=False
        )

        self.config = self._argument_parser.parse_args()
        packages_to_prime = get_packages_to_prime_from_json(packages_path)
        self.targets = self._get_targets_from_packages(packages_to_prime)
        self.packages = self._filter_packages_for_pyreverse(packages_to_prime)

        if self.config.command == "prepare":
            self.command: PrepareCommand | PyreversePrimerCommand = PrepareCommand(
                self.primer_directory, self.packages, self.config
            )
        elif self.config.command == "run":
            self.command = RunCommand(
                self.primer_directory, self.packages, self.targets, self.config
            )
        else:
            self.command = CompareCommand(
                self.primer_directory, self.packages, self.targets, self.config
            )

    def run(self) -> None:
        self.command.run()

    @staticmethod
    def _get_targets_from_packages(
        packages: dict[str, PackageToLint],
    ) -> dict[str, PyreversePrimerTarget]:
        return {
            target_name: PyreversePrimerTarget(package=package_name, **target_data)
            for package_name, package in packages.items()
            for target_name, target_data in package.pyreverse_targets.items()
        }

    @staticmethod
    def _filter_packages_for_pyreverse(
        packages: dict[str, PackageToLint],
    ) -> dict[str, PackageToLint]:
        return {
            package_name: package
            for package_name, package in packages.items()
            if package.pyreverse_targets
        }
