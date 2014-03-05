# Copyright (c) 2003-2013 LOGILAB S.A. (Paris, FRANCE).
#
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
"""Python code format's checker.

By default try to follow Guido's style guide :

http://www.python.org/doc/essays/styleguide.html

Some parts of the process_token method is based from The Tab Nanny std module.
"""

import keyword
import sys
import tokenize

if not hasattr(tokenize, 'NL'):
    raise ValueError("tokenize.NL doesn't exist -- tokenize module too old")

from astroid import nodes

from pylint.interfaces import ITokenChecker, IAstroidChecker, IRawChecker
from pylint.checkers import BaseTokenChecker
from pylint.checkers.utils import check_messages
from pylint.utils import WarningScope, OPTION_RGX

_KEYWORD_TOKENS = ['assert', 'del', 'elif', 'except', 'for', 'if', 'in', 'not',
                   'raise', 'return', 'while', 'yield']
if sys.version_info < (3, 0):
    _KEYWORD_TOKENS.append('print')

_SPACED_OPERATORS = ['==', '<', '>', '!=', '<>', '<=', '>=',
                     '+=', '-=', '*=', '**=', '/=', '//=', '&=', '|=', '^=',
                     '%=', '>>=', '<<=']
_OPENING_BRACKETS = ['(', '[', '{']
_CLOSING_BRACKETS = [')', ']', '}']

_EOL = frozenset([tokenize.NEWLINE, tokenize.NL, tokenize.COMMENT])

# Whitespace checking policy constants
_MUST = 0
_MUST_NOT = 1
_IGNORE = 2

# Whitespace checking config constants
_DICT_SEPARATOR = 'dict-separator'
_TRAILING_COMMA = 'trailing-comma'
_NO_SPACE_CHECK_CHOICES = [_TRAILING_COMMA, _DICT_SEPARATOR]

MSGS = {
    'C0301': ('Line too long (%s/%s)',
              'line-too-long',
              'Used when a line is longer than a given number of characters.'),
    'C0302': ('Too many lines in module (%s)', # was W0302
              'too-many-lines',
              'Used when a module has too much lines, reducing its readability.'
              ),
    'C0303': ('Trailing whitespace',
              'trailing-whitespace',
              'Used when there is whitespace between the end of a line and the '
              'newline.'),
    'C0304': ('Final newline missing',
              'missing-final-newline',
              'Used when the last line in a file is missing a newline.'),
    'W0311': ('Bad indentation. Found %s %s, expected %s',
              'bad-indentation',
              'Used when an unexpected number of indentation\'s tabulations or '
              'spaces has been found.'),
    'W0312': ('Found indentation with %ss instead of %ss',
              'mixed-indentation',
              'Used when there are some mixed tabs and spaces in a module.'),
    'W0301': ('Unnecessary semicolon', # was W0106
              'unnecessary-semicolon',
              'Used when a statement is ended by a semi-colon (";"), which \
              isn\'t necessary (that\'s python, not C ;).'),
    'C0321': ('More than one statement on a single line',
              'multiple-statements',
              'Used when more than on statement are found on the same line.',
              {'scope': WarningScope.NODE}),
    'C0325' : ('Unnecessary parens after %r keyword',
               'superfluous-parens',
               'Used when a single item in parentheses follows an if, for, or '
               'other keyword.'),
    'C0326': ('%s space %s %s %s\n%s',
              'bad-whitespace',
              ('Used when a wrong number of spaces is used around an operator, '
               'bracket or block opener.'),
              {'old_names': [('C0323', 'no-space-after-operator'),
                             ('C0324', 'no-space-after-comma'),
                             ('C0322', 'no-space-before-operator')]})
    }


if sys.version_info < (3, 0):

    MSGS.update({
    'W0331': ('Use of the <> operator',
              'old-ne-operator',
              'Used when the deprecated "<>" operator is used instead \
              of "!=".'),
    'W0332': ('Use of "l" as long integer identifier',
              'lowercase-l-suffix',
              'Used when a lower case "l" is used to mark a long integer. You '
              'should use a upper case "L" since the letter "l" looks too much '
              'like the digit "1"'),
    'W0333': ('Use of the `` operator',
              'backtick',
              'Used when the deprecated "``" (backtick) operator is used '
              'instead  of the str() function.',
              {'scope': WarningScope.NODE}),
    })


