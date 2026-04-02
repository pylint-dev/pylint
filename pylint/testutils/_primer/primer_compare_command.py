# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt
from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import PurePosixPath

from pylint.reporters.json_reporter import JSONMessage
from pylint.testutils._primer.comparator import (
    ChangedMessage,
    Comparator,
    PackageDiff,
    message_diff,
)
from pylint.testutils._primer.primer_command import PrimerCommand

MAX_GITHUB_COMMENT_LENGTH = 65536
USELESS_SUPPRESSION_RE = re.compile(r"Useless suppression of '(.+)'")


def _format_messages(
    messages: list[JSONMessage],
    source_link: Callable[[JSONMessage], str],
) -> str:
    """Format a list of messages as a numbered body for a ``<details>`` block."""
    body = ""
    for count, msg in enumerate(messages, 1):
        body += (
            f"{count}) {msg['symbol']}:\n*{msg['message']}*\n" f"{source_link(msg)}\n"
        )
    return body


class _ClassifiedMessages:
    """All message categories for a single package, pre-formatted for display."""

    __slots__ = (
        "astroid_errors",
        "changed_messages",
        "fixed_false_positives",
        "missing_messages",
        "new_false_positives",
        "new_messages",
    )

    def __init__(
        self,
        new_messages: list[JSONMessage],
        missing_messages: list[JSONMessage],
        changed_messages: list[ChangedMessage],
        source_link: Callable[[JSONMessage], str],
    ) -> None:
        astroid_errors = 0
        new_fp: list[JSONMessage] = []
        fixed_fp: list[JSONMessage] = []
        other_new: list[JSONMessage] = []
        for message in new_messages:
            if message["symbol"] == "astroid-error":
                astroid_errors += 1
            elif USELESS_SUPPRESSION_RE.match(message["message"]):
                fixed_fp.append(message)
            elif message["symbol"] == "locally-disabled":
                # A new locally-disabled means a maintainer had to add a
                # suppression comment — we introduced a false positive.
                new_fp.append(message)
            else:
                other_new.append(message)

        self.astroid_errors = astroid_errors
        self.fixed_false_positives = _format_messages(fixed_fp, source_link)
        self.new_false_positives = _format_messages(new_fp, source_link)
        self.new_messages = _format_messages(other_new, source_link)
        self.missing_messages = _format_messages(missing_messages, source_link)

        body = ""
        for count, (old, new) in enumerate(changed_messages, 1):
            body += (
                f"{count}) [{new['symbol']}]({source_link(new)}):\n"
                f"{message_diff(old, new)}\n"
            )
        self.changed_messages = body


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
        for diff in comparator:
            if len(comment) >= MAX_GITHUB_COMMENT_LENGTH:
                break
            comment += self._create_comment_for_package(diff)
        comment = (
            f"🤖 **Effect of this PR on checked open source code:** 🤖\n\n{comment}"
            if comment
            else (
                "🤖 According to the primer, this change has **no effect** on the"
                " checked open source code. 🤖🎉\n\n"
            )
        )
        return self._truncate_comment(comment)

    def _create_comment_for_package(self, diff: PackageDiff) -> str:
        package = diff.package
        url = self.packages[package].url
        clone_dir = self.packages[package].clone_directory
        commit = diff.new["commit"]

        assert not url.endswith(
            ".git"
        ), "You don't need the .git at the end of the github url."

        def _source_link(msg: JSONMessage) -> str:
            filepath = str(PurePosixPath(msg["path"]).relative_to(clone_dir))
            return f"{url}/blob/{commit}/{filepath}#L{msg['line']}"

        def _details_section(title: str, body: str) -> str:
            # Blank line after <details> required for GitHub markdown rendering.
            return f"{title}\n\n<details>\n\n{body}</details>\n\n"

        classified = _ClassifiedMessages(
            diff.new["messages"], diff.missing["messages"], diff.changed, _source_link
        )
        comment = f"\n**Effect on [{package}]({url}):**\n\n"

        if diff.changed:
            print("Changed:")
            for _, new in diff.changed:
                print(new)
        if diff.new["messages"]:
            print("Now emitted:")
            for msg in diff.new["messages"]:
                print(msg)
        if diff.missing["messages"]:
            print("No longer emitted:")
            for msg in diff.missing["messages"]:
                print(msg)

        if classified.changed_messages:
            comment += _details_section(
                "Changed messages:", classified.changed_messages
            )
        if classified.astroid_errors:
            comment += (
                f'{classified.astroid_errors} "astroid error(s)" were found. '
                "Please open the GitHub Actions log to see what failed or crashed.\n\n"
            )
        if classified.fixed_false_positives:
            comment += _details_section(
                "🎉 Fixed false positives:", classified.fixed_false_positives
            )
        if classified.new_false_positives:
            comment += _details_section(
                "😞 New false positives:", classified.new_false_positives
            )
        if classified.new_messages:
            comment += _details_section("New messages:", classified.new_messages)
        if classified.missing_messages:
            comment += _details_section(
                "Removed messages:", classified.missing_messages
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
            # Cut at the last space before the limit to avoid mid-word truncation.
            cut_point = comment.rfind(" ", 0, max_len - 10)
            if cut_point > 0:
                comment = comment[:cut_point] + "...\n"
            else:
                comment = comment[: max_len - 10] + "...\n"
            # Close any <details> tag left open by the truncation.
            if comment.count("<details>") > comment.count("</details>"):
                comment += closing_tag
            comment += suffix
        comment += hash_information
        return comment
