# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Check format checker helper functions."""

import os
import tempfile
import tokenize

import astroid

from pylint import lint, reporters
from pylint.checkers.base.basic_checker import BasicChecker
from pylint.checkers.format import FormatChecker
from pylint.testutils import CheckerTestCase, MessageTest, _tokenize_str


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
        and so are not always superfluous:
        """
        cases = [
            ("if (odd := is_odd(i))\n"),
            ("not (foo := 5)\n"),
        ]
        for code in cases:
            with self.assertNoMessages():
                self.checker.process_tokens(_tokenize_str(code))

    def testPositiveSuperfluousParensWalrusOperatorIf(self) -> None:
        """Test positive superfluous parens cases with the walrus operator."""
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
        """Make sure the encoding token doesn't change the checker's behavior.

        _tokenize_str doesn't produce an encoding token, but
        reading a file does
        """
        with self.assertNoMessages():
            encoding_token = tokenize.TokenInfo(
                tokenize.ENCODING, "utf-8", (0, 0), (0, 0), ""
            )
            tokens = [
                encoding_token,
                *_tokenize_str("if (\n        None):\n    pass\n"),
            ]
            self.checker.process_tokens(tokens)


def test_disable_global_option_end_of_line() -> None:
    """Test for issue with disabling tokenizer messages
    that extend beyond the scope of the ast tokens
    """
    file_ = tempfile.NamedTemporaryFile("w", delete=False)
    with file_:
        file_.write(
            """
1
    """
        )
    # pylint: disable = too-many-try-statements
    try:
        linter = lint.PyLinter()
        checker = BasicChecker(linter)
        linter.register_checker(checker)
        args = linter._arguments_manager._parse_command_line_configuration(
            [file_.name, "-d", "pointless-statement"]
        )
        myreporter = reporters.CollectingReporter()
        linter.set_reporter(myreporter)
        linter.check(args)
        assert not myreporter.messages
    finally:
        os.remove(file_.name)
