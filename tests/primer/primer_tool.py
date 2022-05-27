# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import argparse
import json
from pathlib import Path

import git

from pylint.testutils.primer import PackageToLint

MAIN_DIR = Path(__file__).parent.parent.parent
PRIMER_DIRECTORY = MAIN_DIR / ".pylint_primer_tests/"
PACKAGES_TO_PRIME_PATH = Path(__file__).parent / "packages_to_prime.json"


class Primer:
    """Main class to handle priming of packages."""

    def __init__(self, json_path: Path) -> None:
        # Preparing arguments
        self._argument_parser = argparse.ArgumentParser(prog="Pylint Primer")
        self._subparsers = self._argument_parser.add_subparsers(dest="command")

        # All arguments for the prepare parser
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

        # Storing arguments
        self.config = self._argument_parser.parse_args()

        self.packages = self._get_packages_to_lint_from_json(json_path)
        """All packages to prime."""

    def run(self) -> None:
        if self.config.command == "prepare":
            self._handle_prepare_command()

    def _handle_prepare_command(self) -> None:
        commit_string = ""
        if self.config.clone:
            for package, data in self.packages.items():
                local_commit = data.lazy_clone()
                print(f"Cloned '{package}' at commit '{local_commit}'.")
                commit_string += local_commit + "_"
        elif self.config.check:
            for package, data in self.packages.items():
                local_commit = git.Repo(data.clone_directory).head.object.hexsha
                print(f"Found '{package}' at commit '{local_commit}'.")
                commit_string += local_commit + "_"
        elif self.config.make_commit_string:
            for package, data in self.packages.items():
                remote_sha1_commit = (
                    git.cmd.Git().ls_remote(data.url, data.branch).split("\t")[0]
                )
                print(f"'{package}' remote is at commit '{remote_sha1_commit}'.")
                commit_string += remote_sha1_commit + "_"
        elif self.config.read_commit_string:
            with open("commit_string.txt", encoding="utf-8") as f:
                print(f.read())

        if commit_string:
            with open("commit_string.txt", "w", encoding="utf-8") as f:
                f.write(commit_string)

    @staticmethod
    def _get_packages_to_lint_from_json(json_path: Path) -> dict[str, PackageToLint]:
        with open(json_path, encoding="utf8") as f:
            return {
                name: PackageToLint(**package_data)
                for name, package_data in json.load(f).items()
            }


if __name__ == "__main__":
    primer = Primer(PACKAGES_TO_PRIME_PATH)
    primer.run()
