# Copyright (c) 2009-2010 Arista Networks, Inc. - James Lingard
# Copyright (c) 2004-2013 LOGILAB S.A. (Paris, FRANCE).
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
"""Checker for string formatting operations.
"""

import sys
import tokenize

import astroid

from pylint.interfaces import ITokenChecker, IAstroidChecker, IRawChecker
from pylint.checkers import BaseChecker, BaseTokenChecker
from pylint.checkers import utils
from pylint.checkers.utils import check_messages

_PY3K = sys.version_info >= (3, 0)

MSGS = {
    'E1300': ("Unsupported format character %r (%#02x) at index %d",
              "bad-format-character",
              "Used when a unsupported format character is used in a format\
              string."),
    'E1301': ("Format string ends in middle of conversion specifier",
              "truncated-format-string",
              "Used when a format string terminates before the end of a \
              conversion specifier."),
    'E1302': ("Mixing named and unnamed conversion specifiers in format string",
              "mixed-format-string",
              "Used when a format string contains both named (e.g. '%(foo)d') \
              and unnamed (e.g. '%d') conversion specifiers.  This is also \
              used when a named conversion specifier contains * for the \
              minimum field width and/or precision."),
    'E1303': ("Expected mapping for format string, not %s",
              "format-needs-mapping",
              "Used when a format string that uses named conversion specifiers \
              is used with an argument that is not a mapping."),
    'W1300': ("Format string dictionary key should be a string, not %s",
              "bad-format-string-key",
              "Used when a format string that uses named conversion specifiers \
              is used with a dictionary whose keys are not all strings."),
    'W1301': ("Unused key %r in format string dictionary",
              "unused-format-string-key",
              "Used when a format string that uses named conversion specifiers \
              is used with a dictionary that conWtains keys not required by the \
              format string."),
    'E1304': ("Missing key %r in format string dictionary",
              "missing-format-string-key",
              "Used when a format string that uses named conversion specifiers \
              is used with a dictionary that doesn't contain all the keys \
              required by the format string."),
    'E1305': ("Too many arguments for format string",
              "too-many-format-args",
              "Used when a format string that uses unnamed conversion \
              specifiers is given too many arguments."),
    'E1306': ("Not enough arguments for format string",
              "too-few-format-args",
              "Used when a format string that uses unnamed conversion \
              specifiers is given too few arguments"),
    }

OTHER_NODES = (astroid.Const, astroid.List, astroid.Backquote,
               astroid.Lambda, astroid.Function,
               astroid.ListComp, astroid.SetComp, astroid.GenExpr)

class StringFormatChecker(BaseChecker):
    """Checks string formatting operations to ensure that the format string
    is valid and the arguments match the format string.
    """

    __implements__ = (IAstroidChecker,)
    name = 'string'
    msgs = MSGS

    @check_messages(*(MSGS.keys()))
    def visit_binop(self, node):
        if node.op != '%':
            return
        left = node.left
        args = node.right

        if not (isinstance(left, astroid.Const)
            and isinstance(left.value, basestring)):
            return
        format_string = left.value
        try:
            required_keys, required_num_args = \
                utils.parse_format_string(format_string)
        except utils.UnsupportedFormatCharacter, e:
            c = format_string[e.index]
            self.add_message('bad-format-character', node=node, args=(c, ord(c), e.index))
            return
        except utils.IncompleteFormatString:
            self.add_message('truncated-format-string', node=node)
            return
        if required_keys and required_num_args:
            # The format string uses both named and unnamed format
            # specifiers.
            self.add_message('mixed-format-string', node=node)
        elif required_keys:
            # The format string uses only named format specifiers.
            # Check that the RHS of the % operator is a mapping object
            # that contains precisely the set of keys required by the
            # format string.
            if isinstance(args, astroid.Dict):
                keys = set()
                unknown_keys = False
                for k, _ in args.items:
                    if isinstance(k, astroid.Const):
                        key = k.value
                        if isinstance(key, basestring):
                            keys.add(key)
                        else:
                            self.add_message('bad-format-string-key', node=node, args=key)
                    else:
                        # One of the keys was something other than a
                        # constant.  Since we can't tell what it is,
                        # supress checks for missing keys in the
                        # dictionary.
                        unknown_keys = True
                if not unknown_keys:
                    for key in required_keys:
                        if key not in keys:
                            self.add_message('missing-format-string-key', node=node, args=key)
                for key in keys:
                    if key not in required_keys:
                        self.add_message('unused-format-string-key', node=node, args=key)
            elif isinstance(args, OTHER_NODES + (astroid.Tuple,)):
                type_name = type(args).__name__
                self.add_message('format-needs-mapping', node=node, args=type_name)
            # else:
                # The RHS of the format specifier is a name or
                # expression.  It may be a mapping object, so
                # there's nothing we can check.
        else:
            # The format string uses only unnamed format specifiers.
            # Check that the number of arguments passed to the RHS of
            # the % operator matches the number required by the format
            # string.
            if isinstance(args, astroid.Tuple):
                num_args = len(args.elts)
            elif isinstance(args, OTHER_NODES + (astroid.Dict, astroid.DictComp)):
                num_args = 1
            else:
                # The RHS of the format specifier is a name or
                # expression.  It could be a tuple of unknown size, so
                # there's nothing we can check.
                num_args = None
            if num_args is not None:
                if num_args > required_num_args:
                    self.add_message('too-many-format-args', node=node)
                elif num_args < required_num_args:
                    self.add_message('too-few-format-args', node=node)


