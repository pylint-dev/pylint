# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Checker for spelling errors in comments and docstrings."""

from __future__ import annotations

import re
import sys
import tokenize
from re import Pattern
from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseTokenChecker
from pylint.checkers.utils import only_required_for_messages

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

if TYPE_CHECKING:
    from pylint.lint import PyLinter

try:
    import enchant
    from enchant.tokenize import (
        Chunker,
        EmailFilter,
        Filter,
        URLFilter,
        WikiWordFilter,
        get_tokenizer,
    )
except ImportError:
    enchant = None

    class EmailFilter:  # type: ignore[no-redef]
        ...

    class URLFilter:  # type: ignore[no-redef]
        ...

    class WikiWordFilter:  # type: ignore[no-redef]
        ...

    class Filter:  # type: ignore[no-redef]
        def _skip(self, word: str) -> bool:
            raise NotImplementedError

    class Chunker:  # type: ignore[no-redef]
        pass

    def get_tokenizer(
        tag: str | None = None,
        chunkers: list[Chunker] | None = None,
        filters: list[Filter] | None = None,
    ):  # pylint: disable=unused-argument
        return Filter()


if enchant is not None:
    br = enchant.Broker()
    dicts = br.list_dicts()
    dict_choices = [""] + [d[0] for d in dicts]
    dicts = [f"{d[0]} ({d[1].name})" for d in dicts]
    dicts = ", ".join(dicts)
    instr = ""
else:
    dicts = "none"
    dict_choices = [""]
    instr = " To make it work, install the 'python-enchant' package."


class WordsWithDigitsFilter(Filter):
    """Skips words with digits."""

    def _skip(self, word: str) -> bool:
        return any(char.isdigit() for char in word)


class WordsWithUnderscores(Filter):
    """Skips words with underscores.

    They are probably function parameter names.
    """

    def _skip(self, word: str) -> bool:
        return "_" in word


class RegExFilter(Filter):
    """Parent class for filters using regular expressions.

    This filter skips any words the match the expression
    assigned to the class attribute ``_pattern``.
    """

    _pattern: Pattern[str]

    def _skip(self, word: str) -> bool:
        return bool(self._pattern.match(word))


class CamelCasedWord(RegExFilter):
    r"""Filter skipping over camelCasedWords.
    This filter skips any words matching the following regular expression:

           ^([a-z]\w+[A-Z]+\w+)

    That is, any words that are camelCasedWords.
    """
    _pattern = re.compile(r"^([a-z]+(\d|[A-Z])(?:\w+)?)")


class SphinxDirectives(RegExFilter):
    r"""Filter skipping over Sphinx Directives.
    This filter skips any words matching the following regular expression:

           ^(:([a-z]+)){1,2}:`([^`]+)(`)?

    That is, for example, :class:`BaseQuery`
    """
    # The final ` in the pattern is optional because enchant strips it out
    _pattern = re.compile(r"^(:([a-z]+)){1,2}:`([^`]+)(`)?")


class ForwardSlashChunker(Chunker):
    """This chunker allows splitting words like 'before/after' into 'before' and
    'after'.
    """

    def next(self):
        while True:
            if not self._text:
                raise StopIteration()
            if "/" not in self._text:
                text = self._text
                self._offset = 0
                self._text = ""
                return text, 0
            pre_text, post_text = self._text.split("/", 1)
            self._text = post_text
            self._offset = 0
            if (
                not pre_text
                or not post_text
                or not pre_text[-1].isalpha()
                or not post_text[0].isalpha()
            ):
                self._text = ""
                self._offset = 0
                return f"{pre_text}/{post_text}", 0
            return pre_text, 0

    def _next(self) -> tuple[str, Literal[0]]:
        while True:
            if "/" not in self._text:
                return self._text, 0
            pre_text, post_text = self._text.split("/", 1)
            if not pre_text or not post_text:
                break
            if not pre_text[-1].isalpha() or not post_text[0].isalpha():
                raise StopIteration()
            self._text = pre_text + " " + post_text
        raise StopIteration()


