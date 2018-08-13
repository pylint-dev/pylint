# -*- coding: utf-8 -*-
# Copyright (c) 2014-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Michal Nowikowski <godfryd@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2017 Pedro Algarvio <pedro@algarvio.me>
# Copyright (c) 2017 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2018 Anthony Sottile <asottile@umich.edu>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unittest for the spelling checker."""

import pytest

import astroid

from pylint.checkers import spelling
from pylint.testutils import CheckerTestCase, Message, set_config, _tokenize_str

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

    skip_on_missing_package_or_dict = pytest.mark.skipif(
        spell_dict is None,
        reason="missing python-enchant package or missing spelling dictionaries")

    def _get_msg_suggestions(self, word, count=4):
        return "'{}'".format("' or '".join(self.checker.spelling_dict.suggest(word)[:count]))

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_check_bad_coment(self):
        with self.assertAddsMessages(
            Message('wrong-spelling-in-comment', line=1,
                    args=('coment', '# bad coment',
                          '      ^^^^^^',
                          self._get_msg_suggestions('coment')))):
            self.checker.process_tokens(_tokenize_str("# bad coment"))

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    @set_config(max_spelling_suggestions=2)
    def test_check_bad_coment_custom_suggestion_count(self):
        with self.assertAddsMessages(
            Message('wrong-spelling-in-comment', line=1,
                    args=('coment', '# bad coment',
                          '      ^^^^^^',
                          self._get_msg_suggestions('coment', count=2)))):
            self.checker.process_tokens(_tokenize_str("# bad coment"))

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_check_bad_docstring(self):
        stmt = astroid.extract_node(
            'def fff():\n   """bad coment"""\n   pass')
        with self.assertAddsMessages(
            Message('wrong-spelling-in-docstring', line=2,
                    args=('coment', 'bad coment',
                          '    ^^^^^^',
                          self._get_msg_suggestions('coment')))):
            self.checker.visit_functiondef(stmt)

        stmt = astroid.extract_node(
            'class Abc(object):\n   """bad coment"""\n   pass')
        with self.assertAddsMessages(
            Message('wrong-spelling-in-docstring', line=2,
                    args=('coment', 'bad coment',
                          '    ^^^^^^',
                          self._get_msg_suggestions('coment')))):
            self.checker.visit_classdef(stmt)

    @pytest.mark.skipif(True, reason='pyenchant\'s tokenizer strips these')
    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_invalid_docstring_characters(self):
        stmt = astroid.extract_node(
            'def fff():\n   """test\\x00"""\n   pass')
        with self.assertAddsMessages(
            Message('invalid-characters-in-docstring', line=2,
                    args=('test\x00',))):
            self.checker.visit_functiondef(stmt)

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_shebangs(self):
        self.checker.process_tokens(_tokenize_str('#!/usr/bin/env python'))
        assert self.linter.release_messages() == []

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_python_coding_comments(self):
        self.checker.process_tokens(_tokenize_str(
            '# -*- coding: utf-8 -*-'))
        assert self.linter.release_messages() == []
        self.checker.process_tokens(_tokenize_str(
            '# coding=utf-8'))
        assert self.linter.release_messages() == []
        self.checker.process_tokens(_tokenize_str(
            '# vim: set fileencoding=utf-8 :'))
        assert self.linter.release_messages() == []
        # Now with a shebang first
        self.checker.process_tokens(_tokenize_str(
            '#!/usr/bin/env python\n# -*- coding: utf-8 -*-'))
        assert self.linter.release_messages() == []
        self.checker.process_tokens(_tokenize_str(
            '#!/usr/bin/env python\n# coding=utf-8'))
        assert self.linter.release_messages() == []
        self.checker.process_tokens(_tokenize_str(
            '#!/usr/bin/env python\n# vim: set fileencoding=utf-8 :'))
        assert self.linter.release_messages() == []

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_top_level_pylint_enable_disable_comments(self):
        self.checker.process_tokens(_tokenize_str('# Line 1\n Line 2\n# pylint: disable=ungrouped-imports'))
        assert self.linter.release_messages() == []

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_words_with_numbers(self):
        self.checker.process_tokens(_tokenize_str('\n# 0ne\n# Thr33\n# Sh3ll'))
        assert self.linter.release_messages() == []

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_wiki_words(self):
        stmt = astroid.extract_node(
            'class ComentAbc(object):\n   """ComentAbc with a bad coment"""\n   pass')
        with self.assertAddsMessages(
            Message('wrong-spelling-in-docstring', line=2,
                    args=('coment', 'ComentAbc with a bad coment',
                          '                     ^^^^^^',
                          self._get_msg_suggestions('coment')))):
            self.checker.visit_classdef(stmt)

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_camel_cased_words(self):
        stmt = astroid.extract_node(
            'class ComentAbc(object):\n   """comentAbc with a bad coment"""\n   pass')
        with self.assertAddsMessages(
            Message('wrong-spelling-in-docstring', line=2,
                    args=('coment', 'comentAbc with a bad coment',
                          '                     ^^^^^^',
                          self._get_msg_suggestions('coment')))):
            self.checker.visit_classdef(stmt)

        # With just a single upper case letter in the end
        stmt = astroid.extract_node(
            'class ComentAbc(object):\n   """argumentN with a bad coment"""\n   pass')
        with self.assertAddsMessages(
            Message('wrong-spelling-in-docstring', line=2,
                    args=('coment', 'argumentN with a bad coment',
                          '                     ^^^^^^',
                          self._get_msg_suggestions('coment')))):
            self.checker.visit_classdef(stmt)

        for ccn in ('xmlHttpRequest', 'newCustomer', 'newCustomerId',
                    'innerStopwatch', 'supportsIpv6OnIos', 'affine3D'):
            stmt = astroid.extract_node(
                'class TestClass(object):\n   """{} comment"""\n   pass'.format(ccn))
            self.checker.visit_classdef(stmt)
            assert self.linter.release_messages() == []

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_words_with_underscores(self):
        stmt = astroid.extract_node(
            'def fff(param_name):\n   """test param_name"""\n   pass')
        self.checker.visit_functiondef(stmt)
        assert self.linter.release_messages() == []

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_email_address(self):
        self.checker.process_tokens(_tokenize_str('# uname@domain.tld'))
        assert self.linter.release_messages() == []

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_urls(self):
        self.checker.process_tokens(_tokenize_str('# https://github.com/rfk/pyenchant'))
        assert self.linter.release_messages() == []

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_sphinx_directives(self):
        stmt = astroid.extract_node(
                'class ComentAbc(object):\n   """This is :class:`ComentAbc` with a bad coment"""\n   pass')
        with self.assertAddsMessages(
            Message('wrong-spelling-in-docstring', line=2,
                    args=('coment', 'This is :class:`ComentAbc` with a bad coment',
                          '                                      ^^^^^^',
                          self._get_msg_suggestions('coment')))):
            self.checker.visit_classdef(stmt)

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_handle_words_joined_by_forward_slash(self):
        stmt = astroid.extract_node('''
        class ComentAbc(object):
            """This is Comment/Abcz with a bad comment"""
            pass
        ''')
        with self.assertAddsMessages(
            Message('wrong-spelling-in-docstring', line=3,
                    args=('Abcz', 'This is Comment/Abcz with a bad comment',
                          '                ^^^^',
                          self._get_msg_suggestions('Abcz')))):
            self.checker.visit_classdef(stmt)
