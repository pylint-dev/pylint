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
    \s*                # Any number of whitespaces
    \#                 # Beginning of comment
    .*                 # Anything
    \bpylint:          # pylint word and column
    \s*                # Any number of whitespaces
    ([^;#]+)           # Anything except semicolon or hash
    [;#]{0,1}"""       # From 0 to 1 repetition of semicolon or hash
OPTION_PO = re.compile(OPTION_RGX, re.VERBOSE)


PragmaRepresenter = namedtuple('PragmaRepresenter', "action messages")


def parse_pragma(pylint_pragma: str) -> List[PragmaRepresenter]:
    token_specification = [
        ('KEYWORD', r"\b(disable-all|skip-file|disable-msg|enable-msg|disable|enable)\b"),
        ('MESSAGE_STRING', r'[A-Za-z\-]{2,}'),  # Identifiers
        ('ASSIGN', r'='),      # Assignment operator
        ('MESSAGE_NUMBER', r'[CREIWF]{1}\d{4}'),
    ]
    tok_regex = '|'.join('(?P<{:s}>{:s})'.format(token_name, token_rgx) for token_name, token_rgx in token_specification)

    action = None
    messages = list()
    for mo in re.finditer(tok_regex, pylint_pragma):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'KEYWORD':
            if action:
                yield PragmaRepresenter(action, messages)
            action = value
            messages = list()
        elif kind in ('MESSAGE_STRING', 'MESSAGE_NUMBER'):
            messages.append(value)
    if action:
        yield PragmaRepresenter(action, messages)