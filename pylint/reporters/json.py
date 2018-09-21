# Copyright (c) 2014 Vlad Temian <vladtemian@gmail.com>
# Copyright (c) 2015-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2017 guillaume2 <guillaume.peillex@gmail.col>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""JSON reporter"""
from __future__ import absolute_import, print_function

import cgi
import json
import sys

from pylint.interfaces import IReporter
from pylint.reporters import BaseReporter


class JSONReporter(BaseReporter):
    """Report messages and layouts in JSON."""

    __implements__ = IReporter
    name = "json"
    extension = "json"

    def __init__(self, output=sys.stdout):
        BaseReporter.__init__(self, output)
        self.messages = []

    def handle_message(self, msg):
        """Manage message of different type and in the context of path."""
        self.messages.append(
            {
                "type": msg.category,
                "module": msg.module,
                "obj": msg.obj,
                "line": msg.line,
                "column": msg.column,
                "path": msg.path,
                "symbol": msg.symbol,
                # pylint: disable=deprecated-method; deprecated since 3.2.
                "message": cgi.escape(msg.msg or ""),
                "message-id": msg.msg_id,
            }
        )

    def display_messages(self, layout):
        """Launch layouts display"""
        if self.cfg:
            if self.messages and not self.cfg.reports and not self.cfg.score:
                print(json.dumps(self.messages, indent=4), file=self.out)
        elif self.messages:
            print(json.dumps(self.messages, indent=4), file=self.out)

    def display_reports(self, layout):  # pylint: disable=arguments-differ
        """"Add a report type in output JSON"""
        print_msg = False
        msg = layout.children[1].children[0].data
        
        if " statements analysed." in msg and self.cfg:
            # Number of analyzed statements case
            try:
                parsed_msg = msg.split(" statements analysed.")
                dict_statements = {}
                dict_statements["type"] = "report"
                dict_statements["output"] = "Number of statements analyzed"
                dict_statements["number"] = int(parsed_msg[0])
            except Exception as err:
                raise Exception("Error during JSON statements number supply: {}".format(err))
            else:
                self.messages.append(dict_statements)
                print_msg = not self.cfg.score
            
        elif "Your code has been rated at" in msg and self.cfg:
            # Rate case
            try:
                parsed_msg = msg.split("/10")
                rate = parsed_msg[0].split("at ")[1]
                previous_rate = parsed_msg[1].split("run: ")[1]

                dict_rate = {}
                dict_rate["type"] = "score"
                dict_rate["output"] = "run"
                dict_rate["rate"] = float(rate)

                dict_previous_rate = {}
                dict_previous_rate["type"] = "score"
                dict_previous_rate["output"] = "previous run"
                dict_previous_rate["rate"] = float(previous_rate)
            except Exception as err:
                raise Exception("Error during JSON rate supply")
            else:
                self.messages.append(dict_rate)
                self.messages.append(dict_previous_rate)
                print_msg = True
                
        if print_msg:
            print(json.dumps(self.messages, indent=4), file=self.out)

    def _display(self, layout):
        """Don't do nothing."""


def register(linter):
    """Register the reporter classes with the linter."""
    linter.register_reporter(JSONReporter)
