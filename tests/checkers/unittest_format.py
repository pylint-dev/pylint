# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Check format checker helper functions."""

import os
import tempfile
import tokenize

import astroid
import pytest

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
    that extend beyond the scope of the ast tokens.
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


@pytest.mark.parametrize(
    "value,expected_scientific,expected_engineering,expected_underscore",
    [
        ("0", "0.0", "0.0", "0.0"),
        ("0e10", "0.0", "0.0", "0.0"),
        ("0e-10", "0.0", "0.0", "0.0"),
        ("0.0e10", "0.0", "0.0", "0.0"),
        ("1e0", "1.0", "1.0", "1.0"),
        ("1e10", "1e10", "10e9", "10_000_000_000.0"),
        # no reason to not use exponential notation for very low number
        # even for strict underscore grouping notation
        ("1e-10", "1e-10", "100e-12", "1e-10"),
        ("2e1", "2e1", "20.0", "20.0"),
        ("2e-1", "2e-1", "200e-3", "0.2"),
        ("3.456e2", "3.456e2", "345.6", "345.6"),
        ("3.456e-2", "3.456e-2", "34.56e-3", "0.03456"),
        ("4e2", "4e2", "400.0", "400.0"),
        ("4e-2", "4e-2", "40e-3", "0.04"),
        ("50e2", "5e3", "5e3", "5_000.0"),
        ("50e-2", "5e-1", "500e-3", "0.5"),
        ("6e6", "6e6", "6e6", "6_000_000.0"),
        ("6e-6", "6e-6", "6e-6", "6e-06"),  # 6e-06 is what python offer on str(float)
        ("10e5", "1e6", "1e6", "1_000_000.0"),
        ("10e-5", "1e-4", "100e-6", "0.0001"),
        ("1_000_000", "1e6", "1e6", "1_000_000.0"),
        ("1000_000", "1e6", "1e6", "1_000_000.0"),
        ("20e9", "2e10", "20e9", "20_000_000_000.0"),
        ("20e-9", "2e-8", "20e-9", "2e-08"),  # 2e-08 is what python offer on str(float)
        (
            # 15 significant digits because we get rounding error otherwise
            # and 15 seems enough especially since we don't auto-fix
            "10_5415_456_465498.16354698489",
            "1.05415456465498e14",
            "105.415456465498e12",
            "105_415_456_465_498.16",
        ),
    ],
)
def test_to_another_standard_notation(
    value: str,
    expected_scientific: str,
    expected_engineering: str,
    expected_underscore: str,
) -> None:
    """Test the conversion of numbers to all possible notations."""
    float_value = float(value)
    scientific = FormatChecker.to_standard_scientific_notation(float_value)
    assert (
        scientific == expected_scientific
    ), f"Scientific notation mismatch expected {expected_scientific}, got {scientific}"
    engineering = FormatChecker.to_standard_engineering_notation(float_value)
    assert (
        engineering == expected_engineering
    ), f"Engineering notation mismatch expected {expected_engineering}, got {engineering}"
    underscore = FormatChecker.to_standard_underscore_grouping(float_value)
    assert (
        underscore == expected_underscore
    ), f"Underscore grouping mismatch expected {expected_underscore}, got {underscore}"
