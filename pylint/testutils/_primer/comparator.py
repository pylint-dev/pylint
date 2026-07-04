# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Callable, Hashable, Iterator
from difflib import SequenceMatcher
from operator import itemgetter
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
    changed: list[ChangedMessage]  # same message, altered line / text


SYMBOL_RENAME_SIMILARITY_THRESHOLD = 0.6


def _pair_by_key(
    old_residuals: list[JSONMessage],
    new_residuals: list[JSONMessage],
    key: Callable[[JSONMessage], tuple[Hashable, ...]],
    accept: Callable[[JSONMessage, JSONMessage], bool] = lambda _o, _n: True,
) -> tuple[list[ChangedMessage], list[JSONMessage], list[JSONMessage]]:
    """Pair messages whose ``key`` matches, preferring the closest line.

    Two messages sharing the key are the "same warning" — if they differ only
    in line numbers or message text, they should be reported as *changed*
    rather than as a separate removal + addition.  Leftovers on each side are
    passed through to the next pass (or reported as missing/new).

    ``accept`` is an optional predicate that can veto a candidate pair (used to
    avoid pairing two unrelated messages that happen to share the key).  Among
    the accepted candidates, the one nearest to the old message's line wins, so
    two warnings that both moved pair with their own counterpart instead of
    crossing (10→21 and 20→11 when 10→11 and 20→21 was meant).
    """
    new_by_key: dict[tuple[Hashable, ...], list[JSONMessage]] = defaultdict(list)
    for m in new_residuals:
        new_by_key[key(m)].append(m)

    paired: list[ChangedMessage] = []
    final_missing: list[JSONMessage] = []
    matched_new: set[int] = set()
    for old in old_residuals:
        bucket = new_by_key.get(key(old), [])
        candidates = [
            (abs(m["line"] - old["line"]), i, m)
            for i, m in enumerate(bucket)
            if accept(old, m)
        ]
        if candidates:
            _distance, index, new = min(candidates, key=itemgetter(0, 1))
            bucket.pop(index)
            paired.append(ChangedMessage(old=old, new=new))
            matched_new.add(id(new))
        else:
            final_missing.append(old)
    final_new = [m for m in new_residuals if id(m) not in matched_new]
    return paired, final_missing, final_new


def _is_symbol_rename(old: JSONMessage, new: JSONMessage) -> bool:
    """True when the two symbols are textually similar enough to be a rename.

    Used to avoid pairing unrelated messages that happen to share a source
    position (e.g. ``useless-suppression`` removed and ``locally-disabled``
    added on the same line — those are conceptually opposite, not a rename).
    """
    ratio = SequenceMatcher(None, old["symbol"], new["symbol"]).ratio()
    return ratio >= SYMBOL_RENAME_SIMILARITY_THRESHOLD


def _pair_residuals(
    old_residuals: list[JSONMessage], new_residuals: list[JSONMessage]
) -> tuple[list[ChangedMessage], list[JSONMessage], list[JSONMessage]]:
    """Pair residual messages with two passes of decreasing strictness.

    First by ``(symbol, path, obj)`` — catches line-only or message-only changes
    for the same warning. Then by exact source location, gated on symbol
    similarity — catches symbol renames such as ``used-before-assignment`` →
    ``possibly-used-before-assignment``, where the same code position now
    emits a renamed message.

    ``astroid-error`` messages embed a unique crash-report path, so a file
    crashing on both runs would pair as a meaningless traceback "diff".  They
    are kept out of pairing so they stay counted in the prominent astroid
    error warning instead.
    """
    old_errors = [m for m in old_residuals if m["symbol"] == "astroid-error"]
    new_errors = [m for m in new_residuals if m["symbol"] == "astroid-error"]
    old_residuals = [m for m in old_residuals if m["symbol"] != "astroid-error"]
    new_residuals = [m for m in new_residuals if m["symbol"] != "astroid-error"]

    paired_by_symbol, missing, new = _pair_by_key(
        old_residuals,
        new_residuals,
        key=lambda m: (m["symbol"], m["path"], m["obj"]),
    )
    paired_by_location, missing, new = _pair_by_key(
        missing,
        new,
        key=lambda m: (
            m["path"],
            m["line"],
            m["column"],
            m.get("endLine"),
            m.get("endColumn"),
        ),
        accept=_is_symbol_rename,
    )
    return paired_by_symbol + paired_by_location, missing + old_errors, new + new_errors


def format_span(msg: JSONMessage) -> str:
    """Format a message's location as ``line:col to endLine:endCol``."""
    start = f"{msg['line']}:{msg['column']}"
    end_line = msg.get("endLine")
    end_col = msg.get("endColumn")
    if end_line is not None and end_col is not None:
        return f"`{start}`-`{end_line}:{end_col}`"
    return f"`{start}`"


def message_diff(change: ChangedMessage) -> str:
    """Return a compact summary of changed fields between two messages.

    Location changes are merged into a single human-readable span.
    String fields (like ``message``) get a ``diff`` code block so GitHub
    renders them with red/green highlighting.
    """
    old, new = change.old, change.new
    changed_keys: set[str] = set()
    for key in old.keys() | new.keys():
        if old.get(key) != new.get(key):
            changed_keys.add(key)

    parts: list[str] = []
    # Location: combine line/column/endLine/endColumn into one sentence.
    if changed_keys & _LOCATION_KEYS:
        parts.append(f"Moved from {format_span(old)} to {format_span(new)}.")

    # Other fields (typically ``message`` or ``type``). ``get`` guards against
    # a field existing on only one side (e.g. the PR changed the JSON schema).
    for key in sorted(changed_keys - _LOCATION_KEYS):
        old_val = old.get(key)
        new_val = new.get(key)
        if (
            isinstance(old_val, str)
            and isinstance(new_val, str)
            and (any(len(v) > 40 or "\n" in v for v in (old_val, new_val)))
        ):
            parts.append(_diff_block(old_val, new_val))
        else:
            parts.append(f"{key}: `{old_val}` → `{new_val}`")
    return "\n\n".join(parts)


def _diff_block(old: str, new: str) -> str:
    """Render a ``diff`` code block comparing two values line by line.

    Unchanged lines of multi-line values (e.g. ``duplicate-code``) are kept
    as context, so only the lines that actually changed stand out.  When a
    changed block keeps its line count, each new line gets a ``^`` caret
    hint under the characters that differ from its old counterpart.
    """
    old_lines, new_lines = old.splitlines(), new.splitlines()
    matcher = SequenceMatcher(None, old_lines, new_lines)
    lines: list[str] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            lines.extend(f"  {line}" for line in old_lines[i1:i2])
            continue
        lines.extend(f"- {line}" for line in old_lines[i1:i2])
        for offset, line in enumerate(new_lines[j1:j2]):
            lines.append(f"+ {line}")
            if tag == "replace" and i2 - i1 == j2 - j1:
                caret_line = _caret_hint(old_lines[i1 + offset], line)
                if caret_line:
                    lines.append(f"  {caret_line}")
    return "```diff\n" + "\n".join(lines) + "\n```"


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
    """Cross-reference two primer JSON outputs and iterate over differences."""

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

            # Second pass: pair residuals by symbol then by location to
            # detect *changed* messages (same warning, different line/text,
            # or a symbol rename at the same source position).
            paired, final_missing, final_new = _pair_residuals(
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
