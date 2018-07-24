# -*- coding: utf-8 -*-
# Copyright (c) 2009-2011, 2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2012 FELD Boris <lothiraldan@gmail.com>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2014-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 buck <buck.2019@gmail.com>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Harut <yes@harutune.name>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Petr Pulc <petrpulc@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2017 Krzysztof Czapla <k.czapla68@gmail.com>
# Copyright (c) 2017 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2017 James M. Allen <james.m.allen@gmail.com>
# Copyright (c) 2017 vinnyrose <vinnyrose@users.noreply.github.com>
# Copyright (c) 2018 Bryce Guinta <bryce.guinta@protonmail.com>
# Copyright (c) 2018 Bryce Guinta <bryce.paul.guinta@gmail.com>
# Copyright (c) 2018 Anthony Sottile <asottile@umich.edu>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Check format checker helper functions"""

from __future__ import unicode_literals

import tokenize
import os
import tempfile

import astroid

from pylint.checkers.format import *
from pylint import reporters
from pylint import lint


from pylint.testutils import (
    CheckerTestCase, Message, set_config, _tokenize_str,
)


class TestMultiStatementLine(CheckerTestCase):
    CHECKER_CLASS = FormatChecker

    def testSingleLineIfStmts(self):
        stmt = astroid.extract_node("""
        if True: pass  #@
        """)
        self.checker.config.single_line_if_stmt = False
        with self.assertAddsMessages(Message('multiple-statements', node=stmt.body[0])):
            self.visitFirst(stmt)
        self.checker.config.single_line_if_stmt = True
        with self.assertNoMessages():
            self.visitFirst(stmt)
        stmt = astroid.extract_node("""
        if True: pass  #@
        else:
            pass
        """)
        with self.assertAddsMessages(Message('multiple-statements', node=stmt.body[0])):
            self.visitFirst(stmt)

    def testSingleLineClassStmts(self):
        stmt = astroid.extract_node("""
        class MyError(Exception): pass  #@
        """)
        self.checker.config.single_line_class_stmt = False
        with self.assertAddsMessages(Message('multiple-statements', node=stmt.body[0])):
            self.visitFirst(stmt)
        self.checker.config.single_line_class_stmt = True
        with self.assertNoMessages():
            self.visitFirst(stmt)

        stmt = astroid.extract_node("""
        class MyError(Exception): a='a'  #@
        """)
        self.checker.config.single_line_class_stmt = False
        with self.assertAddsMessages(Message('multiple-statements', node=stmt.body[0])):
            self.visitFirst(stmt)
        self.checker.config.single_line_class_stmt = True
        with self.assertNoMessages():
            self.visitFirst(stmt)

        stmt = astroid.extract_node("""
        class MyError(Exception): a='a'; b='b'  #@
        """)
        self.checker.config.single_line_class_stmt = False
        with self.assertAddsMessages(Message('multiple-statements', node=stmt.body[0])):
            self.visitFirst(stmt)
        self.checker.config.single_line_class_stmt = True
        with self.assertAddsMessages(Message('multiple-statements', node=stmt.body[0])):
            self.visitFirst(stmt)

    def testTryExceptFinallyNoMultipleStatement(self):
        tree = astroid.extract_node("""
        try:  #@
            pass
        except:
            pass
        finally:
            pass""")
        with self.assertNoMessages():
            self.visitFirst(tree)

    def visitFirst(self, tree):
        self.checker.process_tokens([])
        self.checker.visit_default(tree.body[0])


