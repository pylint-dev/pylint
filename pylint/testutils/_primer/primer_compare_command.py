# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt
from __future__ import annotations

from collections.abc import Callable
from pathlib import PurePosixPath

from pylint.reporters.json_reporter import JSONMessage
from pylint.testutils._primer.comparator import (
    ChangedMessage,
    Comparator,
    message_diff,
)
from pylint.testutils._primer.primer_command import PrimerCommand

MAX_GITHUB_COMMENT_LENGTH = 65536


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


def _format_suppression_false_positives(
    messages: list[JSONMessage],
    source_link: Callable[[JSONMessage], str],
    action: str,
) -> str:
    """Fuse each ``suppressed-message`` into a single false-positive line.

    A message a user had to disable is a false positive, and its
    ``Suppressed 'x' (from line n)`` bookkeeping carries everything needed:
    the symbol, the user's pragma line and the emission location.
    """
    body = ""
    for count, msg in enumerate(messages, 1):
        symbol = msg["message"].removeprefix("Suppressed ").rsplit(" (from line ", 1)[0]
        body += (
            f"{count}) False positive for {symbol} {action} at\n{source_link(msg)}\n"
        )
    return body


def _details_section(title: str, body: str) -> str:
    # Blank line after <details> required for GitHub markdown rendering.
    return f"{title}\n\n<details>\n\n{body}</details>\n\n"


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
            package = diff.package
            url = self.packages[package].url
            assert not url.endswith(
                ".git"
            ), "You don't need the .git at the end of the github url."
            source_link = self._source_link_for(package, diff.new["commit"])
            comment += f"\n**Effect on [{package}]({url}):**\n\n"
            comment += self._format_changed_messages(diff.changed, source_link)
            comment += self._format_diff_messages(
                diff.new["messages"], diff.missing["messages"], source_link
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

    def _source_link_for(
        self, package: str, commit: str
    ) -> Callable[[JSONMessage], str]:
        clone_dir = self.packages[package].clone_directory
        url = self.packages[package].url

        def _link(msg: JSONMessage) -> str:
            filepath = str(PurePosixPath(msg["path"]).relative_to(clone_dir))
            return f"{url}/blob/{commit}/{filepath}#L{msg['line']}"

        return _link

    def _format_changed_messages(
        self,
        changed: list[ChangedMessage],
        source_link: Callable[[JSONMessage], str],
    ) -> str:
        if not changed:
            return ""
        print("Changed:")
        body = ""
        for count, change in enumerate(changed, 1):
            print(change.new)
            body += (
                f"{count}) [{change.new['symbol']}]({source_link(change.new)}):\n"
                f"{message_diff(change)}\n"
            )
        return _details_section("Changed messages:", body)

    def _format_diff_messages(
        self,
        new_messages: list[JSONMessage],
        missing_messages: list[JSONMessage],
        source_link: Callable[[JSONMessage], str],
    ) -> str:
        """Format new and removed messages, classifying suppression bookkeeping.

        A message a user had to disable is a false positive: a removed
        ``suppressed-message`` means such a false positive is no longer
        emitted, a new one means a false positive is emitted (again) despite
        the user's disable.  The comparator already dropped the
        ``useless-suppression`` echo about the same pragma.
        """
        if new_messages:
            print("Now emitted:")
            for message in new_messages:
                print(message)
        if missing_messages:
            print("No longer emitted:")
            for message in missing_messages:
                print(message)

        astroid_errors = [m for m in new_messages if m["symbol"] == "astroid-error"]
        fixed_fp = [m for m in missing_messages if m["symbol"] == "suppressed-message"]
        reintroduced_fp = [
            m for m in new_messages if m["symbol"] == "suppressed-message"
        ]
        other_new = [
            m
            for m in new_messages
            if m["symbol"] not in {"astroid-error", "suppressed-message"}
        ]
        other_missing = [
            m for m in missing_messages if m["symbol"] != "suppressed-message"
        ]

        out = ""
        if astroid_errors:
            out += (
                f'{len(astroid_errors)} "astroid error(s)" were found. '
                "Please open the GitHub Actions log to see what failed or crashed.\n\n"
            )
        if fixed_fp:
            out += _details_section(
                "🎉 Fixed false positives:",
                _format_suppression_false_positives(fixed_fp, source_link, "removed"),
            )
        if reintroduced_fp:
            out += _details_section(
                "⚠️ Reintroduced false positives:",
                _format_suppression_false_positives(
                    reintroduced_fp, source_link, "(disabled by user) reintroduced"
                ),
            )
        if other_new:
            out += _details_section(
                "New messages:", _format_messages(other_new, source_link)
            )
        if other_missing:
            out += _details_section(
                "Removed messages:", _format_messages(other_missing, source_link)
            )
        return out

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
            # Reserve space for the ellipsis, the suffix and the potential
            # closing tags for a code fence and a <details> block.
            suffix = f"\n{truncation_information}\n\n"
            ellipsis = "\n...\n"
            code_fence = "```\n"
            closing_tag = "</details>\n"
            max_len = (
                MAX_GITHUB_COMMENT_LENGTH
                - len(hash_information)
                - len(suffix)
                - len(ellipsis)
                - len(code_fence)
                - len(closing_tag)
            )
            # Cut at the last line break before the limit so the comment ends
            # with complete lines (links and diff lines contain no space to
            # cut at); fall back to a hard cut inside a very long line.
            cut_point = comment.rfind("\n", 0, max_len)
            if cut_point <= 0:
                cut_point = max_len
            comment = comment[:cut_point] + ellipsis
            # Close any code fence or <details> tag left open by the cut.
            if comment.count("```") % 2:
                comment += code_fence
            if comment.count("<details>") > comment.count("</details>"):
                comment += closing_tag
            comment += suffix
        comment += hash_information
        return comment
