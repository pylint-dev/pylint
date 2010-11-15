# Copyright (c) 2009-2010 Google, Inc.
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
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""checker for use of Python logging
"""

from logilab import astng
from pylint import checkers
from pylint import interfaces

EAGER_STRING_INTERPOLATION = 'W6501'

CHECKED_CONVENIENCE_FUNCTIONS = set([
    'critical', 'debug', 'error', 'exception', 'fatal', 'info', 'warn',
    'warning'])


class LoggingChecker(checkers.BaseChecker):
    """Checks use of the logging module."""

    __implements__ = interfaces.IASTNGChecker

    name = 'logging'

    msgs = {EAGER_STRING_INTERPOLATION:
            ('Specify string format arguments as logging function parameters',
             'Used when a logging statement has a call form of '
             '"logging.<logging method>(format_string % (format_args...))". '
             'Such calls should leave string interpolation to the logging '
             'method itself and be written '
             '"logging.<logging method>(format_string, format_args...)" '
             'so that the program may avoid incurring the cost of the '
             'interpolation in those cases in which no message will be '
             'logged. For more, see '
             'http://www.python.org/dev/peps/pep-0282/.')
            }

    def visit_module(self, unused_node):
        """Clears any state left in this checker from last module checked."""
        # The code being checked can just as easily "import logging as foo",
        # so it is necessary to process the imports and store in this field
        # what name the logging module is actually given.
        self._logging_name = None

    def visit_import(self, node):
        """Checks to see if this module uses Python's built-in logging."""
        for module, as_name in node.names:
            if module == 'logging':
                if as_name:
                    self._logging_name = as_name
                else:
                    self._logging_name = 'logging'

    def visit_callfunc(self, node):
        """Checks calls to (simple forms of) logging methods."""
        if (not isinstance(node.func, astng.Getattr)
            or not isinstance(node.func.expr, astng.Name)
            or node.func.expr.name != self._logging_name):
            return
        self._CheckConvenienceMethods(node)
        self._CheckLogMethod(node)

    def _CheckConvenienceMethods(self, node):
        """Checks calls to logging convenience methods (like logging.warn)."""
        if node.func.attrname not in CHECKED_CONVENIENCE_FUNCTIONS:
            return
        if not node.args:
            # Either no args, or star args, or double-star args. Beyond the
            # scope of this checker in any case.
            return
        if isinstance(node.args[0], astng.BinOp) and node.args[0].op == '%':
            self.add_message(EAGER_STRING_INTERPOLATION, node=node)

    def _CheckLogMethod(self, node):
        """Checks calls to logging.log(level, format, *format_args)."""
        if node.func.attrname != 'log':
            return
        if len(node.args) < 2:
            # Either a malformed call or something with crazy star args or
            # double-star args magic. Beyond the scope of this checker.
            return
        if isinstance(node.args[1], astng.BinOp) and node.args[1].op == '%':
            self.add_message(EAGER_STRING_INTERPOLATION, node=node)

def register(linter):
    """Required method to auto-register this checker."""
    linter.register_checker(LoggingChecker(linter))
