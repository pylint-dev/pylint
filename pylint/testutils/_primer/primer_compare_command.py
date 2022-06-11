# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt
from __future__ import annotations

import json

from pylint.testutils._primer.primer_command import PackageMessages, PrimerCommand

MAX_GITHUB_COMMENT_LENGTH = 65536


class CompareCommand(PrimerCommand):
    def run(self) -> None:
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
            if len(comment) >= MAX_GITHUB_COMMENT_LENGTH:
                break

            new_messages = all_new_messages[package]
            package_data = self.packages[package]

            if not missing_messages and not new_messages:
                continue

            comment += f"\n\n**Effect on [{package}]({self.packages[package].url}):**\n"

            # Create comment for new messages
            count = 1
            astroid_errors = 0
            new_non_astroid_messages = ""
            if new_messages:
                print("Now emitted:")
            for message in new_messages:
                filepath = str(message["path"]).replace(
                    str(package_data.clone_directory), ""
                )
                # Existing astroid errors may still show up as "new" because the timestamp
                # in the message is slightly different.
                if message["symbol"] == "astroid-error":
                    astroid_errors += 1
                else:
                    new_non_astroid_messages += (
                        f"{count}) {message['symbol']}:\n*{message['message']}*\n"
                        f"{package_data.url}/blob/{package_data.branch}{filepath}#L{message['line']}\n"
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
                comment += (
                    "The following messages are no longer emitted:\n\n<details>\n\n"
                )
                print("No longer emitted:")
            for message in missing_messages:
                comment += f"{count}) {message['symbol']}:\n*{message['message']}*\n"
                filepath = str(message["path"]).replace(
                    str(package_data.clone_directory), ""
                )
                assert not package_data.url.endswith(
                    ".git"
                ), "You don't need the .git at the end of the github url."
                comment += f"{package_data.url}/blob/{package_data.branch}{filepath}#L{message['line']}\n"
                count += 1
                print(message)
            if missing_messages:
                comment += "\n</details>\n\n"

        if comment == "":
            comment = (
                "🤖 According to the primer, this change has **no effect** on the"
                " checked open source code. 🤖🎉\n\n"
            )
        else:
            comment = (
                f"🤖 **Effect of this PR on checked open source code:** 🤖\n\n{comment}"
            )
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
        with open(self.primer_directory / "comment.txt", "w", encoding="utf-8") as f:
            f.write(comment)
