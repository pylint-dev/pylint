# Copyright (c) 2009-2010 Arista Networks, Inc. - James Lingard
# Copyright (c) 2004-2010 LOGILAB S.A. (Paris, FRANCE).
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
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


"""Checker for string formatting operations.
"""

import string
from logilab import astng
from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker

MSGS = {
    'E9900': ("Unsupported format character %r (%#02x) at index %d",
              "Used when a unsupported format character is used in a format\
              string."),
    'E9901': ("Format string ends in middle of conversion specifier",
              "Used when a format string terminates before the end of a \
              conversion specifier."),
    'E9902': ("Mixing named and unnamed conversion specifiers in format string",
              "Used when a format string contains both named (e.g. '%(foo)d') \
              and unnamed (e.g. '%d') conversion specifiers.  This is also \
              used when a named conversion specifier contains * for the \
              minimum field width and/or precision."),
    'E9903': ("Expected mapping for format string, not %s",
              "Used when a format string that uses named conversion specifiers \
              is used with an argument that is not a mapping."),
    'W9900': ("Format string dictionary key should be a string, not %s",
              "Used when a format string that uses named conversion specifiers \
              is used with a dictionary whose keys are not all strings."),
    'W9901': ("Unused key %r in format string dictionary",
              "Used when a format string that uses named conversion specifiers \
              is used with a dictionary that conWtains keys not required by the \
              format string."),
    'E9904': ("Missing key %r in format string dictionary",
              "Used when a format string that uses named conversion specifiers \
              is used with a dictionary that doesn't contain all the keys \
              required by the format string."),
    'E9905': ("Too many arguments for format string",
              "Used when a format string that uses unnamed conversion \
              specifiers is given too few arguments."),
    'E9906': ("Not enough arguments for format string",
              "Used when a format string that uses unnamed conversion \
              specifiers is given too many arguments"),
    }

class IncompleteFormatString(Exception):
    """A format string ended in the middle of a format specifier."""
    pass

class UnsupportedFormatCharacter(Exception):
    """A format character in a format string is not one of the supported
    format characters."""
    def __init__(self, index):
        Exception.__init__(self, index)
        self.index = index

def parse_format_string(format_string):
    """Parses a format string, returning a tuple of (keys, num_args), where keys
    is the set of mapping keys in the format string, and num_args is the number
    of arguments required by the format string.  Raises
    IncompleteFormatString or UnsupportedFormatCharacter if a
    parse error occurs."""
    keys = set()
    num_args = 0
    def next_char(i):
        i += 1
        if i == len(format_string):
            raise IncompleteFormatString
        return (i, format_string[i])
    i = 0
    while i < len(format_string):
        c = format_string[i]
        if c == '%':
            i, c = next_char(i)
            # Parse the mapping key (optional).
            key = None
            if c == '(':
                depth = 1
                i, c = next_char(i)
                key_start = i
                while depth != 0:
                    if c == '(':
                        depth += 1
                    elif c == ')':
                        depth -= 1
                    i, c = next_char(i)
                key_end = i - 1
                key = format_string[key_start:key_end]

            # Parse the conversion flags (optional).
            while c in '#0- +':
                i, c = next_char(i)
            # Parse the minimum field width (optional).
            if c == '*':
                num_args += 1
                i, c = next_char(i)
            else:
                while c in string.digits:
                    i, c = next_char(i)
            # Parse the precision (optional).
            if c == '.':
                i, c = next_char(i)
                if c == '*':
                    num_args += 1
                    i, c = next_char(i)
                else:
                    while c in string.digits:
                        i, c = next_char(i)
            # Parse the length modifier (optional).
            if c in 'hlL':
                i, c = next_char(i)
            # Parse the conversion type (mandatory).
            if c not in 'diouxXeEfFgGcrs%':
                raise UnsupportedFormatCharacter(i)
            if key:
                keys.add(key)
            elif c != '%':
                num_args += 1
        i += 1
    return keys, num_args

OTHER_NODES = (astng.Const, astng.List, astng.Backquote,
               astng.Lambda, astng.Function,
               astng.ListComp, astng.SetComp, astng.GenExpr)

class StringFormatChecker(BaseChecker):
    """Checks string formatting operations to ensure that the format string
    is valid and the arguments match the format string.
    """

    __implements__ = (IASTNGChecker,)
    name = 'string_format'
    msgs = MSGS

    def visit_binop(self, node):
        if node.op != '%':
            return
        left = node.left
        args = node.right

        if not (isinstance(left, astng.Const)
            and isinstance(left.value, basestring)):
            return
        format_string = left.value
        try:
            required_keys, required_num_args = \
                parse_format_string(format_string)
        except UnsupportedFormatCharacter, e:
            c = format_string[e.index]
            self.add_message('E9900', node=node, args=(c, ord(c), e.index))
            return
        except IncompleteFormatString:
            self.add_message('E9901', node=node)
            return
        if required_keys and required_num_args:
            # The format string uses both named and unnamed format
            # specifiers.
            self.add_message('E9902', node=node)
        elif required_keys:
            # The format string uses only named format specifiers.
            # Check that the RHS of the % operator is a mapping object
            # that contains precisely the set of keys required by the
            # format string.
            if isinstance(args, astng.Dict):
                keys = set()
                unknown_keys = False
                for k, v in args.items:
                    if isinstance(k, astng.Const):
                        key = k.value
                        if isinstance(key, basestring):
                            keys.add(key)
                        else:
                            self.add_message('W9900', node=node, args=key)
                    else:
                        # One of the keys was something other than a
                        # constant.  Since we can't tell what it is,
                        # supress checks for missing keys in the
                        # dictionary.
                        unknown_keys = True
                if not unknown_keys:
                    for key in required_keys:
                        if key not in keys:
                            self.add_message('E9904', node=node, args=key)
                for key in keys:
                    if key not in required_keys:
                        self.add_message('W9901', node=node, args=key)
            elif isinstance(args, OTHER_NODES + (astng.Tuple,)):
                type_name = type(args).__name__
                self.add_message('E9903', node=node, args=type_name)
            # else:
                # The RHS of the format specifier is a name or
                # expression.  It may be a mapping object, so
                # there's nothing we can check.
        else:
            # The format string uses only unnamed format specifiers.
            # Check that the number of arguments passed to the RHS of
            # the % operator matches the number required by the format
            # string.
            if isinstance(args, astng.Tuple):
                num_args = len(args.elts)
            elif isinstance(args, OTHER_NODES + (astng.Dict, astng.DictComp)):
                num_args = 1
            else:
                # The RHS of the format specifier is a name or
                # expression.  It could be a tuple of unknown size, so
                # there's nothing we can check.
                num_args = None
            if num_args is not None:
                if num_args > required_num_args:
                    self.add_message('E9905', node=node)
                elif num_args < required_num_args:
                    self.add_message('E9906', node=node)


def register(linter):
    """required method to auto register this checker """
    linter.register_checker(StringFormatChecker(linter))
