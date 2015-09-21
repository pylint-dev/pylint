# Copyright (c) 2003-2014 LOGILAB S.A. (Paris, FRANCE).
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
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
    name = 'json'
    extension = 'json'

    def __init__(self, output=sys.stdout):
        BaseReporter.__init__(self, output)
        self.messages = []

    def handle_message(self, message):
        """Manage message of different type and in the context of path."""

        self.messages.append({
            'type': message.category,
            'module': message.module,
            'obj': message.obj,
            'line': message.line,
            'column': message.column,
            'path': message.path,
            'symbol': message.symbol,
            # pylint: disable=deprecated-method; deprecated since 3.2.
            'message': cgi.escape(message.msg or ''),
        })

    def _display(self, layout):
        """Launch layouts display"""
        if self.messages:
            print(json.dumps(self.messages, indent=4), file=self.out)


def register(linter):
    """Register the reporter classes with the linter."""
    linter.register_reporter(JSONReporter)
