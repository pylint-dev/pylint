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
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""checker for use of Python logging
"""

import astroid
from pylint import checkers
from pylint import interfaces
from pylint.checkers import utils
from pylint.checkers.utils import check_messages

MSGS = {
    'W1201': ('Specify string format arguments as logging function parameters',
             'logging-not-lazy',
             'Used when a logging statement has a call form of '
             '"logging.<logging method>(format_string % (format_args...))". '
             'Such calls should leave string interpolation to the logging '
             'method itself and be written '
             '"logging.<logging method>(format_string, format_args...)" '
             'so that the program may avoid incurring the cost of the '
             'interpolation in those cases in which no message will be '
             'logged. For more, see '
             'http://www.python.org/dev/peps/pep-0282/.'),
    'E1200': ('Unsupported logging format character %r (%#02x) at index %d',
              'logging-unsupported-format',
              'Used when an unsupported format character is used in a logging\
              statement format string.'),
    'E1201': ('Logging format string ends in middle of conversion specifier',
              'logging-format-truncated',
              'Used when a logging statement format string terminates before\
              the end of a conversion specifier.'),
    'E1205': ('Too many arguments for logging format string',
              'logging-too-many-args',
              'Used when a logging format string is given too few arguments.'),
    'E1206': ('Not enough arguments for logging format string',
              'logging-too-few-args',
              'Used when a logging format string is given too many arguments'),
    }


CHECKED_CONVENIENCE_FUNCTIONS = set([
    'critical', 'debug', 'error', 'exception', 'fatal', 'info', 'warn',
    'warning'])


class LoggingChecker(checkers.BaseChecker):
    """Checks use of the logging module."""

    __implements__ = interfaces.IAstroidChecker
    name = 'logging'
    msgs = MSGS

    options = (('logging-modules',
                {'default' : ('logging',),
                 'type' : 'csv',
                 'metavar' : '<comma separated list>',
                 'help' : ('Logging modules to check that the string format '
                           'arguments are in logging function parameter format')}
                ),
               )

    def visit_module(self, unused_node):
        """Clears any state left in this checker from last module checked."""
        # The code being checked can just as easily "import logging as foo",
        # so it is necessary to process the imports and store in this field
        # what name the logging module is actually given.
        self._logging_names = set()
        logging_mods = self.config.logging_modules

        self._logging_modules = set(logging_mods)
        self._from_imports = {}
        for logging_mod in logging_mods:
            parts = logging_mod.rsplit('.', 1)
            if len(parts) > 1:
                self._from_imports[parts[0]] = parts[1]

    def visit_from(self, node):
        """Checks to see if a module uses a non-Python logging module."""
        try:
            logging_name = self._from_imports[node.modname]
            for module, as_name in node.names:
                if module == logging_name:
                    self._logging_names.add(as_name or module)
        except KeyError:
            pass

    def visit_import(self, node):
        """Checks to see if this module uses Python's built-in logging."""
        for module, as_name in node.names:
            if module in self._logging_modules:
                self._logging_names.add(as_name or module)

    @check_messages(*(MSGS.keys()))
    def visit_callfunc(self, node):
        """Checks calls to logging methods."""
        def is_logging_name():
           return (isinstance(node.func, astroid.Getattr) and
                   isinstance(node.func.expr, astroid.Name) and 
                   node.func.expr.name in self._logging_names)

        def is_logger_class():
            try:
                for inferred in node.func.infer():
                    if isinstance(inferred, astroid.BoundMethod):
                        parent = inferred._proxied.parent
                        if (isinstance(parent, astroid.Class) and 
                            (parent.qname() == 'logging.Logger' or 
                             any(ancestor.qname() == 'logging.Logger' 
                                 for ancestor in parent.ancestors()))):
                            return True, inferred._proxied.name
            except astroid.exceptions.InferenceError:
                pass
            return False, None

        if is_logging_name():
            name = node.func.attrname
        else:
            result, name = is_logger_class()
            if not result:
                return
        self._check_log_method(node, name)

    def _check_log_method(self, node, name):
        """Checks calls to logging.log(level, format, *format_args)."""
        if name == 'log':
            if node.starargs or node.kwargs or len(node.args) < 2:
                # Either a malformed call, star args, or double-star args. Beyond
                # the scope of this checker.
                return
            format_pos = 1
        elif name in CHECKED_CONVENIENCE_FUNCTIONS:
            if node.starargs or node.kwargs or not node.args:
                # Either no args, star args, or double-star args. Beyond the
                # scope of this checker.
                return
            format_pos = 0
        else:
            return

        if isinstance(node.args[format_pos], astroid.BinOp) and node.args[format_pos].op == '%':
            self.add_message('logging-not-lazy', node=node)
        elif isinstance(node.args[format_pos], astroid.Const):
            self._check_format_string(node, format_pos)

    def _check_format_string(self, node, format_arg):
        """Checks that format string tokens match the supplied arguments.

        Args:
          node: AST node to be checked.
          format_arg: Index of the format string in the node arguments.
        """
        num_args = _count_supplied_tokens(node.args[format_arg + 1:])
        if not num_args:
            # If no args were supplied, then all format strings are valid -
            # don't check any further.
            return
        format_string = node.args[format_arg].value
        if not isinstance(format_string, basestring):
            # If the log format is constant non-string (e.g. logging.debug(5)),
            # ensure there are no arguments.
            required_num_args = 0
        else:
            try:
                keyword_args, required_num_args = \
                    utils.parse_format_string(format_string)
                if keyword_args:
                    # Keyword checking on logging strings is complicated by
                    # special keywords - out of scope.
                    return
            except utils.UnsupportedFormatCharacter, ex:
                char = format_string[ex.index]
                self.add_message('logging-unsupported-format', node=node,
                                 args=(char, ord(char), ex.index))
                return
            except utils.IncompleteFormatString:
                self.add_message('logging-format-truncated', node=node)
                return
        if num_args > required_num_args:
            self.add_message('logging-too-many-args', node=node)
        elif num_args < required_num_args:
            self.add_message('logging-too-few-args', node=node)


def _count_supplied_tokens(args):
    """Counts the number of tokens in an args list.

    The Python log functions allow for special keyword arguments: func,
    exc_info and extra. To handle these cases correctly, we only count
    arguments that aren't keywords.

    Args:
      args: List of AST nodes that are arguments for a log format string.

    Returns:
      Number of AST nodes that aren't keywords.
    """
    return sum(1 for arg in args if not isinstance(arg, astroid.Keyword))


def register(linter):
    """Required method to auto-register this checker."""
    linter.register_checker(LoggingChecker(linter))
