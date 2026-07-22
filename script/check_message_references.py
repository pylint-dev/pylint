# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Add ``:ref:`` roles around pylint message symbols in the documentation.

Used by pre-commit on the documentation and the changelog fragments: a bare
message symbol (like ``no-member``) becomes ``:ref:`no-member``` so that it
links to the message's documentation page. Current and renamed messages come
from pylint's message store, permanently deleted messages come from
``DELETED_MESSAGES_IDS``; all of them have a documentation page with a
matching anchor.
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Sequence
from pathlib import Path

from pylint.checkers import initialize as initialize_checkers
from pylint.extensions import initialize as initialize_extensions
from pylint.lint import PyLinter
from pylint.message._deleted_message_ids import DELETED_MESSAGES_IDS

# Words that look like message symbols: lowercase words joined by dashes
# (a few old symbols like 'raw_input-builtin' also contain underscores).
CANDIDATE_PATTERN = re.compile(r"[a-z0-9_]+(?:-[a-z0-9_]+)+")

# Inline markup spans in which a symbol must be left alone: inline literals,
# roles (including existing ``:ref:``), link labels and emphasis (rst does
# not render nested inline markup).
INLINE_SPAN_PATTERN = re.compile(
    r"``[^`]+``|`[^`]+`|\*\*[^\s*][^*]*\*\*|\*[^\s*][^*]*\*"
)

DIRECTIVE_PATTERN = re.compile(r"\.\. ([a-zA-Z-]+)::")

# Directives whose content is regular text where references render fine.
# The content of every other directive (code blocks, tables, toctrees,
# comments, ...) is left untouched.
TEXT_DIRECTIVES = frozenset(
    {
        "admonition",
        "attention",
        "caution",
        "danger",
        "deprecated",
        "error",
        "hint",
        "important",
        "note",
        "seealso",
        "tip",
        "topic",
        "versionadded",
        "versionchanged",
        "warning",
    }
)

# Characters that disqualify a candidate when directly before/after it
# (member of an option like '--disable=no-member', a path, a filename,
# an 'msgid:symbol' pair, ...).
BEFORE_GUARDS = frozenset("`-/\\._:=")
AFTER_GUARDS = frozenset("`/\\_")


def _get_all_symbols() -> frozenset[str]:
    """All symbols with a documentation page: current, renamed and deleted."""
    linter = PyLinter()
    initialize_checkers(linter)
    initialize_extensions(linter)
    symbols: set[str] = set()
    for message in linter.msgs_store.messages:
        symbols.add(message.symbol)
        symbols.update(old_symbol for _, old_symbol in message.old_names)
    for deleted_messages in DELETED_MESSAGES_IDS.values():
        for deleted_message in deleted_messages:
            symbols.add(deleted_message.symbol)
            symbols.update(old_symbol for _, old_symbol in deleted_message.old_names)
    return frozenset(symbols)


def _indentation(line: str) -> int:
    return len(line) - len(line.lstrip())


def _add_references_to_line(line: str, symbols: frozenset[str]) -> str:
    if line.count("`") % 2:
        # Unbalanced backticks: part of a multi-line inline span (a link or
        # a literal continued on the next line), don't touch anything
        return line
    masked_spans = [match.span() for match in INLINE_SPAN_PATTERN.finditer(line)]
    result: list[str] = []
    last_end = 0
    for match in CANDIDATE_PATTERN.finditer(line):
        word = match.group()
        start, end = match.span()
        if word not in symbols:
            continue
        if any(span_start <= start < span_end for span_start, span_end in masked_spans):
            continue
        before = line[start - 1] if start else ""
        after = line[end] if end < len(line) else ""
        if before in BEFORE_GUARDS or after in AFTER_GUARDS:
            continue
        if after == "." and end + 1 < len(line) and line[end + 1].isalnum():
            # A filename like 'bad-name.py', not the end of a sentence
            continue
        result.append(line[last_end:start])
        result.append(f":ref:`{word}`")
        last_end = end
    result.append(line[last_end:])
    return "".join(result)


def add_references(content: str, symbols: frozenset[str]) -> str:
    """Add ``:ref:`` roles to an rst document, leaving literal content alone."""
    new_lines: list[str] = []
    # While set, lines indented more than this are part of a literal block,
    # a non-text directive or a comment, and are left untouched.
    skipped_block_indentation: int | None = None
    for line in content.splitlines(keepends=True):
        stripped = line.strip()
        if skipped_block_indentation is not None:
            if not stripped or _indentation(line) > skipped_block_indentation:
                new_lines.append(line)
                continue
            skipped_block_indentation = None
        if stripped.startswith("..") and (stripped == ".." or stripped[2] in " _|["):
            # Directive, comment, anchor, substitution or citation
            directive_match = DIRECTIVE_PATTERN.match(stripped)
            if (
                directive_match is None
                or directive_match.group(1) not in TEXT_DIRECTIVES
            ):
                skipped_block_indentation = _indentation(line)
            new_lines.append(line)
            continue
        if stripped.startswith(">>>"):
            # Doctest blocks
            new_lines.append(line)
            continue
        new_lines.append(_add_references_to_line(line, symbols))
        if stripped.endswith("::"):
            # The paragraph introduces a literal block
            skipped_block_indentation = _indentation(line)
    return "".join(new_lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filenames", nargs="+", type=Path)
    parser.add_argument(
        "--check", action="store_true", help="Only report issues, do not modify files"
    )
    args = parser.parse_args(argv)
    symbols = _get_all_symbols()
    return_value = 0
    for filename in args.filenames:
        content = filename.read_text(encoding="utf-8")
        new_content = add_references(content, symbols)
        if new_content == content:
            continue
        return_value = 1
        if args.check:
            print(f"{filename}: bare message symbols should use ':ref:'")
        else:
            filename.write_text(new_content, encoding="utf-8")
            print(f"{filename}: added ':ref:' around message symbols")
    return return_value


if __name__ == "__main__":
    raise SystemExit(main())
