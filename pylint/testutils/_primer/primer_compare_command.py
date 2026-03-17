# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt
from __future__ import annotations

import json
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path, PurePosixPath

from pylint.reporters.json_reporter import OldJsonExport
from pylint.testutils._primer.primer_command import (
    PackageData,
    PackageMessages,
    PrimerCommand,
)

MAX_GITHUB_COMMENT_LENGTH = 65536

# Minimum SequenceMatcher ratio to consider two residual messages "the same
# diagnostic".  The identity fields (symbol, path, obj) already match, so a
# generous threshold is fine here.
_FUZZY_THRESHOLD = 0.5

ChangedMessage = tuple[OldJsonExport, OldJsonExport]  # (old, new)
PackageChanges = dict[str, list[ChangedMessage]]  # {package: [(old, new), ...]}


def _match_key(msg: OldJsonExport) -> tuple[str, str, str]:
    return (msg["symbol"], msg["path"], msg["obj"])


def _fuzzy_pair(
    old_msgs: list[OldJsonExport], new_msgs: list[OldJsonExport]
) -> tuple[list[ChangedMessage], list[OldJsonExport], list[OldJsonExport]]:
    """Pair residual messages by similarity.

    Returns (paired, unmatched_old, unmatched_new).
    """
    if not old_msgs or not new_msgs:
        return [], old_msgs, new_msgs

    paired: list[ChangedMessage] = []
    used_old: set[int] = set()
    used_new: set[int] = set()

    for i, old in enumerate(old_msgs):
        old_str = str(old)
        best_ratio = _FUZZY_THRESHOLD
        best_idx = -1
        for j, new in enumerate(new_msgs):
            if j in used_new:
                continue
            ratio = SequenceMatcher(None, old_str, str(new)).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_idx = j
        if best_idx >= 0:
            paired.append((old, new_msgs[best_idx]))
            used_old.add(i)
            used_new.add(best_idx)

    unmatched_old = [m for i, m in enumerate(old_msgs) if i not in used_old]
    unmatched_new = [m for j, m in enumerate(new_msgs) if j not in used_new]
    return paired, unmatched_old, unmatched_new


_LOCATION_KEYS = {"line", "column", "endLine", "endColumn"}


def _format_span(msg: OldJsonExport) -> str:
    """Format a message's location as ``line:col to endLine:endCol``."""
    start = f"{msg['line']}:{msg['column']}"
    end_line = msg.get("endLine")
    end_col = msg.get("endColumn")
    if end_line is not None and end_col is not None:
        return f"{start} to {end_line}:{end_col}"
    return start


def _message_diff(old: OldJsonExport, new: OldJsonExport) -> str:
    """Return a compact summary of changed fields between two messages.

    Location changes are merged into a single human-readable span.
    String fields (like ``message``) get a ``diff`` code block so GitHub
    renders them with red/green highlighting.
    """
    changed_keys: set[str] = set()
    for key in old:
        if old[key] != new[key]:  # type: ignore[literal-required]
            changed_keys.add(key)

    parts: list[str] = []
    # Location: combine line/column/endLine/endColumn into one sentence.
    if changed_keys & _LOCATION_KEYS:
        parts.append(f"Was raised on {_format_span(old)}, now on {_format_span(new)}.")

    # Other fields (typically ``message``).
    for key in sorted(changed_keys - _LOCATION_KEYS):
        old_val = old[key]  # type: ignore[literal-required]
        new_val = new[key]  # type: ignore[literal-required]
        if isinstance(old_val, str) and isinstance(new_val, str):
            parts.append(f"The {key} changed:\n```diff\n- {old_val}\n+ {new_val}\n```")
        else:
            parts.append(f"{key}: {old_val!r} -> {new_val!r}")
    return "\n".join(parts)


def _fuzzy_match_residuals(
    old_residuals: list[OldJsonExport], new_residuals: list[OldJsonExport]
) -> tuple[list[ChangedMessage], list[OldJsonExport], list[OldJsonExport]]:
    """Fuzzy-match residual messages by identity fields then similarity.

    Returns (paired, unmatched_old, unmatched_new) with original order preserved.
    """
    old_by_key: dict[tuple[str, str, str], list[OldJsonExport]] = defaultdict(list)
    new_by_key: dict[tuple[str, str, str], list[OldJsonExport]] = defaultdict(list)
    for m in old_residuals:
        old_by_key[_match_key(m)].append(m)
    for m in new_residuals:
        new_by_key[_match_key(m)].append(m)

    paired: list[ChangedMessage] = []
    paired_old_ids: set[int] = set()
    paired_new_ids: set[int] = set()
    for key in old_by_key:
        if key not in new_by_key:
            continue
        p, _, _ = _fuzzy_pair(old_by_key[key], new_by_key[key])
        for old, new in p:
            paired.append((old, new))
            paired_old_ids.add(id(old))
            paired_new_ids.add(id(new))

    final_missing = [m for m in old_residuals if id(m) not in paired_old_ids]
    final_new = [m for m in new_residuals if id(m) not in paired_new_ids]
    return paired, final_missing, final_new


