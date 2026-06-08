# pylint: disable=redefined-outer-name
"""Base reporter classes for pylint."""

import sys
from typing import IO, Optional, TextIO

from pylint.message import Message
from pylint.reporters.ureports.text import TextReporter


class BaseReporter:
    """Base class for reporters."""

    def __init__(self, output: Optional[TextIO] = None):
        self.output = output or sys.stdout
        self.messages: list[Message] = []
        self.path_stones: list[str] = []

    def handle_message(self, msg: Message) -> None:
        """Handle a message."""
        self.messages.append(msg)

    def writeln(self, text: str = "") -> None:
        """Write a line to the output."""
        self.output.write(text + "\n")

    def display_messages(self) -> None:
        """Display all messages."""
        for msg in self.messages:
            self.writeln(str(msg))

    def on_set_current_module(self, module: str, filepath: str) -> None:
        """Called when a module is set as current."""

    def on_close(self, stats, previous_stats) -> None:
        """Called when the analysis is finished."""

    def display_results(self, layout) -> None:
        """Display the results."""

    def _display_fail_under(self, score: float, fail_under: float) -> None:
        """Display a message when score is below fail-under threshold."""
        if score < fail_under:
            self.writeln(
                f"Your code has been rated at {score:.2f}/10 "
                f"(previous run: {fail_under:.2f}/10, fail-under: {fail_under:.2f})"
            )