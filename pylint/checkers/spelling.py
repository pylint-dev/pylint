# -*- coding: utf-8 -*-
# Copyright (c) 2014-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Michal Nowikowski <godfryd@gmail.com>
# Copyright (c) 2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2015 Pavel Roskin <proski@gnu.org>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016-2017 Pedro Algarvio <pedro@algarvio.me>
# Copyright (c) 2016 Alexander Todorov <atodorov@otb.bg>
# Copyright (c) 2017 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2017 Mikhail Fesenko <proggga@gmail.com>
# Copyright (c) 2018 Mike Frysinger <vapier@gmail.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2018 Anthony Sottile <asottile@umich.edu>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Checker for spelling errors in comments and docstrings.
"""

import os
import sys
import tokenize
import re
import hunspell
from ddtrace import tracer

from pylint.interfaces import ITokenChecker, IAstroidChecker
from pylint.checkers import BaseTokenChecker
from pylint.checkers.utils import check_messages

from pylint.checkers.spelling_tokenizer import (
    EnglishWordFilter,
    WikiWordFilter,
    CamelCasedWordsFilter,
    ForwardSlashChunker,
    get_tokenizer,
)


class SpellingChecker(BaseTokenChecker):
    """Check spelling in comments and docstrings"""

    __implements__ = (ITokenChecker, IAstroidChecker)
    name = "spelling"
    msgs = {
        "C0401": (
            "Wrong spelling of a word '%s' in a comment:\n%s\n"
            "%s\nDid you mean: '%s'?",
            "wrong-spelling-in-comment",
            "Used when a word in comment is not spelled correctly.",
        ),
        "C0402": (
            "Wrong spelling of a word '%s' in a docstring:\n%s\n"
            "%s\nDid you mean: '%s'?",
            "wrong-spelling-in-docstring",
            "Used when a word in docstring is not spelled correctly.",
        ),
        "C0403": (
            "Invalid characters %r in a docstring",
            "invalid-characters-in-docstring",
            "Used when a word in docstring cannot be checked by hunspell.",
        ),
    }
    options = (
        (
            "spelling-dict",
            {
                "default": "",
                "type": "choice",
                "metavar": "<dict name>",
                "choices": ["", "en_US"],
                "help": "Spelling dictionary name. ",
                "Available dictionaries": "en-US",
            },
        ),
        (
            "spelling-ignore-words",
            {
                "default": "",
                "type": "string",
                "metavar": "<comma separated words>",
                "help": "List of comma separated words that " "should not be checked.",
            },
        ),
        (
            "spelling-private-dict-file",
            {
                "default": "",
                "type": "string",
                "metavar": "<path to file>",
                "help": "A path to a file that contains private "
                "dictionary; one word per line.",
            },
        ),
        (
            "spelling-store-unknown-words",
            {
                "default": "n",
                "type": "yn",
                "metavar": "<y_or_n>",
                "help": "Tells whether to store unknown words to "
                "indicated private dictionary in "
                "--spelling-private-dict-file option instead of "
                "raising a message.",
            },
        ),
        (
            "max-spelling-suggestions",
            {
                "default": 4,
                "type": "int",
                "metavar": "N",
                "help": "Limits count of emitted suggestions for " "spelling mistakes.",
            },
        ),
    )

    def open(self):
        self.initialized = False
        self.private_dict_file = None

        dict_name = self.config.spelling_dict
        if not dict_name:
            return

        self.ignore_list = [
            w.strip() for w in self.config.spelling_ignore_words.split(",")
        ]
        # "param" appears in docstring in param description and
        # "pylint" appears in comments in pylint pragmas.
        self.ignore_list.extend(["param", "pylint"])

        # Expand tilde to allow e.g. spelling-private-dict-file = ~/.pylintdict
        if self.config.spelling_private_dict_file:
            self.config.spelling_private_dict_file = os.path.expanduser(
                self.config.spelling_private_dict_file
            )

        if self.config.spelling_store_unknown_words:
            self.unknown_words = set()

        self.hobj = hunspell.HunSpell(
            "/Users/siva.mahadevan/Library/Spelling/en_US.dic",
            "/Users/siva.mahadevan/Library/Spelling/en_US.aff",
        )

        self.tokenizer = get_tokenizer(
            filters=[
                EnglishWordFilter(),
                WikiWordFilter(),
                CamelCasedWordsFilter(),
            ],
            chunkers=[
                ForwardSlashChunker(),
            ],
        )
        self.initialized = True

    def close(self):
        if self.private_dict_file:
            self.private_dict_file.close()

    @tracer.wrap(service="pylint-new")
    def _check_spelling(self, msgid, line, line_num):
        span = tracer.trace("next_token")
        for word in self.tokenizer.tokenize(line):
            span.finish()
            # Skip words from ignore list.
            if word in self.ignore_list:
                continue

            # Strip starting u' from unicode literals and r' from raw strings.
            if word.startswith(("u'", 'u"', "r'", 'r"')) and len(word) > 2:
                word = word[2:]

            # If it is a known word, then continue.
            # Spell check is case sensitive by default, since 'unicode' is
            # a spelling mistake, but 'Unicode' is not.
            with tracer.trace("spellcheck"):
                if self.hobj.spell(word):
                    continue

            # Store word to private dict or raise a message.
            if self.config.spelling_store_unknown_words:
                if word not in self.unknown_words:
                    self.private_dict_file.write("%s\n" % word)
                    self.unknown_words.add(word)
                continue

            # Present up to N suggestions.
            if self.config.max_spelling_suggestions > 0:
                with tracer.trace("suggest"):
                    suggestions = self.hobj.suggest(word)
                del suggestions[self.config.max_spelling_suggestions:]
            else:
                suggestions = []

            m = re.search(r"\b({})\b".format(re.escape(word)), line)
            col = m.regs[1][0]
            indicator = (" " * col) + ("^" * len(word))

            self.add_message(
                msgid,
                line=line_num,
                args=(
                    word,
                    line,
                    indicator,
                    "'{}'".format("' or '".join(suggestions)),
                ),
            )
            span = tracer.trace("next_token")

        span.finish()

    @tracer.wrap(service="pylint-new")
    def process_tokens(self, tokens):
        if not self.initialized:
            return

        # Process tokens and look for comments.
        for (tok_type, token, (start_row, _), _, _) in tokens:
            if tok_type == tokenize.COMMENT:
                if start_row == 1 and token.startswith("#!/"):
                    # Skip shebang lines
                    continue
                if token.startswith("# pylint:"):
                    # Skip pylint enable/disable comments
                    continue
                self._check_spelling("wrong-spelling-in-comment", token, start_row)

    @check_messages("wrong-spelling-in-docstring")
    def visit_module(self, node):
        if not self.initialized:
            return
        self._check_docstring(node)

    @check_messages("wrong-spelling-in-docstring")
    def visit_classdef(self, node):
        if not self.initialized:
            return
        self._check_docstring(node)

    @check_messages("wrong-spelling-in-docstring")
    def visit_functiondef(self, node):
        if not self.initialized:
            return
        self._check_docstring(node)

    def _check_docstring(self, node):
        """check the node has any spelling errors"""
        docstring = node.doc
        if not docstring:
            return

        start_line = node.lineno + 1

        # Go through lines of docstring
        for idx, line in enumerate(docstring.splitlines()):
            self._check_spelling("wrong-spelling-in-docstring", line, start_line + idx)


def register(linter):
    """required method to auto register this checker """
    linter.register_checker(SpellingChecker(linter))
