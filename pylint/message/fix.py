# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Data model for the automatic fixes a checker can attach to a message.

A fix is a list of plain text edits on the original source code. It never
holds astroid nodes, so it can be pickled back from parallel workers.

Line numbers are 1-based and columns use the same unit as astroid's
``col_offset``: a UTF-8 byte offset in the line.
"""

from __future__ import annotations

import enum
import functools
import io
import itertools
import tokenize
from dataclasses import dataclass

from astroid import nodes


class Applicability(enum.Enum):
    """How confident the checker is that applying the fix keeps the code correct."""

    SAFE = "safe"
    """The fix keeps the meaning of the code, it is applied by ``--fix``."""

    UNSAFE = "unsafe"
    """The fix may change the behavior of the code or remove a comment.

    It is applied only with ``--unsafe-fixes``.
    """

    DISPLAY_ONLY = "display-only"
    """The fix is only a suggestion, shown in the JSON output but never applied."""


@dataclass(frozen=True)
class Edit:
    """Replace the text between two positions of a file with ``new_text``.

    An empty ``new_text`` deletes the range, an empty range inserts ``new_text``.
    """

    line: int
    col: int
    end_line: int
    end_col: int
    new_text: str
    filepath: str | None = None
    """The file the positions come from, ``None`` means the file of the message."""

    def __post_init__(self) -> None:
        if (self.line, self.col) > (self.end_line, self.end_col):
            raise ValueError(f"Edit ends before it starts: {self}")

    @property
    def start(self) -> tuple[int, int]:
        return self.line, self.col

    @property
    def end(self) -> tuple[int, int]:
        return self.end_line, self.end_col

    @classmethod
    def replace(cls, node: nodes.NodeNG, new_text: str) -> Edit | None:
        """Replace the source code of ``node``.

        Return ``None`` when the node has no position in a file, for example when
        it was created by an astroid brain.
        """
        if (
            node.lineno is None
            or node.col_offset is None
            or node.end_lineno is None
            or node.end_col_offset is None
        ):
            return None
        return cls(
            node.lineno,
            node.col_offset,
            node.end_lineno,
            node.end_col_offset,
            new_text,
            node.root().file,
        )

    @classmethod
    def delete(cls, node: nodes.NodeNG) -> Edit | None:
        """Remove the source code of ``node``."""
        return cls.replace(node, "")

    @classmethod
    def insert_before(cls, node: nodes.NodeNG, new_text: str) -> Edit | None:
        """Insert ``new_text`` right before the source code of ``node``."""
        if node.lineno is None or node.col_offset is None:
            return None
        return cls(
            node.lineno,
            node.col_offset,
            node.lineno,
            node.col_offset,
            new_text,
            node.root().file,
        )

    @classmethod
    def insert_after(cls, node: nodes.NodeNG, new_text: str) -> Edit | None:
        """Insert ``new_text`` right after the source code of ``node``."""
        if node.end_lineno is None or node.end_col_offset is None:
            return None
        return cls(
            node.end_lineno,
            node.end_col_offset,
            node.end_lineno,
            node.end_col_offset,
            new_text,
            node.root().file,
        )

    @classmethod
    def from_character_columns(
        cls,
        line: int,
        col: int,
        end_line: int,
        end_col: int,
        new_text: str,
        *,
        source_lines: list[str],
    ) -> Edit:
        """Build an edit from character columns, as given by the ``tokenize`` module.

        ``source_lines`` are the lines of the file, used to convert the columns
        to UTF-8 byte offsets.
        """
        return cls(
            line,
            _character_to_byte_column(source_lines, line, col),
            end_line,
            _character_to_byte_column(source_lines, end_line, end_col),
            new_text,
        )


@dataclass(frozen=True)
class Fix:
    """A change that makes a message go away, applied as a whole or not at all."""

    description: str
    """A short sentence telling what the fix does, like "Remove the unused import"."""

    edits: tuple[Edit, ...]
    applicability: Applicability = Applicability.UNSAFE

    def __post_init__(self) -> None:
        if not self.edits:
            raise ValueError("A fix needs at least one edit")
        ordered = sorted(self.edits, key=lambda edit: (edit.start, edit.end))
        for previous, current in itertools.pairwise(ordered):
            if current.start < previous.end:
                raise ValueError(f"Edits of a fix overlap: {previous}, {current}")

    @classmethod
    def create(
        cls,
        description: str,
        *edits: Edit | None,
        applicability: Applicability = Applicability.UNSAFE,
    ) -> Fix | None:
        """Build a fix, or return ``None`` if one of the edits could not be built.

        This lets a checker pass the result of ``Edit.replace`` and friends
        without checking each of them.
        """
        valid_edits = tuple(edit for edit in edits if edit is not None)
        if not valid_edits or len(valid_edits) != len(edits):
            return None
        return cls(description, valid_edits, applicability)


def _character_to_byte_column(source_lines: list[str], line: int, col: int) -> int:
    if line > len(source_lines):
        return col
    return len(source_lines[line - 1][:col].encode("utf-8"))


def _byte_to_character_column(text: str, col: int) -> int:
    return len(text.encode("utf-8")[:col].decode("utf-8", errors="ignore"))


@functools.lru_cache(maxsize=8)
def _module_source_lines(module: nodes.Module) -> list[str]:
    with module.stream() as stream:
        raw: bytes = stream.read()
    return raw.decode(module.file_encoding or "utf-8").splitlines(keepends=True)


def source_segment(node: nodes.NodeNG) -> str | None:
    """Return the original source code of ``node``, like ``ast.get_source_segment``.

    Unlike ``node.as_string()``, the text keeps the parentheses, quotes, spacing and
    comments written by the user. Use it to build the new text of a fix.

    Return ``None`` when the node has no position in a file.
    """
    if (
        node.lineno is None
        or node.col_offset is None
        or node.end_lineno is None
        or node.end_col_offset is None
    ):
        return None
    module = node.root()
    if not isinstance(module, nodes.Module):
        return None
    try:
        lines: list[str] = _module_source_lines(module)
    except (OSError, UnicodeDecodeError, LookupError):
        return None
    if node.end_lineno > len(lines):
        return None
    first: int = node.lineno - 1
    last: int = node.end_lineno - 1
    start = _byte_to_character_column(lines[first], node.col_offset)
    end = _byte_to_character_column(lines[last], node.end_col_offset)
    if first == last:
        return lines[first][start:end]
    return "".join([lines[first][start:], *lines[first + 1 : last], lines[last][:end]])


def source_tokens(node: nodes.NodeNG) -> list[tokenize.TokenInfo] | None:
    """Return the tokens of the original source code of ``node``.

    The positions of the tokens use the same unit as an ``Edit``: lines of the
    file and UTF-8 byte columns, so ``Edit(*token.start, *token.end, "")``
    removes a token. Comments are included, the final ``NEWLINE`` and
    ``ENDMARKER`` tokens are not.

    Return ``None`` when the node has no position in a file.
    """
    segment = source_segment(node)
    if segment is None:
        return None
    lines = _module_source_lines(node.root())
    first_line = lines[node.lineno - 1]
    first_column = _byte_to_character_column(first_line, node.col_offset)

    def position(line: int, col: int) -> tuple[int, int]:
        if line == 1:
            col += first_column
        line += node.lineno - 1
        return line, _character_to_byte_column(lines, line, col)

    tokens = []
    try:
        for token in tokenize.generate_tokens(io.StringIO(segment).readline):
            if (
                token.type in {tokenize.NEWLINE, tokenize.ENDMARKER}
                and not token.string
            ):
                continue
            tokens.append(
                token._replace(start=position(*token.start), end=position(*token.end))
            )
    except (tokenize.TokenError, SyntaxError):
        return None
    return tokens
