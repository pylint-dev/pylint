# Copyright (c) 2014-2016 Claudiu Popa <pcmanticore@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unittest for the spelling checker."""

import pytest

import astroid

from pylint.checkers import spelling
from pylint.testutils import CheckerTestCase, Message, set_config, tokenize_str

# try to create enchant dictionary
try:
    import enchant
except ImportError:
    enchant = None

spell_dict = None
if enchant is not None:
    try:
        enchant.Dict("en_US")
        spell_dict = "en_US"
    except enchant.DictNotFoundError:
        pass


class TestSpellingChecker(CheckerTestCase):
    CHECKER_CLASS = spelling.SpellingChecker

    @pytest.mark.skipif(spell_dict is None,
                        reason="missing python-enchant package or missing "
                        "spelling dictionaries")
    @set_config(spelling_dict=spell_dict)
    def test_check_bad_coment(self):
        try:
            with self.assertAddsMessages(
                Message('wrong-spelling-in-comment', line=1,
                        args=('coment', '# bad coment',
                              '      ^^^^^^',
                              "comet' or 'comment' or 'moment' or 'foment"))):
                self.checker.process_tokens(tokenize_str("# bad coment"))
        except AssertionError:
            # In Arch Linux, at least, the suggestions do not match
            with self.assertAddsMessages(
                Message('wrong-spelling-in-comment', line=1,
                        args=('coment', '# bad coment',
                              '      ^^^^^^',
                              "comet' or 'comment' or 'cement' or 'cogent"))):
                self.checker.process_tokens(tokenize_str("# bad coment"))

    @pytest.mark.skipif(spell_dict is None,
                        reason="missing python-enchant package or missing "
                        "spelling dictionaries")
    @set_config(spelling_dict=spell_dict)
    def test_check_bad_docstring(self):
        stmt = astroid.extract_node(
            'def fff():\n   """bad coment"""\n   pass')
        try:
            with self.assertAddsMessages(
                Message('wrong-spelling-in-docstring', line=2,
                        args=('coment', 'bad coment',
                              '    ^^^^^^',
                              "comet' or 'comment' or 'moment' or 'foment"))):
                self.checker.visit_functiondef(stmt)
        except AssertionError:
            # In Arch Linux, at least, the suggestions do not match
            with self.assertAddsMessages(
                Message('wrong-spelling-in-docstring', line=2,
                        args=('coment', 'bad coment',
                              '    ^^^^^^',
                              "comet' or 'comment' or 'cement' or 'cogent"))):
                self.checker.visit_functiondef(stmt)

        stmt = astroid.extract_node(
            'class Abc(object):\n   """bad coment"""\n   pass')
        try:
            with self.assertAddsMessages(
                Message('wrong-spelling-in-docstring', line=2,
                        args=('coment', 'bad coment',
                              '    ^^^^^^',
                              "comet' or 'comment' or 'moment' or 'foment"))):
                self.checker.visit_classdef(stmt)
        except AssertionError:
            # In Arch Linux, at least, the suggestions do not match
            with self.assertAddsMessages(
                Message('wrong-spelling-in-docstring', line=2,
                        args=('coment', 'bad coment',
                              '    ^^^^^^',
                              "comet' or 'comment' or 'cement' or 'cogent"))):
                self.checker.visit_classdef(stmt)

    @pytest.mark.skipif(spell_dict is None,
                        reason="missing python-enchant package or missing "
                        "spelling dictionaries")
    @set_config(spelling_dict=spell_dict)
    def test_invalid_docstring_characters(self):
        stmt = astroid.extract_node(
            'def fff():\n   """test\\x00"""\n   pass')
        with self.assertAddsMessages(
            Message('invalid-characters-in-docstring', line=2,
                    args=('test\x00',))):
            self.checker.visit_functiondef(stmt)

    @pytest.mark.skipif(spell_dict is None,
                        reason="missing python-enchant package or missing "
                        "spelling dictionaries")
    @set_config(spelling_dict=spell_dict)
    def test_skip_shebangs(self):
        self.checker.process_tokens(tokenize_str('#!/usr/bin/env python'))
        assert self.linter.release_messages() == []

    @pytest.mark.skipif(spell_dict is None,
                        reason="missing python-enchant package or missing "
                        "spelling dictionaries")
    @set_config(spelling_dict=spell_dict)
    def test_skip_python_coding_comments(self):
        self.checker.process_tokens(tokenize_str(
            '# -*- coding: utf-8 -*-'))
        assert self.linter.release_messages() == []
        self.checker.process_tokens(tokenize_str(
            '# coding=utf-8'))
        assert self.linter.release_messages() == []
        self.checker.process_tokens(tokenize_str(
            '# vim: set fileencoding=utf-8 :'))
        assert self.linter.release_messages() == []
        # Now with a shebang first
        self.checker.process_tokens(tokenize_str(
            '#!/usr/bin/env python\n# -*- coding: utf-8 -*-'))
        assert self.linter.release_messages() == []
        self.checker.process_tokens(tokenize_str(
            '#!/usr/bin/env python\n# coding=utf-8'))
        assert self.linter.release_messages() == []
        self.checker.process_tokens(tokenize_str(
            '#!/usr/bin/env python\n# vim: set fileencoding=utf-8 :'))
        assert self.linter.release_messages() == []
        # Howerver, if not found on the first 2 lines...
        with self.assertAddsMessages(
            Message('wrong-spelling-in-comment', line=3,
                    args=('fileencoding',
                          '# vim: set fileencoding=utf-8 :',
                          '           ^^^^^^^^^^^^',
                          "file encoding' or 'file-encoding' or 'filigreeing")),
            Message('wrong-spelling-in-comment', line=3,
                    args=('utf',
                          '# vim: set fileencoding=utf-8 :',
                          '                        ^^^',
                          "fut' or 'uhf"))):
            self.checker.process_tokens(tokenize_str(
                '# Line 1\n# Line 2\n# vim: set fileencoding=utf-8 :'))

    @pytest.mark.skipif(spell_dict is None,
                        reason="missing python-enchant package or missing "
                        "spelling dictionaries")
    @set_config(spelling_dict=spell_dict)
    def test_skip_top_level_pylint_enable_disable_comments(self):
        self.checker.process_tokens(tokenize_str('# Line 1\n Line 2\n# pylint: disable=ungrouped-imports'))
        assert self.linter.release_messages() == []
