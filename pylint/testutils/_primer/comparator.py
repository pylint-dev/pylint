# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Iterator
from difflib import SequenceMatcher
from pathlib import Path
from typing import NamedTuple

from pylint.reporters.json_reporter import JSONMessage
from pylint.testutils._primer.primer_command import PackageData, PackageMessages


class ChangedMessage(NamedTuple):
    """A message that was present on both runs but with altered details."""

    old: JSONMessage
    new: JSONMessage


_LOCATION_KEYS = {"line", "column", "endLine", "endColumn"}


class PackageDiff(NamedTuple):
    """Per-package outcome of comparing a main run against a PR run."""

    package: str
    missing: PackageData  # emitted on main but not on the PR
    new: PackageData  # emitted on the PR but not on main
    changed: list[ChangedMessage]  # same diagnostic, altered line / text


def _match_residuals(
    old_residuals: list[JSONMessage], new_residuals: list[JSONMessage]
) -> tuple[list[ChangedMessage], list[JSONMessage], list[JSONMessage]]:
    """Pair residual messages by ``(symbol, path, obj)``.

    Two messages sharing that key are the "same diagnostic" — if they differ
    only in line numbers or message text, they should be reported as *changed*
    rather than as a separate removal + addition.  Leftovers on each side are
    genuinely missing or genuinely new.

    Returns ``(paired, unmatched_old, unmatched_new)``.
    """
    old_by_key: dict[tuple[str, str, str], list[JSONMessage]] = defaultdict(list)
    new_by_key: dict[tuple[str, str, str], list[JSONMessage]] = defaultdict(list)
    for m in old_residuals:
        old_by_key[m["symbol"], m["path"], m["obj"]].append(m)
    for m in new_residuals:
        new_by_key[m["symbol"], m["path"], m["obj"]].append(m)

    paired: list[ChangedMessage] = []
    paired_old_ids: set[int] = set()
    paired_new_ids: set[int] = set()
    for key in old_by_key:
        if key not in new_by_key:
            continue
        for old, new in zip(old_by_key[key], new_by_key[key]):
            paired.append(ChangedMessage(old=old, new=new))
            paired_old_ids.add(id(old))
            paired_new_ids.add(id(new))

    final_missing = [m for m in old_residuals if id(m) not in paired_old_ids]
    final_new = [m for m in new_residuals if id(m) not in paired_new_ids]
    return paired, final_missing, final_new


def format_span(msg: JSONMessage) -> str:
    """Format a message's location as ``line:col to endLine:endCol``."""
    start = f"{msg['line']}:{msg['column']}"
    end_line = msg.get("endLine")
    end_col = msg.get("endColumn")
    if end_line is not None and end_col is not None:
        return f"`{start}`-`{end_line}:{end_col}`"
    return f"`{start}`"


def message_diff(old: JSONMessage, new: JSONMessage) -> str:
    """Return a compact summary of changed fields between two messages.

    Location changes are merged into a single human-readable span.
    String fields (like ``message``) get a ``diff`` code block so GitHub
    renders them with red/green highlighting.
    """
    changed_keys: set[str] = set()
    for key in set(old) | set(new):
        if old.get(key) != new.get(key):
            changed_keys.add(key)

    parts: list[str] = []
    # Location: combine line/column/endLine/endColumn into one sentence.
    if changed_keys & _LOCATION_KEYS:
        parts.append(f"Moved from {format_span(old)} to {format_span(new)}.")

    # Other fields (typically ``message`` or ``type``).
    for key in sorted(changed_keys - _LOCATION_KEYS):
        old_val = old[key]  # type: ignore[literal-required]
        new_val = new[key]  # type: ignore[literal-required]
        if (
            isinstance(old_val, str)
            and isinstance(new_val, str)
            and (len(old_val) > 40 or len(new_val) > 40)
        ):
            caret_line = _caret_hint(old_val, new_val)
            diff_block = f"```diff\n- {old_val}\n+ {new_val}\n"
            if caret_line:
                diff_block += f"  {caret_line}\n"
            diff_block += "```"
            parts.append(diff_block)
        else:
            parts.append(f"{key}: `{old_val}` → `{new_val}`")
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

    Yields ``PackageDiff`` entries carrying missing, new and changed messages
    for each package that has at least one difference.  *changed* contains
    pairs of ``(old, new)`` messages that are the same diagnostic but with
    altered details (line, message text, etc.).
    """

    def __init__(self, main_data: PackageMessages, pr_data: PackageMessages) -> None:
        self._main_data = main_data
        self._pr_data = pr_data

    @staticmethod
    def from_json(
        base_file: Path | str, new_file: Path | str, batches: int | None = None
    ) -> Comparator:
        """Build a Comparator from JSON file paths, handling batched runs."""
        main_data: PackageMessages
        pr_data: PackageMessages
        if batches is None:
            main_data = Comparator._load_json(base_file)
            pr_data = Comparator._load_json(new_file)
        else:
            main_data = {}
            pr_data = {}
            for idx in range(batches):
                suffix = f"batch{idx}"
                main_data.update(
                    Comparator._load_json(str(base_file).replace("BATCHIDX", suffix))
                )
                pr_data.update(
                    Comparator._load_json(str(new_file).replace("BATCHIDX", suffix))
                )
        return Comparator(main_data, pr_data)

    def __iter__(self) -> Iterator[PackageDiff]:
        main_data = self._main_data
        pr_data = self._pr_data

        for package, data in main_data.items():
            # First pass: exact-match removal.
            pr_messages = list(pr_data[package]["messages"])
            residual_old: list[JSONMessage] = []
            for message in data["messages"]:
                try:
                    pr_messages.remove(message)
                except ValueError:
                    residual_old.append(message)

            # Second pass: pair residuals by position to detect *changed*
            # messages (same diagnostic, different line or text).
            paired, final_missing, final_new = _match_residuals(
                residual_old, pr_messages
            )

            if not final_missing and not final_new and not paired:
                continue
            commit = pr_data[package]["commit"]
            yield PackageDiff(
                package,
                missing=PackageData(commit=commit, messages=final_missing),
                new=PackageData(commit=commit, messages=final_new),
                changed=paired,
            )

    @staticmethod
    def _load_json(file_path: Path | str) -> PackageMessages:
        with open(file_path, encoding="utf-8") as f:
            result: PackageMessages = json.load(f)
        return result
