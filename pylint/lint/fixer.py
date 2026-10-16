# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Apply the automatic fixes attached to messages to the source code."""

from __future__ import annotations

import ast
import difflib
import io
import tokenize
from collections import defaultdict
from collections.abc import Collection, Iterable, Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from astroid.inference_tip import clear_inference_tip_cache

from pylint.checkers.clear_lru_cache import clear_lru_caches
from pylint.message import Applicability, Fix, Message
from pylint.message.fix import _byte_to_character_column
from pylint.reporters import CollectingReporter
from pylint.utils import LinterStats

if TYPE_CHECKING:
    from pylint.lint import PyLinter

MAX_FIX_PASSES = 10
"""Fixing a file can create new messages with new fixes, so files are linted
and fixed again until nothing changes, at most this many times.
"""

_UNFIXABLE_FILE_SYMBOLS = frozenset({"syntax-error", "astroid-error", "fatal"})
"""A file with one of these messages is not parsed correctly and is never fixed."""

_Range = tuple[int, int]
_Replacement = tuple[int, int, str]


@dataclass
class FixResult:
    """The outcome of applying fixes to the source code of one file."""

    source: str
    applied: list[Fix] = field(default_factory=list)
    """Fixes that were applied."""

    conflicting: list[Fix] = field(default_factory=list)
    """Fixes overlapping an applied fix, they can be applied on the next pass."""

    not_allowed: list[Fix] = field(default_factory=list)
    """Fixes whose applicability was not requested, like unsafe fixes without
    ``--unsafe-fixes``.
    """

    syntax_error: SyntaxError | None = None
    """The fixes broke the code, so ``source`` is the original code."""


class _SourceIndex:
    """Convert the (line, UTF-8 byte column) positions of edits to string offsets."""

    def __init__(self, source: str) -> None:
        self.lines = source.splitlines(keepends=True)
        self.line_starts = [0]
        for line in self.lines:
            self.line_starts.append(self.line_starts[-1] + len(line))

    def offset(self, line: int, col: int) -> int:
        if line > len(self.lines):
            # The end of a file without a newline at the end
            return self.line_starts[-1]
        return self.line_starts[line - 1] + _byte_to_character_column(
            self.lines[line - 1], col
        )


def _comment_ranges(source: str, index: _SourceIndex) -> list[_Range]:
    ranges = []
    try:
        for token in tokenize.generate_tokens(io.StringIO(source).readline):
            if token.type == tokenize.COMMENT:
                # tokenize gives character columns, not byte columns
                start = index.line_starts[token.start[0] - 1] + token.start[1]
                ranges.append((start, start + len(token.string)))
    except (tokenize.TokenError, SyntaxError):
        pass
    return ranges


def _removes_a_comment(
    replacements: Iterable[_Replacement], comments: list[_Range]
) -> bool:
    return any(
        start < comment_end and comment_start < end
        for start, end, _ in replacements
        for comment_start, comment_end in comments
    )


def _conflict(first: _Range, second: _Range) -> bool:
    # Touching ranges conflict too: two insertions at the same place, or an
    # insertion at the end of a replacement, have no obvious order.
    return first[0] <= second[1] and second[0] <= first[1]


def apply_fixes(
    source: str, fixes: Iterable[Fix], allowed: Collection[Applicability]
) -> FixResult:
    """Apply the non overlapping ``fixes`` whose applicability is ``allowed``.

    Each fix is applied as a whole or not at all. When two fixes overlap, the
    first one in the file wins and the other one is left for the next pass.
    Identical edits from different fixes are only applied once.

    A safe fix that removes or replaces a comment is treated as unsafe.
    """
    result = FixResult(source)
    index = _SourceIndex(source)
    comments: list[_Range] | None = None
    candidates: list[tuple[_Range, Fix, list[_Replacement]]] = []
    for fix in fixes:
        replacements = [
            (
                index.offset(edit.line, edit.col),
                index.offset(edit.end_line, edit.end_col),
                edit.new_text,
            )
            for edit in fix.edits
        ]
        applicability = fix.applicability
        if applicability is Applicability.SAFE:
            if comments is None:
                comments = _comment_ranges(source, index)
            if _removes_a_comment(replacements, comments):
                applicability = Applicability.UNSAFE
        if applicability not in allowed:
            result.not_allowed.append(fix)
            continue
        span = (
            min(start for start, _, _ in replacements),
            max(end for _, end, _ in replacements),
        )
        candidates.append((span, fix, replacements))

    accepted: set[_Replacement] = set()
    for _, fix, replacements in sorted(candidates, key=lambda item: item[0]):
        new_replacements = [r for r in replacements if r not in accepted]
        if any(
            _conflict((start, end), (other_start, other_end))
            for start, end, _ in new_replacements
            for other_start, other_end, _ in accepted
        ):
            result.conflicting.append(fix)
            continue
        accepted.update(new_replacements)
        result.applied.append(fix)

    new_source = source
    for start, end, text in sorted(accepted, reverse=True):
        new_source = new_source[:start] + text + new_source[end:]
    if new_source != source:
        try:
            ast.parse(new_source)
        except SyntaxError as exc:
            result.syntax_error = exc
            return result
    result.source = new_source
    return result