class TestSuperfluousParentheses(CheckerTestCase):
    CHECKER_CLASS = FormatChecker

    def testCheckKeywordParensHandlesValidCases(self):
        self.checker._keywords_with_parens = set()
        cases = [
            'if foo:',
            'if foo():',
            'if (x and y) or z:',
            'assert foo()',
            'assert ()',
            'if (1, 2) in (3, 4):',
            'if (a or b) in c:',
            'return (x for x in x)',
            'if (x for x in x):',
            'for x in (x for x in x):',
            'not (foo or bar)',
            'not (foo or bar) and baz',
            ]
        with self.assertNoMessages():
            for code in cases:
                self.checker._check_keyword_parentheses(_tokenize_str(code), 0)

    def testCheckKeywordParensHandlesUnnecessaryParens(self):
        self.checker._keywords_with_parens = set()
        cases = [
            (Message('superfluous-parens', line=1, args='if'),
             'if (foo):', 0),
            (Message('superfluous-parens', line=1, args='if'),
             'if ((foo, bar)):', 0),
            (Message('superfluous-parens', line=1, args='if'),
             'if (foo(bar)):', 0),
            (Message('superfluous-parens', line=1, args='return'),
             'return ((x for x in x))', 0),
            (Message('superfluous-parens', line=1, args='not'),
             'not (foo)', 0),
            (Message('superfluous-parens', line=1, args='not'),
             'if not (foo):', 1),
            (Message('superfluous-parens', line=1, args='if'),
             'if (not (foo)):', 0),
            (Message('superfluous-parens', line=1, args='not'),
             'if (not (foo)):', 2),
            (Message('superfluous-parens', line=1, args='for'),
             'for (x) in (1, 2, 3):', 0),
            (Message('superfluous-parens', line=1, args='if'),
             'if (1) in (1, 2, 3):', 0),
            ]
        for msg, code, offset in cases:
            with self.assertAddsMessages(msg):
                self.checker._check_keyword_parentheses(_tokenize_str(code), offset)

    def testCheckIfArgsAreNotUnicode(self):
        self.checker._keywords_with_parens = set()
        cases = [('if (foo):', 0), ('assert (1 == 1)', 0)]

        for code, offset in cases:
            self.checker._check_keyword_parentheses(_tokenize_str(code), offset)
            got = self.linter.release_messages()
            assert isinstance(got[-1].args, str)


    def testFuturePrintStatementWithoutParensWarning(self):
        code = """from __future__ import print_function
print('Hello world!')
"""
        tree = astroid.parse(code)
        with self.assertNoMessages():
            self.checker.process_module(tree)
            self.checker.process_tokens(_tokenize_str(code))

    def testKeywordParensFalsePositive(self):
        self.checker._keywords_with_parens = set()
        code = "if 'bar' in (DICT or {}):"
        with self.assertNoMessages():
            self.checker._check_keyword_parentheses(_tokenize_str(code), start=2)


