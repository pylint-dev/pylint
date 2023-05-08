# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt
from __future__ import annotations

from pathlib import PurePosixPath

from pylint.testutils._primer.comparator import Comparator
from pylint.testutils._primer.primer_command import Messages, PrimerCommand

MAX_GITHUB_COMMENT_LENGTH = 65536


class CompareCommand(PrimerCommand):
    def run(self) -> None:
        comparator = Comparator(self.config.base_file, self.config.new_file)
        comment = self._create_comment(comparator)
        with open(self.primer_directory / "comment.txt", "w", encoding="utf-8") as f:
            f.write(comment)

    def _create_comment(self, comparator: Comparator) -> str:
        comment = ""
        for package, missing_messages, new_messages in comparator:
            if len(comment) >= MAX_GITHUB_COMMENT_LENGTH:
                break
            new_messages = all_new_messages[package]
            if not missing_messages["messages"] and not new_messages["messages"]:
                continue
            comment += self._create_comment_for_package(
                package, missing_messages, new_messages
            )
        comment = (
            f"🤖 **Effect of this PR on checked open source code:** 🤖\n\n{comment}"
            if comment
            else (
                "🤖 According to the primer, this change has **no effect** on the"
                " checked open source code. 🤖🎉\n\n"
            )
        )
        return self._truncate_comment(comment)

    def _create_comment_for_package(
        self, package: str, missing_messages: Messages, new_messages: Messages
    ) -> str:
        comment = f"\n\n**Effect on [{package}]({self.packages[package].url}):**\n"
        # Create comment for new messages
        count = 1
        astroid_errors = 0
        new_non_astroid_messages = ""
        if new_messages["messages"]:
            print("Now emitted:")
        for message in new_messages["messages"]:
            filepath = str(
                PurePosixPath(message["path"]).relative_to(
                    self.packages[package].clone_directory
                )
            )
            # Existing astroid errors may still show up as "new" because the timestamp
            # in the message is slightly different.
            if message["symbol"] == "astroid-error":
                astroid_errors += 1
            else:
                new_non_astroid_messages += (
                    f"{count}) {message['symbol']}:\n*{message['message']}*\n"
                    f"{self.packages[package].url}/blob/{new_messages['commit']}/{filepath}#L{message['line']}\n"
                )
                print(message)
                count += 1

        if astroid_errors:
            comment += (
                f'{astroid_errors} "astroid error(s)" were found. '
                "Please open the GitHub Actions log to see what failed or crashed.\n\n"
            )
        if new_non_astroid_messages:
            comment += (
                "The following messages are now emitted:\n\n<details>\n\n"
                + new_non_astroid_messages
                + "\n</details>\n\n"
            )

        # Create comment for missing messages
        count = 1
        if missing_messages["messages"]:
            comment += "The following messages are no longer emitted:\n\n<details>\n\n"
            print("No longer emitted:")
        for message in missing_messages["messages"]:
            comment += f"{count}) {message['symbol']}:\n*{message['message']}*\n"
            filepath = str(
                PurePosixPath(message["path"]).relative_to(
                    self.packages[package].clone_directory
                )
            )
            assert not self.packages[package].url.endswith(
                ".git"
            ), "You don't need the .git at the end of the github url."
            comment += (
                f"{self.packages[package].url}"
                f"/blob/{new_messages['commit']}/{filepath}#L{message['line']}\n"
            )
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
