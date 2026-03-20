# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt
from __future__ import annotations

from pathlib import PurePosixPath

from pylint.reporters.json_reporter import OldJsonExport
from pylint.testutils._primer.comparator import (
    ChangedMessage,
    Comparator,
    message_diff,
)
from pylint.testutils._primer.primer_command import PrimerCommand

MAX_GITHUB_COMMENT_LENGTH = 65536


class CompareCommand(PrimerCommand):
    def run(self) -> None:
        comparator = Comparator.from_json(
            self.config.base_file, self.config.new_file, self.config.batches
        )
        comment = self._create_comment(comparator)
        with open(self.primer_directory / "comment.txt", "w", encoding="utf-8") as f:
            f.write(comment)

    def _create_comment(self, comparator: Comparator) -> str:
        comment = ""
        for package, missing_messages, new_messages, changed_messages in comparator:
            if len(comment) >= MAX_GITHUB_COMMENT_LENGTH:
                break
            comment += self._create_comment_for_package(
                package,
                missing_messages,
                new_messages,
                changed_messages,
                comparator.commits[package],
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
        self,
        package: str,
        missing_messages: list[OldJsonExport],
        new_messages: list[OldJsonExport],
        changed_messages: list[ChangedMessage],
        commit: str,
    ) -> str:
        url = self.packages[package].url
        clone_dir = self.packages[package].clone_directory

        assert not url.endswith(
            ".git"
        ), "You don't need the .git at the end of the github url."

        def _source_link(msg: OldJsonExport) -> str:
            filepath = str(PurePosixPath(msg["path"]).relative_to(clone_dir))
            return f"{url}/blob/{commit}/{filepath}#L{msg['line']}"

        def _details_section(title: str, body: str) -> str:
            # Two line breaks required after <details> for links to work.
            return f"{title}\n\n<details>\n\n{body}</details>\n\n"

        comment = f"\n**Effect on [{package}]({url}):**\n\n"

        # -- Changed messages (same diagnostic, different details) -----------
        if changed_messages:
            body = ""
            for count, (old, new) in enumerate(changed_messages, 1):
                body += (
                    f"{count}) [{new['symbol']}]({_source_link(new)}):\n"
                    f"{message_diff(old, new)}\n"
                )
            comment += _details_section(
                "The following messages have been changed:", body
            )

        # -- New messages ----------------------------------------------------
        astroid_errors = 0
        new_non_astroid_messages = ""
        count = 0
        for message in new_messages:
            # Existing astroid errors may still show up as "new" because the
            # timestamp in the message is slightly different.
            if message["symbol"] == "astroid-error":
                astroid_errors += 1
            else:
                count += 1
                new_non_astroid_messages += (
                    f"{count}) {message['symbol']}:\n*{message['message']}*\n"
                    f"{_source_link(message)}\n"
                )

        if astroid_errors:
            comment += (
                f'{astroid_errors} "astroid error(s)" were found. '
                "Please open the GitHub Actions log to see what failed or crashed.\n\n"
            )
        if new_non_astroid_messages:
            comment += _details_section(
                "The following messages are now emitted:", new_non_astroid_messages
            )

        # -- Missing messages ------------------------------------------------
        if missing_messages:
            body = ""
            for count, message in enumerate(missing_messages, 1):
                body += (
                    f"{count}) {message['symbol']}:\n*{message['message']}*\n"
                    f"{_source_link(message)}\n"
                )
            comment += _details_section(
                "The following messages are no longer emitted:", body
            )

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
            # Reserve space for the suffix and a potential </details> closing tag.
            suffix = f"\n{truncation_information}\n\n"
            closing_tag = "</details>\n"
            max_len = (
                MAX_GITHUB_COMMENT_LENGTH
                - len(hash_information)
                - len(suffix)
                - len(closing_tag)
            )
            comment = comment[: max_len - 10] + "...\n"
            # Close any <details> tag left open by the truncation.
            if comment.count("<details>") > comment.count("</details>"):
                comment += closing_tag
            comment += suffix
        comment += hash_information
        return comment
