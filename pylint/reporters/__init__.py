# -*- coding: utf-8 -*-
# Copyright (c) 2006, 2010, 2012-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2012-2014 Google, Inc.
# Copyright (c) 2012 FELD Boris <lothiraldan@gmail.com>
# Copyright (c) 2014-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Brett Cannon <brett@python.org>
# Copyright (c) 2014 Ricardo Gemignani <ricardo.gemignani@gmail.com>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Simu Toni <simutoni@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2017 Kári Tristan Helgason <kthelgason@gmail.com>
# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2018 Ville Skyttä <ville.skytta@upcloud.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""utilities methods and classes for reporters"""
from __future__ import print_function

import sys
import locale
import os
import warnings


CMPS = ["=", "-", "+"]

# py3k has no more cmp builtin
if sys.version_info >= (3, 0):

    def cmp(a, b):  # pylint: disable=redefined-builtin
        return (a > b) - (a < b)


def diff_string(old, new):
    """given an old and new int value, return a string representing the
    difference
    """
    diff = abs(old - new)
    diff_str = "%s%s" % (CMPS[cmp(old, new)], diff and ("%.2f" % diff) or "")
    return diff_str


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
        # Build the path prefix to strip to get relative paths
        self.path_strip_prefix = os.getcwd() + os.sep

    def handle_message(self, msg):
        """Handle a new message triggered on the current file."""

    def set_output(self, output=None):
        """set output stream"""
        self.out = output or sys.stdout

    def writeln(self, string=""):
        """write a line in the output buffer"""
        print(string, file=self.out)

    def display_reports(self, layout):
        """display results encapsulated in the layout tree"""
        self.section = 0
        if hasattr(layout, "report_id"):
            layout.children[0].children[0].data += " (%s)" % layout.report_id
        self._display(layout)

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

    name = "collector"

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
