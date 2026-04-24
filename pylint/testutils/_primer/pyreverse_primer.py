# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pylint.testutils._primer import PackageToLint
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
        targets_path: Path,
    ) -> None:
        self.primer_directory = primer_directory
        self._argument_parser = argparse.ArgumentParser(prog="Pylint Pyreverse Primer")
        self._subparsers = self._argument_parser.add_subparsers(
            dest="command", required=True
        )

        prepare_parser = self._subparsers.add_parser("prepare")
        prepare_parser.add_argument(
            "--clone", help="Clone all packages.", action="store_true", default=False
        )
        prepare_parser.add_argument(
            "--check",
            help="Check consistencies and commits of all packages.",
            action="store_true",
            default=False,
        )
        prepare_parser.add_argument(
            "--make-commit-string",
            help="Get latest commit string.",
            action="store_true",
            default=False,
        )
        prepare_parser.add_argument(
            "--read-commit-string",
            help="Print latest commit string.",
            action="store_true",
            default=False,
        )

        run_parser = self._subparsers.add_parser("run")
        run_parser.add_argument(
            "--type", choices=["main", "pr"], required=True, help="Type of primer run."
        )

        compare_parser = self._subparsers.add_parser("compare")
        compare_parser.add_argument(
            "--base-file",
            required=True,
            help="Location of output file of the base run.",
        )
        compare_parser.add_argument(
            "--new-file",
            required=True,
            help="Location of output file of the new run.",
        )
        compare_parser.add_argument(
            "--commit",
            required=True,
            help="Commit hash of the PR commit being checked.",
        )

        self.config = self._argument_parser.parse_args()
        self.targets = self._get_targets_from_json(targets_path)
        self.packages = self._get_packages_to_prime_from_json(
            packages_path, self.targets
        )

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
    def _minimum_python_supported(package_data: dict[str, str]) -> bool:
        min_python_str = package_data.get("minimum_python", None)
        if not min_python_str:
            return True
        min_python_tuple = tuple(int(n) for n in min_python_str.split("."))
        return min_python_tuple <= sys.version_info[:2]

    @staticmethod
    def _get_targets_from_json(
        json_path: Path,
    ) -> dict[str, PyreversePrimerTarget]:
        with open(json_path, encoding="utf-8") as stream:
            return {
                name: PyreversePrimerTarget(**target_data)
                for name, target_data in json.load(stream).items()
            }

    @staticmethod
    def _get_packages_to_prime_from_json(
        json_path: Path,
        targets: dict[str, PyreversePrimerTarget],
    ) -> dict[str, PackageToLint]:
        with open(json_path, encoding="utf-8") as stream:
            packages_to_prime = {
                name: PackageToLint(**package_data)
                for name, package_data in json.load(stream).items()
                if PyreversePrimer._minimum_python_supported(package_data)
            }

        package_names = {target.package for target in targets.values()}
        return {
            package_name: packages_to_prime[package_name]
            for package_name in package_names
            if package_name in packages_to_prime
        }