CODE_FLANKED_IN_BACKTICK_REGEX = re.compile(r"(\s|^)(`{1,2})([^`]+)(\2)([^`]|$)")
MYPY_IGNORE_DIRECTIVE_RULE_REGEX = re.compile(r"(\s|^)(type\: ignore\[[^\]]+\])(.*)")


def _strip_code_flanked_in_backticks(line: str) -> str:
    """Alter line so code flanked in back-ticks is ignored.

    Pyenchant automatically strips back-ticks when parsing tokens,
    so this cannot be done at the individual filter level.
    """

    def replace_code_but_leave_surrounding_characters(match_obj: re.Match[str]) -> str:
        return match_obj.group(1) + match_obj.group(5)

    return CODE_FLANKED_IN_BACKTICK_REGEX.sub(
        replace_code_but_leave_surrounding_characters, line
    )


def _strip_mypy_ignore_directive_rule(line: str) -> str:
    """Alter line so mypy rule name is ignored.

    Pyenchant parses anything flanked by spaces as an individual token,
    so this cannot be done at the individual filter level.
    """

    def replace_rule_name_but_leave_surrounding_characters(
        match_obj: re.Match[str],
    ) -> str:
        return match_obj.group(1) + match_obj.group(3)

    return MYPY_IGNORE_DIRECTIVE_RULE_REGEX.sub(
        replace_rule_name_but_leave_surrounding_characters, line
    )


