# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Check source code is ascii only or has an encoding declaration (PEP 263)."""

from __future__ import annotations

import re
import tokenize
from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseRawFileChecker, BaseTokenChecker
from pylint.typing import ManagedMessage

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class ByIdManagedMessagesChecker(BaseRawFileChecker):
    """Checks for messages that are enabled or disabled by id instead of symbol."""

    name = "miscellaneous"
    msgs = {
        "I0023": (
            "%s",
            "use-symbolic-message-instead",
            "Used when a message is enabled or disabled by id.",
            {"default_enabled": False},
        )
    }
    options = ()

    def _clear_by_id_managed_msgs(self) -> None:
        self.linter._by_id_managed_msgs.clear()

    def _get_by_id_managed_msgs(self) -> list[ManagedMessage]:
        return self.linter._by_id_managed_msgs

    def process_module(self, node: nodes.Module) -> None:
        """Inspect the source file to find messages activated or deactivated by id."""
        managed_msgs = self._get_by_id_managed_msgs()
        for mod_name, msgid, symbol, lineno, is_disabled in managed_msgs:
            if mod_name == node.name:
                verb = "disable" if is_disabled else "enable"
                txt = f"'{msgid}' is cryptic: use '# pylint: {verb}={symbol}' instead"
                self.add_message("use-symbolic-message-instead", line=lineno, args=txt)
        self._clear_by_id_managed_msgs()


class EncodingChecker(BaseTokenChecker, BaseRawFileChecker):
    """BaseChecker for encoding issues.

    Checks for:
    * warning notes in the code like FIXME, XXX
    * encoding issues.
    """

    # configuration section name
    name = "miscellaneous"
    msgs = {
        "W0511": (
            "%s",
            "fixme",
            "Used when a warning note as FIXME or XXX is detected.",
        )
    }

    options = (
        (
            "notes",
            {
                "type": "csv",
                "metavar": "<comma separated values>",
                "default": ("FIXME", "XXX", "TODO"),
                "help": (
                    "List of note tags to take in consideration, "
                    "separated by a comma."
                ),
            },
        ),
        (
            "notes-rgx",
            {
                "type": "string",
                "metavar": "<regexp>",
                "help": "Regular expression of note tags to take in consideration.",
                "default": "",
            },
        ),
        (
            "check-fixme-in-docstring",
            {
                "type": "yn",
                "metavar": "<y or n>",
                "default": False,
                "help": "Whether or not to search for fixme's in docstrings."
            }
        )
    )

    def open(self) -> None:
        super().open()

        notes = "|".join(re.escape(note) for note in self.linter.config.notes)
        if self.linter.config.notes_rgx:
            comment_regex = rf"#\s*({notes}|{self.linter.config.notes_rgx})(?=(:|\s|\Z))"
            self._comment_fixme_pattern = re.compile(comment_regex, re.I)
            if self.linter.config.check_fixme_in_docstring:
                docstring_regex = rf"\"\"\"\s*({notes}|{self.linter.config.notes_rgx})(?=(:|\s|\Z))"
                self._docstring_fixme_pattern = re.compile(docstring_regex, re.I)
        else:
            comment_regex = rf"#\s*({notes})(?=(:|\s|\Z))"
            self._comment_fixme_pattern = re.compile(comment_regex, re.I)
            if self.linter.config.check_fixme_in_docstring:
                docstring_regex = rf"\"\"\"\s*({notes})(?=(:|\s|\Z))"
                self._docstring_fixme_pattern = re.compile(docstring_regex, re.I)

    def _check_encoding(
        self, lineno: int, line: bytes, file_encoding: str
    ) -> str | None:
        try:
            return line.decode(file_encoding)
        except UnicodeDecodeError:
            pass
        except LookupError:
            if (
                line.startswith(b"#")
                and "coding" in str(line)
                and file_encoding in str(line)
            ):
                msg = f"Cannot decode using encoding '{file_encoding}', bad encoding"
                self.add_message("syntax-error", line=lineno, args=msg)
        return None

    def process_module(self, node: nodes.Module) -> None:
        """Inspect the source file to find encoding problem."""
        encoding = node.file_encoding if node.file_encoding else "ascii"

        with node.stream() as stream:
            for lineno, line in enumerate(stream):
                self._check_encoding(lineno + 1, line, encoding)

    def process_tokens(self, tokens: list[tokenize.TokenInfo]) -> None:
        """Inspect the source to find fixme problems."""
        if not self.linter.config.notes:
            return
        for token_info in tokens:
            if token_info.type == tokenize.COMMENT:
                comment_text = token_info.string[1:].lstrip()  # trim '#' and white-spaces
                if self._comment_fixme_pattern.search("#" + comment_text.lower()):
                    self.add_message(
                        "fixme",
                        col_offset=token_info.start[1] + 1,
                        args=comment_text,
                        line=token_info.start[0],
                    )
            elif self.linter.config.check_fixme_in_docstring and self._is_docstring_comment(token_info):
                docstring_lines = token_info.string.split("\n")
                for line_no, line in enumerate(docstring_lines):
                    if line.startswith('"""'):
                        line = line[3:]
                    line = line.lstrip()
                    if line.endswith('"""'):
                        line = line[:-3]
                    if self._docstring_fixme_pattern.search('"""' + line.lower()):
                        self.add_message(
                            "fixme",
                            col_offset=token_info.start[1] + 1,
                            args=line,
                            line=token_info.start[0] + line_no,
                        )

    def _is_docstring_comment(self, token_info: tokenize.TokenInfo) -> bool:
        return token_info.type == tokenize.STRING and token_info.line.lstrip().startswith('"""')


def register(linter: PyLinter) -> None:
    linter.register_checker(EncodingChecker(linter))
    linter.register_checker(ByIdManagedMessagesChecker(linter))
