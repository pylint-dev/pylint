# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import argparse
import json
import warnings
from io import StringIO
from itertools import chain
from pathlib import Path
from typing import Dict, List, Union

import git

from pylint.lint import Run
from pylint.reporters import JSONReporter
from pylint.testutils.primer import PackageToLint

TESTS_DIR = Path(__file__).parent.parent
PRIMER_DIRECTORY = TESTS_DIR / ".pylint_primer_tests/"
PACKAGES_TO_PRIME_PATH = Path(__file__).parent / "packages_to_prime.json"

PackageMessages = Dict[str, List[Dict[str, Union[str, int]]]]


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

        # All arguments for the run parser
        run_parser = self._subparsers.add_parser("run")
        run_parser.add_argument(
            "--type", choices=["main", "pr"], required=True, help="Type of primer run."
        )

        # All arguments for the compare parser
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

        # Storing arguments
        self.config = self._argument_parser.parse_args()

        self.packages = self._get_packages_to_lint_from_json(json_path)
        """All packages to prime."""

    def run(self) -> None:
        if self.config.command == "prepare":
            self._handle_prepare_command()
        if self.config.command == "run":
            self._handle_run_command()
        if self.config.command == "compare":
            self._handle_compare_command()

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
            with open(PRIMER_DIRECTORY / "commit_string.txt", encoding="utf-8") as f:
                print(f.read())

        if commit_string:
            with open(
                PRIMER_DIRECTORY / "commit_string.txt", "w", encoding="utf-8"
            ) as f:
                f.write(commit_string)

    def _handle_run_command(self) -> None:
        packages: PackageMessages = {}

        for package, data in self.packages.items():
            output = self._lint_package(data)
            packages[package] = output
            print(f"Successfully primed {package}.")

        with open(
            PRIMER_DIRECTORY / f"output_{self.config.type}.txt", "w", encoding="utf-8"
        ) as f:
            json.dump(packages, f)

        # Fail loudly (and fail CI pipelines) if any fatal errors are found,
        # unless they are astroid-errors, in which case just warn.
        # This is to avoid introducing a dependency on bleeding-edge astroid
        # for pylint CI pipelines generally, even though we want to use astroid main
        # for the purpose of diffing emitted messages and generating PR comments.
        messages = list(chain.from_iterable(packages.values()))
        astroid_errors = [msg for msg in messages if msg["symbol"] == "astroid-error"]
        other_fatal_msgs = [
            msg
            for msg in messages
            if msg["type"] == "fatal" and msg["symbol"] != "astroid-error"
        ]
        if astroid_errors:
            warnings.warn(f"Fatal errors traced to astroid:  {astroid_errors}")
        assert not other_fatal_msgs, other_fatal_msgs

    def _handle_compare_command(self) -> None:
        with open(self.config.base_file, encoding="utf-8") as f:
            main_dict: PackageMessages = json.load(f)
        with open(self.config.new_file, encoding="utf-8") as f:
            new_dict: PackageMessages = json.load(f)

        final_main_dict: PackageMessages = {}
        for package, messages in main_dict.items():
            final_main_dict[package] = []
            for message in messages:
                try:
                    new_dict[package].remove(message)
                except ValueError:
                    final_main_dict[package].append(message)

        self._create_comment(final_main_dict, new_dict)

    def _create_comment(
        self, all_missing_messages: PackageMessages, all_new_messages: PackageMessages
    ) -> None:
        comment = ""
        for package, missing_messages in all_missing_messages.items():
            new_messages = all_new_messages[package]
            package_data = self.packages[package]

            if not missing_messages and not new_messages:
                continue

            comment += f"\n\n**Effect on [{package}]({self.packages[package].url}):**\n"

            # Create comment for new messages
            count = 1
            fatal_count = 1
            new_non_fatal_messages = ""
            new_fatal_messages = ""
            if new_messages:
                print("Now emitted:")
            for message in new_messages:
                if message["type"] == "fatal":
                    filepath = str(message["path"]).replace(
                        str(package_data.clone_directory), ""
                    )
                    new_fatal_messages += (
                        f"{fatal_count}) {message['symbol']}:\n*{message['message']}*\n"
                        "**Please check your changes on the following file**:\n"
                        f"{package_data.url}/blob/{package_data.branch}{filepath}#L{message['line']}\n"
                    )
                    print(message)
                    fatal_count += 1
                else:
                    filepath = str(message["path"]).replace(
                        str(package_data.clone_directory), ""
                    )
                    new_non_fatal_messages += (
                        f"{count}) {message['symbol']}:\n*{message['message']}*\n"
                        f"{package_data.url}/blob/{package_data.branch}{filepath}#L{message['line']}\n"
                    )
                    print(message)
                    count += 1

            if new_fatal_messages:
                comment += (
                    "The following **fatal messages** are now emitted: 💣💥\n\n<details>\n\n"
                    + new_fatal_messages
                    + "\n</details>\n\n"
                )
            if new_non_fatal_messages:
                comment += (
                    "The following messages are now emitted:\n\n<details>\n\n"
                    + new_non_fatal_messages
                    + "\n</details>\n\n"
                )

            # Create comment for missing messages
            count = 1
            if missing_messages:
                comment += (
                    "The following messages are no longer emitted:\n\n<details>\n\n"
                )
                print("No longer emitted:")
            for message in missing_messages:
                comment += f"{count}) {message['symbol']}:\n*{message['message']}*\n"
                filepath = str(message["path"]).replace(
                    str(package_data.clone_directory), ""
                )
                comment += f"{package_data.url}/blob/{package_data.branch}{filepath}#L{message['line']}\n"
                count += 1
                print(message)
            if missing_messages:
                comment += "\n</details>\n\n"

        if comment == "":
            comment = "🤖 According to the primer, this change has **no effect** on the checked open source code. 🤖🎉"
        else:
            comment = (
                "🤖 **Effect of this PR on checked open source code:** 🤖\n\n" + comment
            )

        with open(PRIMER_DIRECTORY / "comment.txt", "w", encoding="utf-8") as f:
            f.write(comment)

    def _lint_package(self, data: PackageToLint) -> list[dict[str, str | int]]:
        # We want to test all the code we can
        enables = ["--enable-all-extensions", "--enable=all"]
        # Duplicate code takes too long and is relatively safe
        # TODO: Find a way to allow cyclic-import and compare output correctly
        disables = ["--disable=duplicate-code,cyclic-import"]
        arguments = data.pylint_args + enables + disables
        if data.pylintrc_relpath:
            arguments += [f"--rcfile={data.pylintrc_relpath}"]
        output = StringIO()
        reporter = JSONReporter(output)
        Run(arguments, reporter=reporter, exit=False)
        return json.loads(output.getvalue())

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
