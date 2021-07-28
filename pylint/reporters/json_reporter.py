# Copyright (c) 2014 Vlad Temian <vladtemian@gmail.com>
# Copyright (c) 2015-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2017 guillaume2 <guillaume.peillex@gmail.col>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Clément Pit-Claudel <cpitclaudel@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""JSON reporter"""
import json

from pylint.interfaces import IReporter
from pylint.reporters.base_reporter import BaseReporter


class JSONReporter(BaseReporter):
    """Report messages and layouts in JSON."""

    __implements__ = IReporter
    name = "json"
    extension = "json"

    def display_messages(self, layout):
        """Launch layouts display"""
        json_dumpable = [
            {
                "type": msg.category,
                "module": msg.module,
                "obj": msg.obj,
                "line": msg.line,
                "column": msg.column,
                "path": msg.path,
                "symbol": msg.symbol,
                "message": msg.msg or "",
                "message-id": msg.msg_id,
            }
            for msg in self.messages
        ]
        print(json.dumps(json_dumpable, indent=4), file=self.out)

    def display_reports(self, layout):
        """Don't do anything in this reporter."""

    def _display(self, layout):
        """Do nothing."""


def register(linter):
    """Register the reporter classes with the linter."""
    linter.register_reporter(JSONReporter)
