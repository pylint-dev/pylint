# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt
from __future__ import annotations

import json
from pathlib import Path

from pylint.testutils._primer.primer_command import PackageMessages, PrimerCommand

MAX_GITHUB_COMMENT_LENGTH = 65536


class CompareCommand(PrimerCommand):
    def run(self) -> None:
        main_messages = self._load_json(self.config.base_file)
        pr_messages = self._load_json(self.config.new_file)
        missing_messages, new_messages = self._cross_reference(
            main_messages, pr_messages
        )
        comment = self._create_comment(missing_messages, new_messages)
        with open(self.primer_directory / "comment.txt", "w", encoding="utf-8") as f:
            f.write(comment)

    @staticmethod
    def _cross_reference(
        main_dict: PackageMessages, pr_messages: PackageMessages
    ) -> tuple[PackageMessages, PackageMessages]:
        missing_messages: PackageMessages = {}
        for package, messages in main_dict.items():
            missing_messages[package] = []
            for message in messages:
                try:
                    pr_messages[package].remove(message)
                except ValueError:
                    missing_messages[package].append(message)
        return missing_messages, pr_messages

    @staticmethod
    def _load_json(file_path: Path | str) -> PackageMessages:
        with open(file_path, encoding="utf-8") as f:
            result: PackageMessages = json.load(f)
        return result

    def _create_comment(
        self, all_missing_messages: PackageMessages, all_new_messages: PackageMessages
    ) -> str:
        comment = ""
        for package, missing_messages in all_missing_messages.items():
            if len(comment) >= MAX_GITHUB_COMMENT_LENGTH:
                break
            new_messages = all_new_messages[package]
            if not missing_messages and not new_messages:
                continue
            comment += self._create_comment_for_package(
                package, new_messages, missing_messages
            )
        if comment == "":
            comment = (
                "🤖 According to the primer, this change has **no effect** on the"
                " checked open source code. 🤖🎉\n\n"
            )
        else:
            comment = (
                f"🤖 **Effect of this PR on checked open source code:** 🤖\n\n{comment}"
            )
        return self._truncate_comment(comment)

    def _create_comment_for_package(
        self, package: str, new_messages, missing_messages
    ) -> str:
        comment = f"\n\n**Effect on [{package}]({self.packages[package].url}):**\n"
        # Create comment for new messages
        count = 1
        astroid_errors = 0
        new_non_astroid_messages = ""
        if new_messages:
            print("Now emitted:")
        for message in new_messages:
            filepath = str(message["path"]).replace(
                str(self.packages[package].clone_directory), ""
            )
            # Existing astroid errors may still show up as "new" because the timestamp
            # in the message is slightly different.
            if message["symbol"] == "astroid-error":
                astroid_errors += 1
            else:
                new_non_astroid_messages += (
                    f"{count}) {message['symbol']}:\n*{message['message']}*\n"
                    f"{self.packages[package].url}/blob/{self.packages[package].branch}{filepath}#L{message['line']}\n"
                )
                print(message)
                count += 1

        if astroid_errors:
            comment += (
                f"{astroid_errors} error(s) were found stemming from the `astroid` library. "
                "This is unlikely to have been caused by your changes. "
                "A GitHub Actions warning links directly to the crash report template. "
                "Please open an issue against `astroid` if one does not exist already. \n\n"
            )
        if new_non_astroid_messages:
            comment += (
                "The following messages are now emitted:\n\n<details>\n\n"
                + new_non_astroid_messages
                + "\n</details>\n\n"
            )

        # Create comment for missing messages
        count = 1
        if missing_messages:
            comment += "The following messages are no longer emitted:\n\n<details>\n\n"
            print("No longer emitted:")
        for message in missing_messages:
            comment += f"{count}) {message['symbol']}:\n*{message['message']}*\n"
            filepath = str(message["path"]).replace(
                str(self.packages[package].clone_directory), ""
            )
            assert not self.packages[package].url.endswith(
                ".git"
            ), "You don't need the .git at the end of the github url."
            comment += f"{self.packages[package].url}/blob/{self.packages[package].branch}{filepath}#L{message['line']}\n"
            count += 1
            print(message)
        if missing_messages:
            comment += "\n</details>\n\n"
        return comment

    def _truncate_comment(self, comment: str) -> str:
        """GitHub allows only a set number of characters in a comment."""
        hash_information = (
            f"*This comment was generated for commit {self.config.commit}*"
        )
        if len(comment) + len(hash_information) >= MAX_GITHUB_COMMENT_LENGTH:
            truncation_information = (
                f"*This comment was truncated because GitHub allows only"
                f" {MAX_GITHUB_COMMENT_LENGTH} characters in a comment.*"
            )
            max_len = (
                MAX_GITHUB_COMMENT_LENGTH
                - len(hash_information)
                - len(truncation_information)
            )
            comment = f"{comment[:max_len - 10]}...\n\n{truncation_information}\n\n"
        comment += hash_information
        return comment
