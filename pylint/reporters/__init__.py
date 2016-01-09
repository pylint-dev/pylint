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
"""utilities methods and classes for reporters"""
from __future__ import print_function

import sys
import locale
import os
import warnings

import six

CMPS = ['=', '-', '+']

# py3k has no more cmp builtin
if sys.version_info >= (3, 0):
    def cmp(a, b): # pylint: disable=redefined-builtin
        return (a > b) - (a < b)

def diff_string(old, new):
    """given a old and new int value, return a string representing the
    difference
    """
    diff = abs(old - new)
    diff_str = "%s%s" % (CMPS[cmp(old, new)], diff and ('%.2f' % diff) or '')
    return diff_str


class BaseReporter(object):
    """base class for reporters

    symbols: show short symbolic names for messages.
    """

    extension = ''

    def __init__(self, output=None):
        self.linter = None
        self.section = 0
        self.out = None
        self.out_encoding = None
        self.set_output(output)
        # Build the path prefix to strip to get relative paths
        self.path_strip_prefix = os.getcwd() + os.sep

    def handle_message(self, msg):
        """Handle a new message triggered on the current file.

        Invokes the legacy add_message API by default."""
        self.add_message(
            msg.msg_id, (msg.abspath, msg.module, msg.obj, msg.line, msg.column),
            msg.msg)

    def add_message(self, msg_id, location, msg):
        """Deprecated, do not use."""
        # pylint: disable=no-self-use,unused-argument
        msg = ("This method is deprecated, use handle_message instead. "
               "It will be removed in Pylint 1.6.")
        warnings.warn(msg, DeprecationWarning, stacklevel=2)

    def set_output(self, output=None):
        """set output stream"""
        self.out = output or sys.stdout

    if six.PY3:
        encode = lambda self, string: string
    else:
        def encode(self, string):
            if not isinstance(string, six.text_type):
                return string
            encoding = (getattr(self.out, 'encoding', None) or
                        locale.getdefaultlocale()[1] or
                        sys.getdefaultencoding())
            # errors=replace, we don't want to crash when attempting to show
            # source code line that can't be encoded with the current locale
            # settings
            return string.encode(encoding, 'replace')

    def writeln(self, string=''):
        """write a line in the output buffer"""
        print(self.encode(string), file=self.out)

    def display_reports(self, layout):
        """display results encapsulated in the layout tree"""
        self.section = 0
        if hasattr(layout, 'report_id'):
            layout.children[0].children[0].data += ' (%s)' % layout.report_id
        self._display(layout)

    def display_results(self, layout):
        warnings.warn("display_results is deprecated, use display_reports instead. "
                      "The former will be removed in Pylint 2.0.",
                      DeprecationWarning)
        self.display_reports(layout)

    def _display(self, layout):
        """display the layout"""
        raise NotImplementedError()

    def display_messages(self, layout):
        """Hook for displaying the messages of the reporter

        This will be called whenever the underlying messages
        needs to be displayed. For some reporters, it probably
        doesn't make sense to display messages as soon as they
        are available, so some mechanism of storing them could be used.
        This method can be implemented to display them after they've
        been aggregated.
        """

    # Event callbacks

    def on_set_current_module(self, module, filepath):
        """Hook called when a module starts to be analysed."""

    def on_close(self, stats, previous_stats):
        """Hook called when a module finished analyzing."""


class CollectingReporter(BaseReporter):
    """collects messages"""

    name = 'collector'

    def __init__(self):
        BaseReporter.__init__(self)
        self.messages = []

    def handle_message(self, msg):
        self.messages.append(msg)

    _display = None


def initialize(linter):
    """initialize linter with reporters in this package """
    from pylint import utils
    utils.register_plugins(linter, __path__[0])
