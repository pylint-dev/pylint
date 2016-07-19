# Copyright (c) 2003-2016 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unittest for the spelling checker."""

import unittest

from astroid import test_utils

from pylint.checkers import spelling
from pylint.testutils import (
    CheckerTestCase, Message, set_config, tokenize_str,
)

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


class SpellingCheckerTest(CheckerTestCase):
    CHECKER_CLASS = spelling.SpellingChecker

    @unittest.skipIf(spell_dict is None,
                     "missing python-enchant package or missing "
                     "spelling dictionaries")
    @set_config(spelling_dict=spell_dict)
    def test_check_bad_coment(self):
        with self.assertAddsMessages(
            Message('wrong-spelling-in-comment', line=1,
                    args=('coment', '# bad coment',
                          '      ^^^^^^',
                          "comet' or 'comment' or 'moment' or 'foment"))):
            self.checker.process_tokens(tokenize_str("# bad coment"))

    @unittest.skipIf(spell_dict is None,
                     "missing python-enchant package or missing "
                     "spelling dictionaries")
    @set_config(spelling_dict=spell_dict)
    def test_check_bad_docstring(self):
        stmt = test_utils.extract_node(
            'def fff():\n   """bad coment"""\n   pass')
        with self.assertAddsMessages(
            Message('wrong-spelling-in-docstring', line=2,
                    args=('coment', 'bad coment',
                          '    ^^^^^^',
                          "comet' or 'comment' or 'moment' or 'foment"))):
            self.checker.visit_functiondef(stmt)

        stmt = test_utils.extract_node(
            'class Abc(object):\n   """bad coment"""\n   pass')
        with self.assertAddsMessages(
            Message('wrong-spelling-in-docstring', line=2,
                    args=('coment', 'bad coment',
                          '    ^^^^^^',
                          "comet' or 'comment' or 'moment' or 'foment"))):
            self.checker.visit_classdef(stmt)

    @unittest.skipIf(spell_dict is None,
                     "missing python-enchant package or missing "
                     "spelling dictionaries")
    @set_config(spelling_dict=spell_dict)
    def test_invalid_docstring_characters(self):
        stmt = test_utils.extract_node(
            'def fff():\n   """test\\x00"""\n   pass')
        with self.assertAddsMessages(
            Message('invalid-characters-in-docstring', line=2,
                    args=('test\x00',))):
            self.checker.visit_functiondef(stmt)


if __name__ == '__main__':
    unittest.main()
