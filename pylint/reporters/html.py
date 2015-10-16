# Copyright (c) 2003-2013 LOGILAB S.A. (Paris, FRANCE).
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
"""HTML reporter"""

import itertools
import string
import sys

import six

from pylint.interfaces import IReporter
from pylint.reporters import BaseReporter
from pylint.reporters.ureports.html_writer import HTMLWriter
from pylint.reporters.ureports.nodes import Section, Table


class HTMLReporter(BaseReporter):
    """report messages and layouts in HTML"""

    __implements__ = IReporter
    name = 'html'
    extension = 'html'

    def __init__(self, output=sys.stdout):
        BaseReporter.__init__(self, output)
        self.msgs = []
        # Add placeholders for title and parsed messages
        self.header = None
        self.msgargs = []

    @staticmethod
    def _parse_msg_template(msg_template):
        formatter = string.Formatter()
        parsed = formatter.parse(msg_template)
        for item in parsed:
            if item[1]:
                yield item[1]

    def _parse_template(self):
        """Helper function to parse the message template"""
        self.header = []
        if self.linter.config.msg_template:
            msg_template = self.linter.config.msg_template
        else:
            msg_template = '{category}{module}{obj}{line}{column}{msg}'

        _header, _msgs = itertools.tee(self._parse_msg_template(msg_template))
        self.header = list(_header)
        self.msgargs = list(_msgs)

    def handle_message(self, msg):
        """manage message of different type and in the context of path"""

        # It would be better to do this in init, but currently we do not
        # have access to the linter (as it is setup in lint.set_reporter()
        # Therefore we try to parse just the once.
        if self.header is None:
            self._parse_template()

        # We want to add the lines given by the template
        values = [getattr(msg, field) for field in self.msgargs]
        self.msgs += [value if isinstance(value, six.text_type) else str(value)
                      for value in values]

    def set_output(self, output=None):
        """set output stream

        messages buffered for old output is processed first"""
        if self.out and self.msgs:
            self._display(Section())
        BaseReporter.set_output(self, output)

    def _display(self, layout):
        """launch layouts display

        overridden from BaseReporter to add insert the messages section
        (in add_message, message is not displayed, just collected so it
        can be displayed in an html table)
        """
        if self.msgs:
            # add stored messages to the layout
            msgs = self.header
            cols = len(self.header)
            msgs += self.msgs
            sect = Section('Messages')
            layout.append(sect)
            sect.append(Table(cols=cols, children=msgs, rheaders=1))
            self.msgs = []
        HTMLWriter().format(layout, self.out)


def register(linter):
    """Register the reporter classes with the linter."""
    linter.register_reporter(HTMLReporter)
