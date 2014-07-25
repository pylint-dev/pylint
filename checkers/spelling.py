# Copyright 2014 Michal Nowikowski.
#
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
"""Checker for spelling errors in comments and docstrings.
"""

import sys
import tokenize
import string
import re

import astroid

from pylint.interfaces import ITokenChecker, IAstroidChecker, IRawChecker
from pylint.checkers import BaseChecker, BaseTokenChecker
from pylint.checkers import utils
from pylint.checkers.utils import check_messages

try:
    import enchant
except ImportError:
    enchant = None

if enchant is not None:
    br = enchant.Broker()
    dicts = br.list_dicts()
    dict_choices = [''] + [d[0] for d in dicts]
    dicts = ["%s (%s)" % (d[0], d[1].name) for d in dicts]
    dicts = ", ".join(dicts)
    instr = ""
else:
    dicts = "none"
    dict_choices = ['']
    instr = " To make it working install python-enchant package."

table = string.maketrans("", "")

class SpellingInCommentsChecker(BaseTokenChecker):
    """Check spelling in comments"""
    __implements__ = (ITokenChecker, IAstroidChecker)
    name = 'spelling'
    msgs = {
        'C8402': ('Wrong spelling of a word \'%s\' in a comment:\n%s\n%s\nDid you mean: \'%s\'?',
                  'wrong-spelling-in-comment',
                  'Used when a word in comment is not spelled correctly.'),
        'C8403': ('Wrong spelling of a word \'%s\' in a docstring:\n%s\n%s\nDid you mean: \'%s\'?',
                  'wrong-spelling-in-docstring',
                  'Used when a word in docstring is not spelled correctly.'),
        }
    options = (('spelling-dict',
                {'default' : '', 'type' : 'choice', 'metavar' : '<dict name>',
                 'choices': dict_choices,
                 'help' : 'Spelling dictionary name. Available dictionaries: %s.%s' % (dicts, instr)}),
               ('spelling-ignore-words',
                {'default' : '', 'type' : 'string', 'metavar' : '<comma separated words>',
                 'help' : 'List of comma separated words that should not be checked.'}),
                 )

    def open(self):
        self.initialized = False

        if enchant is None:
            return

        dict_name = self.config.spelling_dict
        if not dict_name:
            return

        self.ignore_list = self.config.spelling_ignore_words.split(",")
        self.spelling_dict = enchant.Dict(dict_name)

        puncts = string.punctuation.replace("'", "")
        self.regex = re.compile('[%s]' % re.escape(puncts))

        self.initialized = True

    def process_tokens(self, tokens):
        if not self.initialized:
            return

        # process tokens and look for comments
        for (tok_type, token, (start_row, start_col), _, _) in tokens:
            if tok_type == tokenize.COMMENT:
                # replace punctuation signs with space: e.g. and/or -> and or
                comment = self.regex.sub(' ', token)

                # go through words and check them
                for w in comment.split():
                    if not w in self.ignore_list and not self.spelling_dict.check(w):
                        suggestions = self.spelling_dict.suggest(w)[:4]
                        col = token.index(w)
                        indicator = (" " * col) + ("^" * len(w))
                        self.add_message('wrong-spelling-in-comment', line=start_row,
                                         args=(w, token, indicator, "' or '".join(suggestions)))

    @check_messages('wrong-spelling-in-docstring')
    def visit_module(self, node):
        if not self.initialized:
            return
        self._check_docstring(node)

    @check_messages('wrong-spelling-in-docstring')
    def visit_class(self, node):
        if not self.initialized:
            return
        self._check_docstring(node)

    @check_messages('wrong-spelling-in-docstring')
    def visit_function(self, node):
        if not self.initialized:
            return
        self._check_docstring(node)

    def _check_docstring(self, node):
        """check the node has any spelling errors"""
        docstring = node.doc
        if not docstring:
            return

        start_line = node.lineno + 1

        # go through lines of docstring
        for idx, line in enumerate(docstring.splitlines()):
            # replace punctuation signs with space: e.g. and/or -> and or
            line2 = self.regex.sub(' ', line.strip())

            # go through words in a line and check them
            for w in line2.split():
                if not w in self.ignore_list and not self.spelling_dict.check(w):
                    suggestions = self.spelling_dict.suggest(w)[:4]
                    col = line.index(w)
                    indicator = (" " * col) + ("^" * len(w))
                    self.add_message('wrong-spelling-in-docstring', line=start_line + idx,
                                     args=(w, line, indicator, "' or '".join(suggestions)))


def register(linter):
    """required method to auto register this checker """
    linter.register_checker(SpellingInCommentsChecker(linter))
