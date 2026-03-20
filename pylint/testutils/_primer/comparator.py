# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Iterator
from difflib import SequenceMatcher
from pathlib import Path

from pylint.reporters.json_reporter import OldJsonExport
from pylint.testutils._primer.primer_command import PackageMessages

ChangedMessage = tuple[OldJsonExport, OldJsonExport]  # (old, new)

_LOCATION_KEYS = {"line", "column", "endLine", "endColumn"}


def _position_key(msg: OldJsonExport) -> tuple[str, str, str]:
    """Key that identifies a diagnostic independently of its text or location.

    Two messages that share (symbol, path, obj) are the "same diagnostic" — if
    they differ only in line numbers or message text, they should be reported as
    *changed* rather than as a separate removal + addition.
    """
    return (msg["symbol"], msg["path"], msg["obj"])


def _match_residuals(
    old_residuals: list[OldJsonExport], new_residuals: list[OldJsonExport]
) -> tuple[list[ChangedMessage], list[OldJsonExport], list[OldJsonExport]]:
    """Pair residual messages by position key ``(symbol, path, obj)``.

    Messages that share the same key are paired 1:1 in order.  Any left-over
    messages remain as genuinely missing or genuinely new.

    Returns ``(paired, unmatched_old, unmatched_new)``.
    """
    old_by_key: dict[tuple[str, str, str], list[OldJsonExport]] = defaultdict(list)
    new_by_key: dict[tuple[str, str, str], list[OldJsonExport]] = defaultdict(list)
    for m in old_residuals:
        old_by_key[_position_key(m)].append(m)
    for m in new_residuals:
        new_by_key[_position_key(m)].append(m)

    paired: list[ChangedMessage] = []
    paired_old_ids: set[int] = set()
    paired_new_ids: set[int] = set()
    for key in old_by_key:
        if key not in new_by_key:
            continue
        for old, new in zip(old_by_key[key], new_by_key[key]):
            paired.append((old, new))
            paired_old_ids.add(id(old))
            paired_new_ids.add(id(new))

    final_missing = [m for m in old_residuals if id(m) not in paired_old_ids]
    final_new = [m for m in new_residuals if id(m) not in paired_new_ids]
    return paired, final_missing, final_new


def format_span(msg: OldJsonExport) -> str:
    """Format a message's location as ``line:col to endLine:endCol``."""
    start = f"{msg['line']}:{msg['column']}"
    end_line = msg.get("endLine")
    end_col = msg.get("endColumn")
    if end_line is not None and end_col is not None:
        return f"from `{start}` to `{end_line}:{end_col}`"
    return f"at `{start}`"


def message_diff(old: OldJsonExport, new: OldJsonExport) -> str:
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
        parts.append(f"Was raised {format_span(old)}, now {format_span(new)}.")

    # Other fields (typically ``message``).
    for key in sorted(changed_keys - _LOCATION_KEYS):
        old_val = old[key]  # type: ignore[literal-required]
        new_val = new[key]  # type: ignore[literal-required]
        if isinstance(old_val, str) and isinstance(new_val, str):
            caret_line = _caret_hint(old_val, new_val)
            diff_block = f"```diff\n- {old_val}\n+ {new_val}\n"
            if caret_line:
                diff_block += f"  {caret_line}\n"
            diff_block += "```"
            parts.append(diff_block)
        else:
            parts.append(f"{key}: {old_val!r} -> {new_val!r}")
    return "\n\n".join(parts)


def _caret_hint(old: str, new: str) -> str:
    """Build a ``^`` marker line highlighting changed spans in *new*.

    Uses SequenceMatcher to find which parts of *new* differ from *old*
    and places ``^`` characters under them (aligned with the ``+ `` prefix).
    Returns an empty string when the whole line changed (carets wouldn't help).
    """
    matcher = SequenceMatcher(None, old, new)
    carets = [" "] * len(new)
    changed_count = 0
    for tag, _i1, _i2, j1, j2 in matcher.get_opcodes():
        if tag != "equal":
            for j in range(j1, j2):
                carets[j] = "^"
            changed_count += j2 - j1
    # If most of the string changed, carets are just noise.
    if changed_count > len(new) * 0.6:
        return ""
    return "".join(carets).rstrip()


class Comparator:
    """Cross-reference two primer JSON outputs and iterate over differences.

    Yields ``(package, missing, new, changed)`` for each package that has at
    least one difference.  *changed* contains pairs of ``(old, new)`` messages
    that are the same diagnostic but with altered details (line, message text,
    etc.).
    """

    def __init__(self, main_data: PackageMessages, pr_data: PackageMessages) -> None:
        self.missing_messages: dict[str, list[OldJsonExport]] = {}
        self.new_messages: dict[str, list[OldJsonExport]] = {}
        self.changed_messages: dict[str, list[ChangedMessage]] = {}
        self.commits: dict[str, str] = {}

        for package, data in main_data.items():
            self.commits[package] = pr_data[package]["commit"]
            # First pass: exact-match removal.
            residual_old: list[OldJsonExport] = []
            for message in data["messages"]:
                try:
                    pr_data[package]["messages"].remove(message)
                except ValueError:
                    residual_old.append(message)

            # Second pass: pair residuals by position to detect *changed*
            # messages (same diagnostic, different line or text).
            paired, final_missing, final_new = _match_residuals(
                residual_old, pr_data[package]["messages"]
            )

            self.missing_messages[package] = final_missing
            self.new_messages[package] = final_new
            self.changed_messages[package] = paired

    def __iter__(
        self,
    ) -> Iterator[
        tuple[
            str,
            list[OldJsonExport],
            list[OldJsonExport],
            list[ChangedMessage],
        ]
    ]:
        for package, missing in self.missing_messages.items():
            new = self.new_messages[package]
            changed = self.changed_messages[package]
            if not missing and not new and not changed:
                continue
            yield package, missing, new, changed

    @staticmethod
    def from_json(
        base_file: str, new_file: str, batches: int | None = None
    ) -> Comparator:
        """Build a Comparator from JSON file paths, handling batched runs."""
        main_data: PackageMessages
        pr_data: PackageMessages
        if batches is None:
            main_data = _load_json(base_file)
            pr_data = _load_json(new_file)
        else:
            main_data = {}
            pr_data = {}
            for idx in range(batches):
                main_data.update(
                    _load_json(base_file.replace("BATCHIDX", "batch" + str(idx)))
                )
                pr_data.update(
                    _load_json(new_file.replace("BATCHIDX", "batch" + str(idx)))
                )
        return Comparator(main_data, pr_data)


def _load_json(file_path: Path | str) -> PackageMessages:
    with open(file_path, encoding="utf-8") as f:
        result: PackageMessages = json.load(f)
    return result
