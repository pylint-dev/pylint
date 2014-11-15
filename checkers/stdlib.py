# Copyright 2012 Google Inc.
#
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""Checkers for various standard library functions."""

import re
import sys

import astroid
from astroid.bases import Instance

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from pylint.checkers import utils

_VALID_OPEN_MODE_REGEX = re.compile(r'^(r?U|[rwa]\+?b?)$')

if sys.version_info >= (3, 0):
    OPEN_MODULE = '_io'
else:
    OPEN_MODULE = '__builtin__'

class StdlibChecker(BaseChecker):
    __implements__ = (IAstroidChecker,)
    name = 'stdlib'

    msgs = {
        'W1501': ('"%s" is not a valid mode for open.',
                  'bad-open-mode',
                  'Python supports: r, w, a modes with b, +, and U options. '
                  'See http://docs.python.org/2/library/functions.html#open'),
        'W1502': ('Using datetime.time in a boolean context.',
                  'boolean-datetime',
                  'Using datetetime.time in a boolean context can hide '
                  'subtle bugs when the time they represent matches '
                  'midnight UTC. This behaviour was fixed in Python 3.5. '
                  'See http://bugs.python.org/issue13936 for reference.',
                  {'maxversion': (3, 5)}),
        }

    @utils.check_messages('bad-open-mode')
    def visit_callfunc(self, node):
        """Visit a CallFunc node."""
        if hasattr(node, 'func'):
            infer = utils.safe_infer(node.func)
            if infer and infer.root().name == OPEN_MODULE:
                if getattr(node.func, 'name', None) in ('open', 'file'):
                    self._check_open_mode(node)

    @utils.check_messages('boolean-datetime')
    def visit_unaryop(self, node):
        if node.op == 'not':
            self._check_datetime(node.operand)

    @utils.check_messages('boolean-datetime')
    def visit_if(self, node):
        self._check_datetime(node.test)

    @utils.check_messages('boolean-datetime')
    def visit_ifexp(self, node):
        self._check_datetime(node.test)

    @utils.check_messages('boolean-datetime')
    def visit_boolop(self, node):
        for value in node.values:
            self._check_datetime(value)

    def _check_datetime(self, node):
        """ Check that a datetime was infered.
        If so, emit boolean-datetime warning.
        """
        try:
            infered = next(node.infer())
        except astroid.InferenceError:
            return
        if (isinstance(infered, Instance) and
                infered.qname() == 'datetime.time'):
            self.add_message('boolean-datetime', node=node)

    def _check_open_mode(self, node):
        """Check that the mode argument of an open or file call is valid."""
        try:
            mode_arg = utils.get_argument_from_call(node, position=1, keyword='mode')
            if mode_arg:
                mode_arg = utils.safe_infer(mode_arg)
                if (isinstance(mode_arg, astroid.Const)
                        and not _VALID_OPEN_MODE_REGEX.match(mode_arg.value)):
                    self.add_message('bad-open-mode', node=node,
                                     args=(mode_arg.value))
        except (utils.NoSuchArgumentError, TypeError):
            pass

def register(linter):
    """required method to auto register this checker """
    linter.register_checker(StdlibChecker(linter))

