# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import os
import sys
from typing import TYPE_CHECKING, List, Optional

from pylint.message import Message
from pylint.reporters.ureports.nodes import Text
from pylint.typing import CheckerStats

if TYPE_CHECKING:
    from pylint.reporters.ureports.nodes import Section


class BaseReporter:
    """base class for reporters

    symbols: show short symbolic names for messages.
    """

    extension = ""

    def __init__(self, output=None):
        self.linter = None
        self.section = 0
        self.out = None
        self.out_encoding = None
        self.set_output(output)
        self.messages: List[Message] = []
        # Build the path prefix to strip to get relative paths
        self.path_strip_prefix = os.getcwd() + os.sep

    def handle_message(self, msg: Message) -> None:
        """Handle a new message triggered on the current file."""
        self.messages.append(msg)

    def set_output(self, output=None):
        """set output stream"""
        self.out = output or sys.stdout

    def writeln(self, string=""):
        """write a line in the output buffer"""
        print(string, file=self.out)

    def display_reports(self, layout: "Section") -> None:
        """display results encapsulated in the layout tree"""
        self.section = 0
        if layout.report_id:
            if isinstance(layout.children[0].children[0], Text):
                layout.children[0].children[0].data += f" ({layout.report_id})"
            else:
                raise ValueError(f"Incorrect child for {layout.children[0].children}")
        self._display(layout)

    def _display(self, layout: "Section") -> None:
        """display the layout"""
        raise NotImplementedError()

    def display_messages(self, layout: Optional["Section"]) -> None:
        """Hook for displaying the messages of the reporter

        This will be called whenever the underlying messages
        needs to be displayed. For some reporters, it probably
        doesn't make sense to display messages as soon as they
        are available, so some mechanism of storing them could be used.
        This method can be implemented to display them after they've
        been aggregated.
        """

    # Event callbacks

    def on_set_current_module(self, module: str, filepath: Optional[str]) -> None:
        """Hook called when a module starts to be analysed."""

    def on_close(
        self,
        stats: CheckerStats,
        previous_stats: CheckerStats,
    ) -> None:
        """Hook called when a module finished analyzing."""
