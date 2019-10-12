# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

from collections import namedtuple
from typing import List
import re

# Allow stopping after the first semicolon/hash encountered,
# so that an option can be continued with the reasons
# why it is active or disabled.
OPTION_RGX = r"""
    \s*                # Any number of whithespace
    \#?                # One or zero hash
    .*                 # Anything (as much as possible)
    (\s*               # Beginning of first matched group and any number of whitespaces
    \#                 # Beginning of comment
    .*?                # Anything (as little as possible)
    \bpylint:          # pylint word and column
    \s*                # Any number of whitespaces
    ([^;#\n]+))        # Anything except semicolon or hash or newline (it is the second matched group) 
                       # and end of the first matched group
    [;#]{0,1}"""       # From 0 to 1 repetition of semicolon or hash
OPTION_PO = re.compile(OPTION_RGX, re.VERBOSE)


PragmaRepresenter = namedtuple('PragmaRepresenter', "action messages")


TOKEN_SPECIFICATION = [
    ('KEYWORD', r"\b(disable-all|skip-file|disable-msg|enable-msg|disable|enable)\b"),
    ('MESSAGE_STRING', r'[A-Za-z\-]{2,}'),  # Identifiers
    ('ASSIGN', r'='),      # Assignment operator
    ('MESSAGE_NUMBER', r'[CREIWF]{1}\d{4}'),
]
TOK_REGEX = '|'.join('(?P<{:s}>{:s})'.format(token_name, token_rgx) for token_name, token_rgx in TOKEN_SPECIFICATION)


class PragmaParserError(Exception):
    """
    A class for exceptions thrown by pragma_parser module
    """
    def __init__(self, message, token):
        """
        :args message: explain the reason why the exception has been thrown
        :args token: token concerned by the exception
        """
        self.message = message
        self.token = token


def parse_pragma(pylint_pragma: str) -> List[PragmaRepresenter]:
    action = None
    messages = []
    requiring_assignment = (False, '')
    for mo in re.finditer(TOK_REGEX, pylint_pragma):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'ASSIGN' and not requiring_assignment[0]:
            raise PragmaParserError('The assignment operator = should '
                                    'not be present right after the token', requiring_assignment[1])
        elif requiring_assignment[0] and kind != 'ASSIGN':
            raise PragmaParserError('The assignment operator = is '
                                    'missing right after the token', requiring_assignment[1])
        else:
            requiring_assignment = (False, requiring_assignment[1])
        if kind == 'KEYWORD':
            if action:
                yield PragmaRepresenter(action, messages)
            action = value
            messages = list()
            if value in ('disable-msg', 'enable-msg', 'disable', 'enable'):
                requiring_assignment = (True, value)
            else:
                requiring_assignment = (False, value)
        elif kind in ('MESSAGE_STRING', 'MESSAGE_NUMBER'):
            messages.append(value)
    if action:
        yield PragmaRepresenter(action, messages)