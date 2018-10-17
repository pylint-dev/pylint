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
# Copyright (c) 2018 Siva Mahadevan <svmhdvn@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Checker for spelling errors in comments and docstrings.
"""

import os
import tokenize
import re

try:
    import hunspell
except ImportError:
    hunspell = None

from pylint.interfaces import ITokenChecker, IAstroidChecker
from pylint.checkers import BaseTokenChecker
from pylint.checkers.utils import check_messages


class Tokenizer:
    def __init__(self, filters, chunkers):
        self.filters = filters
        self.chunkers = chunkers
        self.sub_tokens = []

    def __iter__(self):
        return self

    def __next__(self):
        valid = False
        while not valid:
            valid = True

            if self.sub_tokens:
                base_token = self.sub_tokens.pop()
            else:
                base_token = self.next()  # pylint: disable=E1111

            for f in self.filters:
                if f.skip(base_token):
                    valid = False
                    break

        for c in self.chunkers:
            chunks = c.split(base_token)
            if len(chunks) > 1:
                self.sub_tokens.extend(chunks)
                return self.sub_tokens.pop()

        return base_token

    def tokenize(self, text):
        self._text = text
        self._offset = 0
        return self

    # pylint: disable=R0201
    def next(self):
        raise StopIteration()


class WordTokenizer(Tokenizer):
    """Tokenizer class that performs very basic word-finding.

    This tokenizer does the most basic thing that could work - it splits
    text into words based on whitespace boundaries, and removes basic
    punctuation symbols from the start and end of each word.
    """

    # Chars to remove from start/end of words
    strip_from_start = set("\"'`([<{")
    strip_from_end = set("\"'`]).!,?;:>}")

    def next(self):
        while self._offset < len(self._text):
            # Find start of next word
            while self._offset < len(self._text) and self._text[self._offset].isspace():
                self._offset += 1
            sPos = self._offset

            # Find end of word
            while (
                self._offset < len(self._text)
                and not self._text[self._offset].isspace()
            ):
                self._offset += 1
            ePos = self._offset

            # Strip chars from front of word
            while sPos < len(self._text) and self._text[sPos] in self.strip_from_start:
                sPos += 1

            # Strip chars from end of word
            while ePos > 0 and self._text[ePos - 1] in self.strip_from_end:
                ePos -= 1

            # Return if word isn't empty
            if sPos < ePos:
                return self._text[sPos:ePos]

        raise StopIteration()


class ForwardSlashChunker:
    """
    This chunker allows splitting words like 'before/after' into 'before' and 'after'
    """

    # pylint: disable=R0201
    def split(self, token):
        return token.split("/")


class EnglishWordFilter:
    _pattern = re.compile(r"^[a-zA-Z'/\-]+$")

    def skip(self, token):
        return not bool(self._pattern.match(token))


class CamelCasedWordsFilter:
    r"""Filter skipping over camelCasedWords.
    This filter skips any words matching the following regular expression:

        ^([a-z]\w+[A-Z]+\w+)

    That is, any words that are camelCasedWords.
    """
    _pattern = re.compile(r"^([a-z]+([\d]|[A-Z])(?:\w+)?)")

    def skip(self, word):
        return bool(self._pattern.match(word))


class WikiWordFilter:
    r"""Filter skipping over WikiWords.
    This filter skips any words matching the following regular expression:

        ^([A-Z]\w+[A-Z]+\w+)

    That is, any words that are WikiWords.
    """
    _pattern = re.compile(r"^([A-Z]\w+[A-Z]+\w+)")

    def skip(self, word):
        return bool(self._pattern.match(word))


def get_tokenizer(filters=None, chunkers=None):
    return WordTokenizer(filters or [], chunkers or [])


def _find_dictionary(dict_name, dict_paths):
    if not dict_name or not dict_paths:
        return None

    for path in dict_paths.split(":"):
        dic = os.path.join(os.path.expanduser(path), dict_name + ".dic")
        aff = os.path.join(os.path.expanduser(path), dict_name + ".aff")
        if os.path.isfile(dic) and os.path.isfile(aff):
            return (dic, aff)

        return None


class SpellingChecker(BaseTokenChecker):
    """Check spelling in comments and docstrings"""

    __implements__ = (ITokenChecker, IAstroidChecker)
    name = "spelling"
    msgs = {
        "C0401": (
            "Wrong spelling of a word '%s' in a comment:\n%s\n%s\n%s",
            "wrong-spelling-in-comment",
            "Used when a word in comment is not spelled correctly.",
        ),
        "C0402": (
            "Wrong spelling of a word '%s' in a docstring:\n%s\n%s\n%s",
            "wrong-spelling-in-docstring",
            "Used when a word in docstring is not spelled correctly.",
        ),
    }
    options = (
        (
            "spelling-dict-name",
            {
                "default": "",
                "type": "string",
                "metavar": "<dict name>",
                "help": "Spelling dictionary name.",
            },
        ),
        (
            "spelling-dict-paths",
            {
                "default": "",
                "type": "string",
                "metavar": "<colon separated path string>",
                "help": "Paths string of directories where Hunspell dictionaries are installed.",
            },
        ),
        (
            "spelling-ignore-words",
            {
                "default": "",
                "type": "string",
                "metavar": "<comma separated words>",
                "help": "List of comma separated words that should not be checked.",
            },
        ),
        (
            "spelling-private-dict-file",
            {
                "default": "",
                "type": "string",
                "metavar": "<path to file>",
                "help": "A path to a file that contains private dictionary; one word per line.",
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

        if not hunspell:
            return
        dict_tuple = _find_dictionary(
            self.config.spelling_dict_name, self.config.spelling_dict_paths
        )
        if not dict_tuple:
            return
        self.hobj = hunspell.HunSpell(dict_tuple[0], dict_tuple[1])

        self.ignore_list = {
            w.strip() for w in self.config.spelling_ignore_words.split(",")
        }
        # "param" appears in docstring in param description and
        # "pylint" appears in comments in pylint pragmas.
        self.ignore_list.update(["param", "pylint"])

        # Expand tilde to allow e.g. spelling-private-dict-file = ~/.pylintdict
        if self.config.spelling_private_dict_file:
            # TODO if/once hunspell starts supporting adding hunspell "personal" dicts
            #      using hobj.add_dic, refactor this to support that API
            self.private_dict_file = open(
                os.path.expanduser(self.config.spelling_private_dict_file), "a+"
            )
            self.private_dict_file.seek(0)
            for line in self.private_dict_file.read().splitlines():
                self.ignore_list.add(line)

        if self.config.spelling_store_unknown_words:
            self.unknown_words = set()

        self.tokenizer = get_tokenizer(
            filters=[EnglishWordFilter(), WikiWordFilter(), CamelCasedWordsFilter()],
            chunkers=[ForwardSlashChunker()],
        )
        self.initialized = True

    def close(self):
        if self.private_dict_file:
            self.private_dict_file.close()

    def _check_spelling(self, msgid, line, line_num):
        for word in self.tokenizer.tokenize(line):
            # Skip words from ignore list.
            if word in self.ignore_list:
                continue

            # If it is a known word, then continue.
            # Spell check is case sensitive by default, since 'unicode' is
            # a spelling mistake, but 'Unicode' is not.
            if self.hobj.spell(word):
                continue

            # Don't raise a message if unknown words should be stored in
            # the private dict file instead.
            if self.config.spelling_store_unknown_words:
                if word not in self.unknown_words:
                    self.private_dict_file.write(word + "\n")
                    self.unknown_words.add(word)
                continue

            # Show an indicator under the occurrence of the word in the original line
            m = re.search(r"(\W|^)({})(\W|$)".format(re.escape(word)), line)
            col = m.regs[2][0]
            indicator = (" " * col) + ("^" * len(word))

            # Present up to N suggestions.
            suggestions = ""
            if self.config.max_spelling_suggestions > 0:
                suggested_words = self.hobj.suggest(word)
                del suggested_words[self.config.max_spelling_suggestions :]
                suggestions = "Did you mean: '{}'?".format(
                    "' or '".join(suggested_words)
                )

            self.add_message(
                msgid, line=line_num, args=(word, line, indicator, suggestions)
            )

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