def _underline_token(token):
    length = token[3][1] - token[2][1]
    offset = token[2][1]
    return token[4] + (' ' * offset) + ('^' * length)


def _column_distance(token1, token2):
    if token1 == token2:
        return 0
    if token2[3] < token1[3]:
        token1, token2 = token2, token1
    if token1[3][0] != token2[2][0]:
        return None
    return token2[2][1] - token1[3][1]


class FormatChecker(BaseTokenChecker):
    """checks for :
    * unauthorized constructions
    * strict indentation
    * line length
    * use of <> instead of !=
    """

    __implements__ = (ITokenChecker, IAstroidChecker, IRawChecker)

    # configuration section name
    name = 'format'
    # messages
    msgs = MSGS
    # configuration options
    # for available dict keys/values see the optik parser 'add_option' method
    options = (('max-line-length',
                {'default' : 80, 'type' : "int", 'metavar' : '<int>',
                 'help' : 'Maximum number of characters on a single line.'}),
               ('ignore-long-lines',
                {'type': 'regexp', 'metavar': '<regexp>',
                 'default': r'^\s*(# )?<?https?://\S+>?$',
                 'help': ('Regexp for a line that is allowed to be longer than '
                          'the limit.')}),
               ('single-line-if-stmt',
                 {'default': False, 'type' : 'yn', 'metavar' : '<y_or_n>',
                  'help' : ('Allow the body of an if to be on the same '
                            'line as the test if there is no else.')}),
               ('no-space-check',
                {'default': ','.join(_NO_SPACE_CHECK_CHOICES),
                 'type': 'multiple_choice',
                 'choices': _NO_SPACE_CHECK_CHOICES,
                 'help': ('List of optional constructs for which whitespace '
                          'checking is disabled')}),
               ('max-module-lines',
                {'default' : 1000, 'type' : 'int', 'metavar' : '<int>',
                 'help': 'Maximum number of lines in a module'}
                ),
               ('indent-string',
                {'default' : '    ', 'type' : "string", 'metavar' : '<string>',
                 'help' : 'String used as indentation unit. This is usually \
"    " (4 spaces) or "\\t" (1 tab).'}),
               )
    def __init__(self, linter=None):
        BaseTokenChecker.__init__(self, linter)
        self._lines = None
        self._visited_lines = None

    def new_line(self, tok_type, line, line_num, junk):
        """a new line has been encountered, process it if necessary"""
        if not tok_type in junk:
            self._lines[line_num] = line.split('\n')[0]
        self.check_lines(line, line_num)

    def process_module(self, module):
        self._keywords_with_parens = set()
        for node in module.body:
            if (isinstance(node, nodes.From) and node.modname == '__future__'
                and any(name == 'print_function' for name, _ in node.names)):
                self._keywords_with_parens.add('print')

    def _check_keyword_parentheses(self, tokens, start):
        """Check that there are not unnecessary parens after a keyword.

        Parens are unnecessary if there is exactly one balanced outer pair on a
        line, and it is followed by a colon, and contains no commas (i.e. is not a
        tuple).

        Args:
        tokens: list of Tokens; the entire list of Tokens.
        start: int; the position of the keyword in the token list.
        """
        # If the next token is not a paren, we're fine.
        if tokens[start+1][1] != '(':
            return

        found_and_or = False
        depth = 0
        keyword_token = tokens[start][1]
        line_num = tokens[start][2][0]

        for i in xrange(start, len(tokens) - 1):
            token = tokens[i]

            # If we hit a newline, then assume any parens were for continuation.
            if token[0] == tokenize.NL:
                return

            if token[1] == '(':
                depth += 1
            elif token[1] == ')':
                depth -= 1
                if not depth:
                    # ')' can't happen after if (foo), since it would be a syntax error.
                    if (tokens[i+1][1] in (':', ')', ']', '}', 'in') or
                        tokens[i+1][0] in (tokenize.NEWLINE, tokenize.ENDMARKER,
                                             tokenize.COMMENT)):
                        # The empty tuple () is always accepted.
                        if i == start + 2:
                            return
                        if keyword_token == 'not':
                            if not found_and_or:
                                self.add_message('C0325', line=line_num,
                                                 args=keyword_token)
                        elif keyword_token in ('return', 'yield'):
                            self.add_message('C0325', line=line_num,
                                             args=keyword_token)
                        elif keyword_token not in self._keywords_with_parens:
                            if not (tokens[i+1][1] == 'in' and found_and_or):
                                self.add_message('C0325', line=line_num,
                                                 args=keyword_token)
                    return
            elif depth == 1:
                # This is a tuple, which is always acceptable.
                if token[1] == ',':
                    return
                # 'and' and 'or' are the only boolean operators with lower precedence
                # than 'not', so parens are only required when they are found.
                elif token[1] in ('and', 'or'):
                    found_and_or = True
                # A yield inside an expression must always be in parentheses,
                # quit early without error.
                elif token[1] == 'yield':
                    return
                # A generator expression always has a 'for' token in it, and
                # the 'for' token is only legal inside parens when it is in a
                # generator expression.  The parens are necessary here, so bail
                # without an error.
                elif token[1] == 'for':
                    return

    def _opening_bracket(self, tokens, i):
        self._bracket_stack.append(tokens[i][1])
        # Special case: ignore slices
        if tokens[i][1] == '[' and tokens[i+1][1] == ':':
            return

        if (i > 0 and (tokens[i-1][0] == tokenize.NAME and
                       not (keyword.iskeyword(tokens[i-1][1]))
                       or tokens[i-1][1] in _CLOSING_BRACKETS)):
            self._check_space(tokens, i, (_MUST_NOT, _MUST_NOT))
        else:
            self._check_space(tokens, i, (_IGNORE, _MUST_NOT))

    def _closing_bracket(self, tokens, i):
        self._bracket_stack.pop()
        # Special case: ignore slices
        if tokens[i-1][1] == ':' and tokens[i][1] == ']':
            return
        policy_before = _MUST_NOT
        if tokens[i][1] in _CLOSING_BRACKETS and tokens[i-1][1] == ',':
            if _TRAILING_COMMA in self.config.no_space_check:
                policy_before = _IGNORE

        self._check_space(tokens, i, (policy_before, _IGNORE))

    def _check_equals_spacing(self, tokens, i):
        """Check the spacing of a single equals sign."""
        if self._inside_brackets('(') or self._inside_brackets('lambda'):
            self._check_space(tokens, i, (_MUST_NOT, _MUST_NOT))
        else:
            self._check_space(tokens, i, (_MUST, _MUST))

    def _open_lambda(self, tokens, i): # pylint:disable=unused-argument
        self._bracket_stack.append('lambda')

    def _handle_colon(self, tokens, i):
        # Special case: ignore slices
        if self._inside_brackets('['):
            return
        if (self._inside_brackets('{') and
            _DICT_SEPARATOR in self.config.no_space_check):
            policy = (_IGNORE, _IGNORE)
        else:
            policy = (_MUST_NOT, _MUST)
        self._check_space(tokens, i, policy)

        if self._inside_brackets('lambda'):
            self._bracket_stack.pop()

    def _handle_comma(self, tokens, i):
        # Only require a following whitespace if this is
        # not a hanging comma before a closing bracket.
        if tokens[i+1][1] in _CLOSING_BRACKETS:
            self._check_space(tokens, i, (_MUST_NOT, _IGNORE))
        else:
            self._check_space(tokens, i, (_MUST_NOT, _MUST))

    def _check_surrounded_by_space(self, tokens, i):
        """Check that a binary operator is surrounded by exactly one space."""
        self._check_space(tokens, i, (_MUST, _MUST))

    def _check_space(self, tokens, i, policies):
        def _policy_string(policy):
            if policy == _MUST:
                return 'Exactly one', 'required'
            else:
                return 'No', 'allowed'

        def _name_construct(token):
            if tokens[i][1] == ',':
                return 'comma'
            elif tokens[i][1] == ':':
                return ':'
            elif tokens[i][1] in '()[]{}':
                return 'bracket'
            elif tokens[i][1] in ('<', '>', '<=', '>=', '!='):
                return 'comparison'
            else:
                if self._inside_brackets('('):
                    return 'keyword argument assignment'
                else:
                    return 'assignment'

        good_space = [True, True]
        pairs = [(tokens[i-1], tokens[i]), (tokens[i], tokens[i+1])]

        for other_idx, (policy, token_pair) in enumerate(zip(policies, pairs)):
            if token_pair[other_idx][0] in _EOL or policy == _IGNORE:
                continue

            distance = _column_distance(*token_pair)
            if distance is None:
                continue
            good_space[other_idx] = (
                (policy == _MUST and distance == 1) or
                (policy == _MUST_NOT and distance == 0))

        warnings = []
        if not any(good_space) and policies[0] == policies[1]:
            warnings.append((policies[0], 'around'))
        else:
            for ok, policy, position in zip(good_space, policies, ('before', 'after')):
                if not ok:
                    warnings.append((policy, position))
        for policy, position in warnings:
            construct = _name_construct(tokens[i])
            count, state = _policy_string(policy)
            self.add_message('C0326', line=tokens[i][2][0],
                             args=(count, state, position, construct,
                                   _underline_token(tokens[i])))

    def _inside_brackets(self, left):
        return self._bracket_stack[-1] == left

    def _prepare_token_dispatcher(self):
        raw = [
            (_KEYWORD_TOKENS,
             self._check_keyword_parentheses),

            (_OPENING_BRACKETS, self._opening_bracket),

            (_CLOSING_BRACKETS, self._closing_bracket),

            (['='], self._check_equals_spacing),

            (_SPACED_OPERATORS, self._check_surrounded_by_space),

            ([','], self._handle_comma),

            ([':'], self._handle_colon),

            (['lambda'], self._open_lambda),
            ]

        dispatch = {}
        for tokens, handler in raw:
            for token in tokens:
                dispatch[token] = handler
        return dispatch

    def process_tokens(self, tokens):
        """process tokens and search for :

         _ non strict indentation (i.e. not always using the <indent> parameter as
           indent unit)
         _ too long lines (i.e. longer than <max_chars>)
         _ optionally bad construct (if given, bad_construct must be a compiled
           regular expression).
        """
        self._bracket_stack = [None]
        indent = tokenize.INDENT
        dedent = tokenize.DEDENT
        newline = tokenize.NEWLINE
        junk = (tokenize.COMMENT, tokenize.NL)
        indents = [0]
        check_equal = 0
        line_num = 0
        previous = None
        self._lines = {}
        self._visited_lines = {}
        new_line_delay = False
        token_handlers = self._prepare_token_dispatcher()
        for idx, (tok_type, token, start, _, line) in enumerate(tokens):
            if new_line_delay:
                new_line_delay = False
                self.new_line(tok_type, line, line_num, junk)
            if start[0] != line_num:
                if previous is not None and previous[0] == tokenize.OP and previous[1] == ';':
                    self.add_message('W0301', line=previous[2])
                previous = None
                line_num = start[0]
                # A tokenizer oddity: if an indented line contains a multi-line
                # docstring, the line member of the INDENT token does not contain
                # the full line; therefore we delay checking the new line until
                # the next token.
                if tok_type == tokenize.INDENT:
                    new_line_delay = True
                else:
                    self.new_line(tok_type, line, line_num, junk)
            if tok_type not in (indent, dedent, newline) + junk:
                previous = tok_type, token, start[0]

            if tok_type == tokenize.OP:
                if token == '<>':
                    self.add_message('W0331', line=line_num)
            elif tok_type == tokenize.NUMBER:
                if token.endswith('l'):
                    self.add_message('W0332', line=line_num)

            elif tok_type == newline:
                # a program statement, or ENDMARKER, will eventually follow,
                # after some (possibly empty) run of tokens of the form
                #     (NL | COMMENT)* (INDENT | DEDENT+)?
                # If an INDENT appears, setting check_equal is wrong, and will
                # be undone when we see the INDENT.
                check_equal = 1

            elif tok_type == indent:
                check_equal = 0
                self.check_indent_level(token, indents[-1]+1, line_num)
                indents.append(indents[-1]+1)

            elif tok_type == dedent:
                # there's nothing we need to check here!  what's important is
                # that when the run of DEDENTs ends, the indentation of the
                # program statement (or ENDMARKER) that triggered the run is
                # equal to what's left at the top of the indents stack
                check_equal = 1
                if len(indents) > 1:
                    del indents[-1]

            elif check_equal and tok_type not in junk:
                # this is the first "real token" following a NEWLINE, so it
                # must be the first token of the next program statement, or an
                # ENDMARKER; the "line" argument exposes the leading whitespace
                # for this statement; in the case of ENDMARKER, line is an empty
                # string, so will properly match the empty string with which the
                # "indents" stack was seeded
                check_equal = 0
                self.check_indent_level(line, indents[-1], line_num)

            try:
                handler = token_handlers[token]
            except KeyError:
                pass
            else:
                handler(tokens, idx)

        line_num -= 1 # to be ok with "wc -l"
        if line_num > self.config.max_module_lines:
            self.add_message('C0302', args=line_num, line=1)

    @check_messages('C0321', 'C03232', 'C0323', 'C0324')
    def visit_default(self, node):
        """check the node line number and check it if not yet done"""
        if not node.is_statement:
            return
        if not node.root().pure_python:
            return # XXX block visit of child nodes
        prev_sibl = node.previous_sibling()
        if prev_sibl is not None:
            prev_line = prev_sibl.fromlineno
        else:
            # The line on which a finally: occurs in a try/finally
            # is not directly represented in the AST. We infer it
            # by taking the last line of the body and adding 1, which
            # should be the line of finally:
            if (isinstance(node.parent, nodes.TryFinally)
                and node in node.parent.finalbody):
                prev_line = node.parent.body[0].tolineno + 1
            else:
                prev_line = node.parent.statement().fromlineno
        line = node.fromlineno
        assert line, node
        if prev_line == line and self._visited_lines.get(line) != 2:
            self._check_multi_statement_line(node, line)
            return
        if line in self._visited_lines:
            return
        try:
            tolineno = node.blockstart_tolineno
        except AttributeError:
            tolineno = node.tolineno
        assert tolineno, node
        lines = []
        for line in xrange(line, tolineno + 1):
            self._visited_lines[line] = 1
            try:
                lines.append(self._lines[line].rstrip())
            except KeyError:
                lines.append('')

    def _check_multi_statement_line(self, node, line):
        """Check for lines containing multiple statements."""
        # Do not warn about multiple nested context managers
        # in with statements.
        if isinstance(node, nodes.With):
            return
        # For try... except... finally..., the two nodes
        # appear to be on the same line due to how the AST is built.
        if (isinstance(node, nodes.TryExcept) and
            isinstance(node.parent, nodes.TryFinally)):
            return
        if (isinstance(node.parent, nodes.If) and not node.parent.orelse
            and self.config.single_line_if_stmt):
            return
        self.add_message('C0321', node=node)
        self._visited_lines[line] = 2

    @check_messages('W0333')
    def visit_backquote(self, node):
        self.add_message('W0333', node=node)

    def check_lines(self, lines, i):
        """check lines have less than a maximum number of characters
        """
        max_chars = self.config.max_line_length
        ignore_long_line = self.config.ignore_long_lines

        for line in lines.splitlines(True):
            if not line.endswith('\n'):
                self.add_message('C0304', line=i)
            else:
                stripped_line = line.rstrip()
                if line[len(stripped_line):] not in ('\n', '\r\n'):
                    self.add_message('C0303', line=i)
                # Don't count excess whitespace in the line length.
                line = stripped_line
            mobj = OPTION_RGX.search(line)
            if mobj and mobj.group(1).split('=', 1)[0].strip() == 'disable':
                line = line.split('#')[0].rstrip()

            if len(line) > max_chars and not ignore_long_line.search(line):
                self.add_message('C0301', line=i, args=(len(line), max_chars))
            i += 1

    def check_indent_level(self, string, expected, line_num):
        """return the indent level of the string
        """
        indent = self.config.indent_string
        if indent == '\\t': # \t is not interpreted in the configuration file
            indent = '\t'
        level = 0
        unit_size = len(indent)
        while string[:unit_size] == indent:
            string = string[unit_size:]
            level += 1
        suppl = ''
        while string and string[0] in ' \t':
            if string[0] != indent[0]:
                if string[0] == '\t':
                    args = ('tab', 'space')
                else:
                    args = ('space', 'tab')
                self.add_message('W0312', args=args, line=line_num)
                return level
            suppl += string[0]
            string = string[1:]
        if level != expected or suppl:
            i_type = 'spaces'
            if indent[0] == '\t':
                i_type = 'tabs'
            self.add_message('W0311', line=line_num,
                             args=(level * unit_size + len(suppl), i_type,
                                   expected * unit_size))


def register(linter):
    """required method to auto register this checker """
    linter.register_checker(FormatChecker(linter))
