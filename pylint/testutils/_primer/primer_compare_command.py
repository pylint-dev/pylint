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
from pylint.testutils._primer.primer_comment import (
    MAX_GITHUB_COMMENT_LENGTH,
    truncate_comment,
)


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
            comment += self._format_new_messages(diff.new["messages"], source_link)
            comment += self._format_missing_messages(
                diff.missing["messages"], source_link
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

    def _format_new_messages(
        self,
        messages: list[JSONMessage],
        source_link: Callable[[JSONMessage], str],
    ) -> str:
        if not messages:
            return ""
        print("Now emitted:")
        astroid_errors = 0
        fixed_fp: list[JSONMessage] = []
        other_new: list[JSONMessage] = []
        for message in messages:
            print(message)
            if message["symbol"] == "astroid-error":
                astroid_errors += 1
            elif message["symbol"] == "useless-suppression":
                fixed_fp.append(message)
            else:
                other_new.append(message)

        out = ""
        if astroid_errors:
            out += (
                f'{astroid_errors} "astroid error(s)" were found. '
                "Please open the GitHub Actions log to see what failed or crashed.\n\n"
            )
        if fixed_fp:
            out += _details_section(
                "🎉 Fixed false positives:", _format_messages(fixed_fp, source_link)
            )
        if other_new:
            out += _details_section(
                "New messages:", _format_messages(other_new, source_link)
            )
        return out

    def _format_missing_messages(
        self,
        messages: list[JSONMessage],
        source_link: Callable[[JSONMessage], str],
    ) -> str:
        if not messages:
            return ""
        print("No longer emitted:")
        for message in messages:
            print(message)
        return _details_section(
            "Removed messages:", _format_messages(messages, source_link)
        )

    def _truncate_comment(self, comment: str) -> str:
        """GitHub allows only a set number of characters in a comment."""
        return truncate_comment(comment, self.config.commit, MAX_GITHUB_COMMENT_LENGTH)
