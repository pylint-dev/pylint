# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Check format checker helper functions."""

import os
import re
import tempfile
import tokenize
from decimal import Decimal

import astroid
import pytest

from pylint import lint, reporters
from pylint.checkers.base.basic_checker import BasicChecker
from pylint.checkers.format import FormatChecker, NumberFormatterHelper
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
        file_.write("""
1
    """)
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


class TestIgnorePatternInLongLines(CheckerTestCase):
    CHECKER_CLASS = FormatChecker

    def test_ignore_pattern_in_long_lines(self) -> None:
        self.checker.linter.config.max_line_length = 20
        self.checker.linter.config.ignore_pattern_in_long_lines = re.compile(
            r"\s*# type: ignore"
        )
        cases = [
            "x = '12345'            # type: ignore",
            "x = '12345678901234'   # type: ignore",
        ]
        with self.assertNoMessages():
            for code in cases:
                self.checker.process_tokens(_tokenize_str(code + "\n"))

    def test_ignore_pattern_in_long_lines_still_catches_too_long_code(self) -> None:
        self.checker.linter.config.max_line_length = 20
        self.checker.linter.config.ignore_pattern_in_long_lines = re.compile(
            r"\s*# type: ignore"
        )
        cases = [
            (
                MessageTest("line-too-long", line=1, args=(26, 20)),
                "x = '12345678901234567890'  # type: ignore",
            ),
            (
                MessageTest("line-too-long", line=1, args=(38, 20)),
                "x = '12345'            # other: ignore",
            ),
        ]
        for msg, code in cases:
            with self.assertAddsMessages(msg):
                self.checker.process_tokens(_tokenize_str(code + "\n"))


@pytest.mark.parametrize(
    "value,expected_scientific,expected_engineering,expected_underscore",
    [
        ("0", "0.0", "0.0", "0.0"),
        ("0e10", "0.0", "0.0", "0.0"),
        ("0e-10", "0.0", "0.0", "0.0"),
        ("0.0e10", "0.0", "0.0", "0.0"),
        ("1e0", "1.0", "1.0", "1.0"),
        ("1e10", "1.0e10", "10.0e9", "10_000_000_000.0"),
        # no reason to not use exponential notation for very low number
        # even for strict underscore grouping notation
        ("1e-10", "1.0e-10", "100.0e-12", "1e-10"),
        ("2e1", "2.0e1", "20.0", "20.0"),
        ("2e-1", "2.0e-1", "200.0e-3", "0.2"),
        ("3.456e2", "3.456e2", "345.6", "345.6"),
        ("3.456e-2", "3.456e-2", "34.56e-3", "0.03456"),
        ("4e2", "4.0e2", "400.0", "400.0"),
        ("4e-2", "4.0e-2", "40.0e-3", "0.04"),
        ("50e2", "5.0e3", "5.0e3", "5_000.0"),
        ("50e-2", "5.0e-1", "500.0e-3", "0.5"),
        ("6e6", "6.0e6", "6.0e6", "6_000_000.0"),
        (
            "6e-6",
            "6.0e-6",
            "6.0e-6",
            "6e-06",
        ),  # 6e-06 is what python offer on str(float)
        ("10e5", "1.0e6", "1.0e6", "1_000_000.0"),
        ("10e-5", "1.0e-4", "100.0e-6", "0.0001"),
        ("1_000_000", "1.0e6", "1.0e6", "1_000_000.0"),
        ("1000_000", "1.0e6", "1.0e6", "1_000_000.0"),
        ("20e9", "2.0e10", "20.0e9", "20_000_000_000.0"),
        (
            "20e-9",
            "2.0e-8",
            "20.0e-9",
            "2e-08",
        ),  # 2e-08 is what python offer on str(float)
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
    dec_value = Decimal(value)
    sig_figs = len(dec_value.as_tuple().digits)
    scientific = NumberFormatterHelper.to_standard_scientific_notation(
        dec_value, sig_figs
    )
    assert (
        scientific == expected_scientific
    ), f"Scientific notation mismatch expected {expected_scientific}, got {scientific}"
    engineering = NumberFormatterHelper.to_standard_engineering_notation(
        dec_value, sig_figs
    )
    assert (
        engineering == expected_engineering
    ), f"Engineering notation mismatch expected {expected_engineering}, got {engineering}"
    underscore = NumberFormatterHelper.to_standard_underscore_grouping(float_value)
    assert (
        underscore == expected_underscore
    ), f"Underscore grouping mismatch expected {expected_underscore}, got {underscore}"


@pytest.mark.parametrize(
    "value,group_size,expected",
    [
        # Hex (group by 4)
        ("0x0", 4, "0x0"),
        ("0xA", 4, "0xA"),
        ("0xFF", 4, "0xFF"),
        ("0xABCD", 4, "0xABCD"),
        ("0x1_0000", 4, "0x1_0000"),
        ("0xDEADBEEF", 4, "0xDEAD_BEEF"),
        ("0x12c_456", 4, "0x12_c456"),
        ("0xDE_AD_BE_EF", 4, "0xDEAD_BEEF"),
        ("0x1234567890ABCDEF", 4, "0x1234_5678_90AB_CDEF"),
        ("0xABCDE_F", 4, "0xAB_CDEF"),
        ("0xA_B", 4, "0xAB"),
        ("0XFF", 4, "0xFF"),
        # Binary (group by 4)
        ("0b0", 4, "0b0"),
        ("0b1010", 4, "0b1010"),
        ("0b11110100001001000000", 4, "0b1111_0100_0010_0100_0000"),
        ("0b1111_001", 4, "0b111_1001"),
        ("0B1010", 4, "0b1010"),
        # Octal (group by 3)
        ("0o0", 3, "0o0"),
        ("0o777", 3, "0o777"),
        ("0o123456", 3, "0o123_456"),
        ("0o3641100", 3, "0o3_641_100"),
        ("0o12_3456", 3, "0o123_456"),
        ("0O777", 3, "0o777"),
        # Decimal integers (group by 3, no prefix)
        ("0", 3, "0"),
        ("999", 3, "999"),
        ("1234567", 3, "1_234_567"),
        ("1_23_456", 3, "123_456"),
        ("1000000", 3, "1_000_000"),
    ],
)
def test_to_standard_non_decimal_grouping(
    value: str, group_size: int, expected: str
) -> None:
    prefix_length = 2 if value[:2].lower() in {"0x", "0b", "0o"} else 0
    result = NumberFormatterHelper.to_standard_non_decimal_grouping(
        value, group_size, prefix_length
    )
    assert (
        result == expected
    ), f"Non-decimal grouping mismatch: expected {expected!r}, got {result!r}"