class StringMethodsChecker(BaseChecker):
    __implements__ = (IAstroidChecker,)
    name = 'string'
    msgs = {
        'E1310': ("Suspicious argument in %s.%s call",
                  "bad-str-strip-call",
                  "The argument to a str.{l,r,}strip call contains a"
                  " duplicate character, "),
        }

    @check_messages(*(MSGS.keys()))
    def visit_callfunc(self, node):
        func = utils.safe_infer(node.func)
        if (isinstance(func, astroid.BoundMethod)
            and isinstance(func.bound, astroid.Instance)
            and func.bound.name in ('str', 'unicode', 'bytes')
            and func.name in ('strip', 'lstrip', 'rstrip')
            and node.args):
            arg = utils.safe_infer(node.args[0])
            if not isinstance(arg, astroid.Const):
                return
            if len(arg.value) != len(set(arg.value)):
                self.add_message('bad-str-strip-call', node=node,
                                 args=(func.bound.name, func.name))


class StringConstantChecker(BaseTokenChecker):
    """Check string literals"""
    __implements__ = (ITokenChecker, IRawChecker)
    name = 'string_constant'
    msgs = {
        'W1401': ('Anomalous backslash in string: \'%s\'. '
                  'String constant might be missing an r prefix.',
                  'anomalous-backslash-in-string',
                  'Used when a backslash is in a literal string but not as an '
                  'escape.'),
        'W1402': ('Anomalous Unicode escape in byte string: \'%s\'. '
                  'String constant might be missing an r or u prefix.',
                  'anomalous-unicode-escape-in-string',
                  'Used when an escape like \\u is encountered in a byte '
                  'string where it has no effect.'),
        }

    # Characters that have a special meaning after a backslash in either
    # Unicode or byte strings.
    ESCAPE_CHARACTERS = 'abfnrtvx\n\r\t\\\'\"01234567'

    # TODO(mbp): Octal characters are quite an edge case today; people may
    # prefer a separate warning where they occur.  \0 should be allowed.

    # Characters that have a special meaning after a backslash but only in
    # Unicode strings.
    UNICODE_ESCAPE_CHARACTERS = 'uUN'

    def process_module(self, module):
        self._unicode_literals = 'unicode_literals' in module.future_imports

    def process_tokens(self, tokens):
        for (tok_type, token, (start_row, start_col), _, _) in tokens:
            if tok_type == tokenize.STRING:
                # 'token' is the whole un-parsed token; we can look at the start
                # of it to see whether it's a raw or unicode string etc.
                self.process_string_token(token, start_row, start_col)

    def process_string_token(self, token, start_row, start_col):
        for i, c in enumerate(token):
            if c in '\'\"':
                quote_char = c
                break
        prefix = token[:i].lower() #  markers like u, b, r.
        after_prefix = token[i:]
        if after_prefix[:3] == after_prefix[-3:] == 3 * quote_char:
            string_body = after_prefix[3:-3]
        else:
            string_body = after_prefix[1:-1]  # Chop off quotes
        # No special checks on raw strings at the moment.
        if 'r' not in prefix:
            self.process_non_raw_string_token(prefix, string_body,
                start_row, start_col)

    def process_non_raw_string_token(self, prefix, string_body, start_row,
                                     start_col):
        """check for bad escapes in a non-raw string.

        prefix: lowercase string of eg 'ur' string prefix markers.
        string_body: the un-parsed body of the string, not including the quote
        marks.
        start_row: integer line number in the source.
        start_col: integer column number in the source.
        """
        # Walk through the string; if we see a backslash then escape the next
        # character, and skip over it.  If we see a non-escaped character,
        # alert, and continue.
        #
        # Accept a backslash when it escapes a backslash, or a quote, or
        # end-of-line, or one of the letters that introduce a special escape
        # sequence <http://docs.python.org/reference/lexical_analysis.html>
        #
        # TODO(mbp): Maybe give a separate warning about the rarely-used
        # \a \b \v \f?
        #
        # TODO(mbp): We could give the column of the problem character, but
        # add_message doesn't seem to have a way to pass it through at present.
        i = 0
        while True:
            i = string_body.find('\\', i)
            if i == -1:
                break
            # There must be a next character; having a backslash at the end
            # of the string would be a SyntaxError.
            next_char = string_body[i+1]
            match = string_body[i:i+2]
            if next_char in self.UNICODE_ESCAPE_CHARACTERS:
                if 'u' in prefix:
                    pass
                elif (_PY3K or self._unicode_literals) and 'b' not in prefix:
                    pass  # unicode by default
                else:
                    self.add_message('anomalous-unicode-escape-in-string', 
                                     line=start_row, args=(match, ))
            elif next_char not in self.ESCAPE_CHARACTERS:
                self.add_message('anomalous-backslash-in-string', 
                                 line=start_row, args=(match, ))
            # Whether it was a valid escape or not, backslash followed by
            # another character can always be consumed whole: the second
            # character can never be the start of a new backslash escape.
            i += 2



def register(linter):
    """required method to auto register this checker """
    linter.register_checker(StringFormatChecker(linter))
    linter.register_checker(StringMethodsChecker(linter))
    linter.register_checker(StringConstantChecker(linter))
