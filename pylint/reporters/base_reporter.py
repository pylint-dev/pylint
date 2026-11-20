# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING, TextIO

from pylint.message import Message
from pylint.reporters.ureports.nodes import Text
from pylint.utils import LinterStats

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter
    from pylint.reporters.ureports.nodes import Section


class BaseReporter:
    """Base class for reporters.

    symbols: show short symbolic names for messages.
    """

    extension = ""

    name = "base"
    """Name of the reporter."""

    def __init__(self, output: TextIO | None = None) -> None:
        self.linter: PyLinter
        self.section = 0
        self.out: TextIO = output or sys.stdout
        self.messages: list[Message] = []
        # Build the path prefix to strip to get relative paths
        self.path_strip_prefix = os.getcwd() + os.sep

    def handle_message(self, msg: Message) -> None:
        """Handle a new message triggered on the current file."""
        self.messages.append(msg)

    def writeln(self, string: str = "") -> None:
        """Write a line in the output buffer."""
        encoding = self._output_encoding()
        if encoding:
            # Replace what the output cannot encode (e.g. non-Latin characters
            # when stdout is redirected on Windows with a code page such as
            # cp1252) before writing anything: ``colorama`` writes a line in
            # several chunks, so a retry after a failure would duplicate the
            # chunks already written.
            string = self.reencode_output_after_unicode_error(string, encoding)
        try:
            print(string, file=self.out)
        except UnicodeEncodeError:
            print(
                self.reencode_output_after_unicode_error(string, "ascii"), file=self.out
            )

    def _output_encoding(self) -> str | None:
        """Return the encoding of the output stream, if it has one."""
        # ``colorama.AnsiToWin32`` (see ColorizedTextReporter) has no
        # ``encoding``, but its ``stream`` proxies the one of the wrapped stream.
        return getattr(self.out, "encoding", None) or getattr(
            getattr(self.out, "stream", None), "encoding", None
        )

    @staticmethod
    def reencode_output_after_unicode_error(
        string: str, encoding: str = "utf-8"
    ) -> str:
        """Replace the characters that cannot be encoded with ``encoding``."""
        return string.encode(encoding, errors="replace").decode(
            encoding, errors="replace"
        )

    def display_reports(self, layout: Section) -> None:
        """Display results encapsulated in the layout tree."""
        self.section = 0
        if layout.report_id:
            if isinstance(layout.children[0].children[0], Text):
                layout.children[0].children[0].data += f" ({layout.report_id})"
            else:
                raise ValueError(f"Incorrect child for {layout.children[0].children}")
        self._display(layout)

    def _display(self, layout: Section) -> None:
        """Display the layout."""
        raise NotImplementedError()

    def display_messages(self, layout: Section | None) -> None:
        """Hook for displaying the messages of the reporter.

        This will be called whenever the underlying messages
        needs to be displayed. For some reporters, it probably
        doesn't make sense to display messages as soon as they
        are available, so some mechanism of storing them could be used.
        This method can be implemented to display them after they've
        been aggregated.
        """

    # Event callbacks

    def on_set_current_module(self, module: str, filepath: str | None) -> None:
        """Hook called when a module starts to be analysed."""

    def on_close(
        self,
        stats: LinterStats,
        previous_stats: LinterStats | None,
    ) -> None:
        """Hook called when a module finished analyzing."""