class SpellingChecker(BaseTokenChecker):
    """Check spelling in comments and docstrings."""

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
            "Used when a word in docstring cannot be checked by enchant.",
        ),
    }
    options = (
        (
            "spelling-dict",
            {
                "default": "",
                "type": "choice",
                "metavar": "<dict name>",
                "choices": dict_choices,
                "help": "Spelling dictionary name. "
                f"Available dictionaries: {dicts}.{instr}",
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
                "type": "path",
                "metavar": "<path to file>",
                "help": "A path to a file that contains the private "
                "dictionary; one word per line.",
            },
        ),
        (
            "spelling-store-unknown-words",
            {
                "default": "n",
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Tells whether to store unknown words to the "
                "private dictionary (see the "
                "--spelling-private-dict-file option) instead of "
                "raising a message.",
            },
        ),
        (
            "max-spelling-suggestions",
            {
                "default": 4,
                "type": "int",
                "metavar": "N",
                "help": "Limits count of emitted suggestions for spelling mistakes.",
            },
        ),
        (
            "spelling-ignore-comment-directives",
            {
                "default": "fmt: on,fmt: off,noqa:,noqa,nosec,isort:skip,mypy:",
                "type": "string",
                "metavar": "<comma separated words>",
                "help": "List of comma separated words that should be considered "
                "directives if they appear at the beginning of a comment "
                "and should not be checked.",
            },
        ),
    )

    def open(self) -> None:
        self.initialized = False
        if enchant is None:
            return
        dict_name = self.linter.config.spelling_dict
        if not dict_name:
            return

        self.ignore_list = [
            w.strip() for w in self.linter.config.spelling_ignore_words.split(",")
        ]
        # "param" appears in docstring in param description and
        # "pylint" appears in comments in pylint pragmas.
        self.ignore_list.extend(["param", "pylint"])

        self.ignore_comment_directive_list = [
            w.strip()
            for w in self.linter.config.spelling_ignore_comment_directives.split(",")
        ]

        if self.linter.config.spelling_private_dict_file:
            self.spelling_dict = enchant.DictWithPWL(
                dict_name, self.linter.config.spelling_private_dict_file
            )
        else:
            self.spelling_dict = enchant.Dict(dict_name)

        if self.linter.config.spelling_store_unknown_words:
            self.unknown_words: set[str] = set()

        self.tokenizer = get_tokenizer(
            dict_name,
            chunkers=[ForwardSlashChunker],
            filters=[
                EmailFilter,
                URLFilter,
                WikiWordFilter,
                WordsWithDigitsFilter,
                WordsWithUnderscores,
                CamelCasedWord,
                SphinxDirectives,
            ],
        )
        self.initialized = True

    def _check_spelling(self, msgid: str, line: str, line_num: int) -> None:
        original_line = line
        try:
            # The mypy warning is caught by the except statement
            initial_space = re.search(r"^\s+", line).regs[0][1]  # type: ignore[union-attr]
        except (IndexError, AttributeError):
            initial_space = 0
        if line.strip().startswith("#") and "docstring" not in msgid:
            line = line.strip()[1:]
            # A ``Filter`` cannot determine if the directive is at the beginning of a line,
            #   nor determine if a colon is present or not (``pyenchant`` strips trailing colons).
            #   So implementing this here.
            for iter_directive in self.ignore_comment_directive_list:
                if line.startswith(" " + iter_directive):
                    line = line[(len(iter_directive) + 1) :]
                    break
            starts_with_comment = True
        else:
            starts_with_comment = False

        line = _strip_code_flanked_in_backticks(line)
        line = _strip_mypy_ignore_directive_rule(line)

        for word, word_start_at in self.tokenizer(line.strip()):
            word_start_at += initial_space
            lower_cased_word = word.casefold()

            # Skip words from ignore list.
            if word in self.ignore_list or lower_cased_word in self.ignore_list:
                continue

            # Strip starting u' from unicode literals and r' from raw strings.
            if word.startswith(("u'", 'u"', "r'", 'r"')) and len(word) > 2:
                word = word[2:]
                lower_cased_word = lower_cased_word[2:]

            # If it is a known word, then continue.
            try:
                if self.spelling_dict.check(lower_cased_word):
                    # The lower cased version of word passed spell checking
                    continue

                # If we reached this far, it means there was a spelling mistake.
                # Let's retry with the original work because 'unicode' is a
                # spelling mistake but 'Unicode' is not
                if self.spelling_dict.check(word):
                    continue
            except enchant.errors.Error:
                self.add_message(
                    "invalid-characters-in-docstring", line=line_num, args=(word,)
                )
                continue

            # Store word to private dict or raise a message.
            if self.linter.config.spelling_store_unknown_words:
                if lower_cased_word not in self.unknown_words:
                    with open(
                        self.linter.config.spelling_private_dict_file,
                        "a",
                        encoding="utf-8",
                    ) as f:
                        f.write(f"{lower_cased_word}\n")
                    self.unknown_words.add(lower_cased_word)
            else:
                # Present up to N suggestions.
                suggestions = self.spelling_dict.suggest(word)
                del suggestions[self.linter.config.max_spelling_suggestions :]
                line_segment = line[word_start_at:]
                match = re.search(rf"(\W|^)({word})(\W|$)", line_segment)
                if match:
                    # Start position of second group in regex.
                    col = match.regs[2][0]
                else:
                    col = line_segment.index(word)
                col += word_start_at
                if starts_with_comment:
                    col += 1
                indicator = (" " * col) + ("^" * len(word))
                all_suggestion = "' or '".join(suggestions)
                args = (word, original_line, indicator, f"'{all_suggestion}'")
                self.add_message(msgid, line=line_num, args=args)

    def process_tokens(self, tokens: list[tokenize.TokenInfo]) -> None:
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

    @only_required_for_messages("wrong-spelling-in-docstring")
    def visit_module(self, node: nodes.Module) -> None:
        self._check_docstring(node)

    @only_required_for_messages("wrong-spelling-in-docstring")
    def visit_classdef(self, node: nodes.ClassDef) -> None:
        self._check_docstring(node)

    @only_required_for_messages("wrong-spelling-in-docstring")
    def visit_functiondef(
        self, node: nodes.FunctionDef | nodes.AsyncFunctionDef
    ) -> None:
        self._check_docstring(node)

    visit_asyncfunctiondef = visit_functiondef

    def _check_docstring(
        self,
        node: nodes.FunctionDef
        | nodes.AsyncFunctionDef
        | nodes.ClassDef
        | nodes.Module,
    ) -> None:
        """Check if the node has any spelling errors."""
        if not self.initialized:
            return
        if not node.doc_node:
            return
        start_line = node.lineno + 1
        # Go through lines of docstring
        for idx, line in enumerate(node.doc_node.value.splitlines()):
            self._check_spelling("wrong-spelling-in-docstring", line, start_line + idx)


def register(linter: PyLinter) -> None:
    linter.register_checker(SpellingChecker(linter))