class CompareCommand(PrimerCommand):
    def run(self) -> None:
        if self.config.batches is None:
            main_data = self._load_json(self.config.base_file)
            pr_data = self._load_json(self.config.new_file)
        else:
            main_data = {}
            pr_data = {}
            for idx in range(self.config.batches):
                main_data.update(
                    self._load_json(
                        self.config.base_file.replace("BATCHIDX", "batch" + str(idx))
                    )
                )
                pr_data.update(
                    self._load_json(
                        self.config.new_file.replace("BATCHIDX", "batch" + str(idx))
                    )
                )

        missing_messages_data, new_messages_data, changed_messages_data = (
            self._cross_reference(main_data, pr_data)
        )
        comment = self._create_comment(
            missing_messages_data, new_messages_data, changed_messages_data
        )
        with open(self.primer_directory / "comment.txt", "w", encoding="utf-8") as f:
            f.write(comment)

    @staticmethod
    def _cross_reference(
        main_data: PackageMessages, pr_data: PackageMessages
    ) -> tuple[PackageMessages, PackageMessages, PackageChanges]:
        missing_messages_data: PackageMessages = {}
        changed_messages_data: PackageChanges = {}
        for package, data in main_data.items():
            package_missing_messages: list[OldJsonExport] = []
            for message in data["messages"]:
                try:
                    pr_data[package]["messages"].remove(message)
                except ValueError:
                    package_missing_messages.append(message)

            paired, final_missing, final_new = _fuzzy_match_residuals(
                package_missing_messages, pr_data[package]["messages"]
            )

            missing_messages_data[package] = PackageData(
                commit=pr_data[package]["commit"], messages=final_missing
            )
            pr_data[package]["messages"] = final_new
            changed_messages_data[package] = paired
        return missing_messages_data, pr_data, changed_messages_data

    @staticmethod
    def _load_json(file_path: Path | str) -> PackageMessages:
        with open(file_path, encoding="utf-8") as f:
            result: PackageMessages = json.load(f)
        return result

    def _create_comment(
        self,
        all_missing_messages: PackageMessages,
        all_new_messages: PackageMessages,
        all_changed_messages: PackageChanges,
    ) -> str:
        comment = ""
        for package, missing_messages in all_missing_messages.items():
            if len(comment) >= MAX_GITHUB_COMMENT_LENGTH:
                break
            new_messages = all_new_messages[package]
            changed = all_changed_messages.get(package, [])
            if (
                not missing_messages["messages"]
                and not new_messages["messages"]
                and not changed
            ):
                continue
            comment += self._create_comment_for_package(
                package, new_messages, missing_messages, changed
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
        new_messages: PackageData,
        missing_messages: PackageData,
        changed_messages: list[ChangedMessage],
    ) -> str:
        url = self.packages[package].url
        clone_dir = self.packages[package].clone_directory
        commit = new_messages["commit"]

        assert not url.endswith(
            ".git"
        ), "You don't need the .git at the end of the github url."

        def _source_link(msg: OldJsonExport) -> str:
            filepath = str(PurePosixPath(msg["path"]).relative_to(clone_dir))
            return f"{url}/blob/{commit}/{filepath}#L{msg['line']}"

        comment = f"\n\n**Effect on [{package}]({url}):**\n"

        # -- Changed messages (same diagnostic, different details) -----------
        if changed_messages:
            comment += "The following messages have been changed:\n\n<details>\n\n"
            for count, (old, new) in enumerate(changed_messages, 1):
                comment += (
                    f"{count}) {new['symbol']}:\n"
                    f"{_message_diff(old, new)}\n"
                    f"{_source_link(new)}\n"
                )
            comment += "\n</details>\n\n"

        # -- New messages ----------------------------------------------------
        astroid_errors = 0
        new_non_astroid_messages = ""
        count = 0
        for message in new_messages["messages"]:
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
            comment += (
                "The following messages are now emitted:\n\n<details>\n\n"
                + new_non_astroid_messages
                + "\n</details>\n\n"
            )

        # -- Missing messages ------------------------------------------------
        if missing_messages["messages"]:
            comment += "The following messages are no longer emitted:\n\n<details>\n\n"
            for count, message in enumerate(missing_messages["messages"], 1):
                comment += (
                    f"{count}) {message['symbol']}:\n*{message['message']}*\n"
                    f"{_source_link(message)}\n"
                )
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
