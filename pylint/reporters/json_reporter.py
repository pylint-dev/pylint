# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

"""JSON reporter."""
import json
from typing import TYPE_CHECKING, Optional

from pylint.interfaces import IReporter
from pylint.reporters.base_reporter import BaseReporter

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter
    from pylint.reporters.ureports.nodes import Section


class JSONReporter(BaseReporter):
    """Report messages and layouts in JSON."""

    __implements__ = IReporter
    name = "json"
    extension = "json"

    def display_messages(self, layout: Optional["Section"]) -> None:
        """Launch layouts display."""
        json_dumpable = [
            {
                "type": msg.category,
                "module": msg.module,
                "obj": msg.obj,
                "line": msg.line,
                "column": msg.column,
                "endLine": msg.end_line,
                "endColumn": msg.end_column,
                "path": msg.path,
                "symbol": msg.symbol,
                "message": msg.msg or "",
                "message-id": msg.msg_id,
            }
            for msg in self.messages
        ]
        print(json.dumps(json_dumpable, indent=4), file=self.out)

    def display_reports(self, layout: "Section") -> None:
        """Don't do anything in this reporter."""

    def _display(self, layout: "Section") -> None:
        """Do nothing."""


def register(linter: "PyLinter") -> None:
    linter.register_reporter(JSONReporter)
