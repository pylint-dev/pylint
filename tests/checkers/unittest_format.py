# Copyright (c) 2009-2011, 2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2012 FELD Boris <lothiraldan@gmail.com>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2014-2020 Claudiu Popa <pcmanticore@gmail.com>
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
# Copyright (c) 2018, 2020 Bryce Guinta <bryce.guinta@protonmail.com>
# Copyright (c) 2018 Bryce Guinta <bryce.paul.guinta@gmail.com>
# Copyright (c) 2018, 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Check format checker helper functions"""

import os
import tempfile
import tokenize
from typing import Any

import astroid

from pylint import lint, reporters
from pylint.checkers.format import FormatChecker
from pylint.testutils import CheckerTestCase, MessageTest, _tokenize_str


class TestMultiStatementLine(CheckerTestCase):
    CHECKER_CLASS = FormatChecker

    def testSingleLineIfStmts(self) -> None:
        stmt = astroid.extract_node(
            """
        if True: pass  #@
        """
        )
        self.checker.config.single_line_if_stmt = False
        with self.assertAddsMessages(
            MessageTest("multiple-statements", node=stmt.body[0])
        ):
            self.visitFirst(stmt)
        self.checker.config.single_line_if_stmt = True
        with self.assertNoMessages():
            self.visitFirst(stmt)
        stmt = astroid.extract_node(
            """
        if True: pass  #@
        else:
            pass
        """
        )
        with self.assertAddsMessages(
            MessageTest("multiple-statements", node=stmt.body[0])
        ):
            self.visitFirst(stmt)

    def testSingleLineClassStmts(self) -> None:
        stmt = astroid.extract_node(
            """
        class MyError(Exception): pass  #@
        """
        )
        self.checker.config.single_line_class_stmt = False
        with self.assertAddsMessages(
            MessageTest("multiple-statements", node=stmt.body[0])
        ):
            self.visitFirst(stmt)
        self.checker.config.single_line_class_stmt = True
        with self.assertNoMessages():
            self.visitFirst(stmt)

        stmt = astroid.extract_node(
            """
        class MyError(Exception): a='a'  #@
        """
        )
        self.checker.config.single_line_class_stmt = False
        with self.assertAddsMessages(
            MessageTest("multiple-statements", node=stmt.body[0])
        ):
            self.visitFirst(stmt)
        self.checker.config.single_line_class_stmt = True
        with self.assertNoMessages():
            self.visitFirst(stmt)

        stmt = astroid.extract_node(
            """
        class MyError(Exception): a='a'; b='b'  #@
        """
        )
        self.checker.config.single_line_class_stmt = False
        with self.assertAddsMessages(
            MessageTest("multiple-statements", node=stmt.body[0])
        ):
            self.visitFirst(stmt)
        self.checker.config.single_line_class_stmt = True
        with self.assertAddsMessages(
            MessageTest("multiple-statements", node=stmt.body[0])
        ):
            self.visitFirst(stmt)

    def testTryExceptFinallyNoMultipleStatement(self) -> None:
        tree = astroid.extract_node(
            """
        try:  #@
            pass
        except:
            pass
        finally:
            pass"""
        )
        with self.assertNoMessages():
            self.visitFirst(tree)

    def visitFirst(self, tree: Any) -> None:
        self.checker.process_tokens([])
        self.checker.visit_default(tree.body[0])

    def test_ellipsis_is_ignored(self) -> None:
        code = """
        from typing import overload
        @overload
        def concat2(arg1: str) -> str: ...
        """
        tree = astroid.extract_node(code)
        with self.assertNoMessages():
            self.visitFirst(tree)

        code = """
        def concat2(arg1: str) -> str: ...
        """
        stmt = astroid.extract_node(code)
        with self.assertAddsMessages(
            MessageTest("multiple-statements", node=stmt.body[0])
        ):
            self.visitFirst(stmt)