def read_source(path: str) -> tuple[str, str]:
    """Read a Python file, keeping its line endings, and return it with its
    encoding.
    """
    with open(path, "rb") as stream:
        raw = stream.read()
    encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
    return raw.decode(encoding), encoding


def write_source(path: str, source: str, encoding: str) -> None:
    # 'utf-8-sig' writes the byte order mark back
    with open(path, "wb") as stream:
        stream.write(source.encode(encoding))


def unified_diff(path: str, before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=path,
            tofile=path,
        )
    )


def group_fixes_by_file(
    messages: Iterable[Message], unfixable: Collection[str]
) -> dict[str, list[Fix]]:
    """Return the fixes of each file, without the files that cannot be parsed."""
    fixes: defaultdict[str, list[Fix]] = defaultdict(list)
    broken_files = set()
    for message in messages:
        if message.symbol in _UNFIXABLE_FILE_SYMBOLS:
            broken_files.add(message.abspath)
        elif (
            message.fix is not None
            and message.abspath
            and message.symbol not in unfixable
            and message.msg_id not in unfixable
        ):
            fixes[message.abspath].append(message.fix)
    return {
        # The same message can be emitted twice, for example in parallel mode
        path: list(dict.fromkeys(fix))
        for path, fix in fixes.items()
        if path not in broken_files
    }


@dataclass
class FixSummary:
    """What happened to the files during the fix passes."""

    applied: int = 0
    original_sources: dict[str, str] = field(default_factory=dict)
    fixed_sources: dict[str, str] = field(default_factory=dict)
    broken: dict[str, SyntaxError] = field(default_factory=dict)
    """Files where the fixes produced invalid code, they were left unchanged."""

    not_converged: list[str] = field(default_factory=list)
    """Files that still had fixes to apply after the last pass."""


def _reset_linter_state(linter: PyLinter) -> None:
    """Forget the counts of the previous pass."""
    linter.stats = LinterStats()
    linter.msg_status = 0


def _forget_files(paths: Collection[str]) -> None:
    """Make astroid parse the given files again, after they were fixed.

    ``MANAGER.clear_cache()`` would also forget the transforms registered by
    plugins, so only the modules of these files are removed from the cache.
    """
    # pylint: disable-next=import-outside-toplevel
    from pylint.lint.pylinter import MANAGER

    for name, module in list(MANAGER.astroid_cache.items()):
        if module.file in paths:
            del MANAGER.astroid_cache[name]
    clear_inference_tip_cache()
    clear_lru_caches()


class _FileFixer:
    """Apply the fixes of each file and remember the sources seen so far."""

    def __init__(
        self, summary: FixSummary, allowed: Collection[Applicability], write: bool
    ) -> None:
        self.summary = summary
        self.allowed = allowed
        self.write = write
        self.seen_sources: defaultdict[str, set[str]] = defaultdict(set)
        self.encodings: dict[str, str] = {}

    def fix(self, path: str, fixes: list[Fix]) -> bool:
        """Apply the fixes of a file and return whether it changed."""
        if path in self.summary.broken:
            return False
        if path in self.summary.fixed_sources:
            source = self.summary.fixed_sources[path]
        else:
            source, self.encodings[path] = read_source(path)
            self.summary.original_sources[path] = source
        result = apply_fixes(source, fixes, self.allowed)
        if result.syntax_error is not None:
            self.summary.broken[path] = result.syntax_error
            return False
        if result.source == source or result.source in self.seen_sources[path]:
            # Nothing to do, or the fixes keep undoing each other
            return False
        self.seen_sources[path].add(source)
        self.summary.applied += len(result.applied)
        self.summary.fixed_sources[path] = result.source
        if self.write:
            write_source(path, result.source, self.encodings[path])
        return True


def _lint(linter: PyLinter, files_or_modules: Sequence[str]) -> list[Message]:
    """Lint the files without displaying anything, and return the messages."""
    original_reporter = linter.reporter
    collector = CollectingReporter()
    # A StringIO can be pickled in parallel mode, unlike some standard outputs
    collector.out = io.StringIO()
    linter.set_reporter(collector)
    try:
        linter.check(files_or_modules)
    finally:
        linter.set_reporter(original_reporter)
        _reset_linter_state(linter)
    return collector.messages


def fix_files(
    linter: PyLinter,
    files_or_modules: Sequence[str],
    allowed: Collection[Applicability],
    *,
    write: bool = True,
    max_passes: int = MAX_FIX_PASSES,
) -> FixSummary:
    """Lint the files and apply the fixes of the messages until nothing changes.

    When ``write`` is false, a single pass is done and the files are not
    modified, the fixed sources are in the returned summary.
    """
    summary = FixSummary()
    file_fixer = _FileFixer(summary, allowed, write)
    unfixable = set(linter.config.unfixable)
    targets: Sequence[str] = files_or_modules
    for _ in range(max_passes if write else 1):
        fixes_by_file = group_fixes_by_file(_lint(linter, targets), unfixable)
        targets = [
            path for path, fixes in fixes_by_file.items() if file_fixer.fix(path, fixes)
        ]
        _forget_files(targets)
        if not targets:
            return summary
    if write:
        summary.not_converged = list(targets)
    return summary