class TestCheckSpace(CheckerTestCase):
    CHECKER_CLASS = FormatChecker

    def testParenthesesGood(self):
        good_cases = [
            '(a)\n',
            '(a * (b + c))\n',
            '(#\n    a)\n',
            ]
        with self.assertNoMessages():
            for code in good_cases:
                self.checker.process_tokens(_tokenize_str(code))

    def testParenthesesBad(self):
        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('No', 'allowed', 'after', 'bracket', '( a)\n^'))):
            self.checker.process_tokens(_tokenize_str('( a)\n'))

        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('No', 'allowed', 'before', 'bracket', '(a )\n   ^'))):
            self.checker.process_tokens(_tokenize_str('(a )\n'))

        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('No', 'allowed', 'before', 'bracket', 'foo (a)\n    ^'))):
            self.checker.process_tokens(_tokenize_str('foo (a)\n'))

        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('No', 'allowed', 'before', 'bracket', '{1: 2} [1]\n       ^'))):
            self.checker.process_tokens(_tokenize_str('{1: 2} [1]\n'))

    def testTrailingCommaGood(self):
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('(a, )\n'))
            self.checker.process_tokens(_tokenize_str('(a,)\n'))

        self.checker.config.no_space_check = []
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('(a,)\n'))

    @set_config(no_space_check=[])
    def testTrailingCommaBad(self):
        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('No', 'allowed', 'before', 'bracket', '(a, )\n    ^'))):
            self.checker.process_tokens(_tokenize_str('(a, )\n'))

    def testComma(self):
        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('No', 'allowed', 'before', 'comma', '(a , b)\n   ^'))):
            self.checker.process_tokens(_tokenize_str('(a , b)\n'))

    def testSpacesAllowedInsideSlices(self):
        good_cases = [
            '[a:b]\n',
            '[a : b]\n',
            '[a : ]\n',
            '[:a]\n',
            '[:]\n',
            '[::]\n',
            ]
        with self.assertNoMessages():
            for code in good_cases:
                self.checker.process_tokens(_tokenize_str(code))

    def testKeywordSpacingGood(self):
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('foo(foo=bar)\n'))
            self.checker.process_tokens(_tokenize_str('foo(foo: int = bar)\n'))
            self.checker.process_tokens(_tokenize_str('foo(foo: module.classname = bar)\n'))
            self.checker.process_tokens(_tokenize_str('foo(foo: Dict[int, str] = bar)\n'))
            self.checker.process_tokens(_tokenize_str('foo(foo: \'int\' = bar)\n'))
            self.checker.process_tokens(_tokenize_str('foo(foo: Dict[int, \'str\'] = bar)\n'))
            self.checker.process_tokens(_tokenize_str('lambda x=1: x\n'))

    def testKeywordSpacingBad(self):
        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('No', 'allowed', 'before', 'keyword argument assignment',
                          '(foo =bar)\n     ^'))):
            self.checker.process_tokens(_tokenize_str('(foo =bar)\n'))

        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('No', 'allowed', 'after', 'keyword argument assignment',
                          '(foo= bar)\n    ^'))):
            self.checker.process_tokens(_tokenize_str('(foo= bar)\n'))

        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('No', 'allowed', 'around', 'keyword argument assignment',
                          '(foo = bar)\n     ^'))):
            self.checker.process_tokens(_tokenize_str('(foo = bar)\n'))

        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('Exactly one', 'required', 'before', 'keyword argument assignment',
                          '(foo: int= bar)\n         ^'))):
            self.checker.process_tokens(_tokenize_str('(foo: int= bar)\n'))

        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('Exactly one', 'required', 'after', 'keyword argument assignment',
                          '(foo: int =bar)\n          ^'))):
            self.checker.process_tokens(_tokenize_str('(foo: int =bar)\n'))

        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('Exactly one', 'required', 'around', 'keyword argument assignment',
                          '(foo: int=bar)\n         ^'))):
            self.checker.process_tokens(_tokenize_str('(foo: int=bar)\n'))

        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('Exactly one', 'required', 'around', 'keyword argument assignment',
                          '(foo: List[int]=bar)\n               ^'))):
            self.checker.process_tokens(_tokenize_str('(foo: List[int]=bar)\n'))
        # Regression test for #1831
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str("(arg: Tuple[\n    int, str] = None):\n"))

    def testOperatorSpacingGood(self):
        good_cases = [
            'a = b\n'
            'a < b\n'
            'a\n< b\n',
            ]
        with self.assertNoMessages():
            for code in good_cases:
                self.checker.process_tokens(_tokenize_str(code))

    def testOperatorSpacingBad(self):
        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('Exactly one', 'required', 'before', 'comparison', 'a< b\n ^'))):
            self.checker.process_tokens(_tokenize_str('a< b\n'))

        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('Exactly one', 'required', 'after', 'comparison', 'a <b\n  ^'))):
            self.checker.process_tokens(_tokenize_str('a <b\n'))

        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('Exactly one', 'required', 'around', 'comparison', 'a<b\n ^'))):
            self.checker.process_tokens(_tokenize_str('a<b\n'))

        with self.assertAddsMessages(
            Message('bad-whitespace', line=1,
                    args=('Exactly one', 'required', 'around', 'comparison', 'a<  b\n ^'))):
            self.checker.process_tokens(_tokenize_str('a<  b\n'))

    def testValidTypingAnnotationEllipses(self):
        """Make sure ellipses in function typing annotation
        doesn't cause a false positive bad-whitespace message"""
        with self.assertNoMessages():
            self.checker.process_tokens(
                _tokenize_str('def foo(t: Tuple[str, ...] = None):\n'))

    def testEmptyLines(self):
        self.checker.config.no_space_check = []
        with self.assertAddsMessages(
            Message('trailing-whitespace', line=2)):
            self.checker.process_tokens(_tokenize_str('a = 1\n \nb = 2\n'))

        with self.assertAddsMessages(
            Message('trailing-whitespace', line=2)):
            self.checker.process_tokens(_tokenize_str('a = 1\n\t\nb = 2\n'))

        with self.assertAddsMessages(
            Message('trailing-whitespace', line=2)):
            self.checker.process_tokens(_tokenize_str('a = 1\n\v\nb = 2\n'))

        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('a = 1\n\f\nb = 2\n'))

        self.checker.config.no_space_check = ['empty-line']
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('a = 1\n \nb = 2\n'))

        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('a = 1\n\t\nb = 2\n'))

        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str('a = 1\n\v\nb = 2\n'))


    def test_encoding_token(self):
        """Make sure the encoding token doesn't change the checker's behavior

        _tokenize_str doesn't produce an encoding token, but
        reading a file does
        """
        with self.assertNoMessages():
            encoding_token = tokenize.TokenInfo(tokenize.ENCODING, "utf-8", (0, 0), (0, 0), '')
            tokens = [encoding_token] + _tokenize_str('if (\n        None):\n    pass\n')
            self.checker.process_tokens(tokens)


def test_disable_global_option_end_of_line():
    """
    Test for issue with disabling tokenizer messages
    that extend beyond the scope of the ast tokens
    """
    file_ = tempfile.NamedTemporaryFile('w', delete=False)
    with file_:
        file_.write("""
mylist = [
    None
        ]
    """)
    try:
        linter = lint.PyLinter()
        checker = FormatChecker(linter)
        linter.register_checker(checker)
        args = linter.load_command_line_configuration(
            [file_.name, '-d' ,'bad-continuation'])
        myreporter = reporters.CollectingReporter()
        linter.set_reporter(myreporter)
        linter.check(args)
        assert not myreporter.messages
    finally:
        os.remove(file_.name)