class TestSuperfluousParentheses(CheckerTestCase):
    CHECKER_CLASS = FormatChecker

    def testCheckKeywordParensHandlesValidCases(self) -> None:
        cases = [
            "if foo:",
            "if foo():",
            "if (x and y) or z:",
            "assert foo()",
            "assert ()",
            "if (1, 2) in (3, 4):",
            "if (a or b) in c:",
            "return (x for x in x)",
            "if (x for x in x):",
            "for x in (x for x in x):",
            "not (foo or bar)",
            "not (foo or bar) and baz",
            "return [x for x in (3 if 1 else [4])]",
            "return (x for x in ((3, 4) if 2 > 1 else (5, 6)))",
        ]
        with self.assertNoMessages():
            for code in cases:
                self.checker._check_keyword_parentheses(_tokenize_str(code), 0)

    def testCheckKeywordParensHandlesUnnecessaryParens(self) -> None:
        cases = [
            (MessageTest("superfluous-parens", line=1, args="if"), "if (foo):", 0),
            (
                MessageTest("superfluous-parens", line=1, args="if"),
                "if ((foo, bar)):",
                0,
            ),
            (
                MessageTest("superfluous-parens", line=1, args="if"),
                "if (foo(bar)):",
                0,
            ),
            (MessageTest("superfluous-parens", line=1, args="not"), "not (foo)", 0),
            (
                MessageTest("superfluous-parens", line=1, args="not"),
                "if not (foo):",
                1,
            ),
            (
                MessageTest("superfluous-parens", line=1, args="if"),
                "if (not (foo)):",
                0,
            ),
            (
                MessageTest("superfluous-parens", line=1, args="not"),
                "if (not (foo)):",
                2,
            ),
            (
                MessageTest("superfluous-parens", line=1, args="for"),
                "for (x) in (1, 2, 3):",
                0,
            ),
            (
                MessageTest("superfluous-parens", line=1, args="if"),
                "if (1) in (1, 2, 3):",
                0,
            ),
        ]
        for msg, code, offset in cases:
            with self.assertAddsMessages(msg):
                self.checker._check_keyword_parentheses(_tokenize_str(code), offset)

    def testNoSuperfluousParensWalrusOperatorIf(self) -> None:
        """Parenthesis change the meaning of assignment in the walrus operator
        and so are not always superfluous:"""
        cases = [
            ("if (odd := is_odd(i))\n"),
            ("not (foo := 5)\n"),
        ]
        for code in cases:
            with self.assertNoMessages():
                self.checker.process_tokens(_tokenize_str(code))

    def testPositiveSuperfluousParensWalrusOperatorIf(self) -> None:
        """Test positive superfluous parens cases with the walrus operator"""
        cases = [
            (
                MessageTest("superfluous-parens", line=1, args="if"),
                "if ((x := y)):\n",
            ),
            (
                MessageTest("superfluous-parens", line=1, args="not"),
                "if not ((x := y)):\n",
            ),
        ]
        for msg, code in cases:
            with self.assertAddsMessages(msg):
                self.checker.process_tokens(_tokenize_str(code))

    def testCheckIfArgsAreNotUnicode(self) -> None:
        cases = [("if (foo):", 0), ("assert (1 == 1)", 0)]

        for code, offset in cases:
            self.checker._check_keyword_parentheses(_tokenize_str(code), offset)
            got = self.linter.release_messages()
            assert isinstance(got[-1].args, str)

    def testFuturePrintStatementWithoutParensWarning(self) -> None:
        code = """from __future__ import print_function
print('Hello world!')
"""
        tree = astroid.parse(code)
        with self.assertNoMessages():
            self.checker.process_module(tree)
            self.checker.process_tokens(_tokenize_str(code))

    def testKeywordParensFalsePositive(self) -> None:
        code = "if 'bar' in (DICT or {}):"
        with self.assertNoMessages():
            self.checker._check_keyword_parentheses(_tokenize_str(code), start=2)


class TestCheckSpace(CheckerTestCase):
    CHECKER_CLASS = FormatChecker

    def test_encoding_token(self) -> None:
        """Make sure the encoding token doesn't change the checker's behavior

        _tokenize_str doesn't produce an encoding token, but
        reading a file does
        """
        with self.assertNoMessages():
            encoding_token = tokenize.TokenInfo(
                tokenize.ENCODING, "utf-8", (0, 0), (0, 0), ""
            )
            tokens = [encoding_token] + _tokenize_str(
                "if (\n        None):\n    pass\n"
            )
            self.checker.process_tokens(tokens)


def test_disable_global_option_end_of_line() -> None:
    """
    Test for issue with disabling tokenizer messages
    that extend beyond the scope of the ast tokens
    """
    file_ = tempfile.NamedTemporaryFile("w", delete=False)
    with file_:
        file_.write(
            """
mylist = [
    None
        ]
    """
        )
    try:
        linter = lint.PyLinter()
        checker = FormatChecker(linter)
        linter.register_checker(checker)
        args = linter.load_command_line_configuration(
            [file_.name, "-d", "bad-continuation"]
        )
        myreporter = reporters.CollectingReporter()
        linter.set_reporter(myreporter)
        linter.check(args)
        assert not myreporter.messages
    finally:
        os.remove(file_.name)
