# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Python code format's checker.

By default, try to follow Guido's style guide :

https://www.python.org/doc/essays/styleguide/

Some parts of the process_token method is based from The Tab Nanny std module.
"""

from __future__ import annotations

import decimal
import math
import re
import tokenize
from decimal import Decimal, localcontext
from functools import reduce
from re import Match
from typing import TYPE_CHECKING, Literal

from astroid import nodes

from pylint.checkers import BaseRawFileChecker, BaseTokenChecker
from pylint.checkers.utils import only_required_for_messages
from pylint.constants import WarningScope
from pylint.interfaces import HIGH
from pylint.typing import MessageDefinitionTuple
from pylint.utils.pragma_parser import OPTION_PO, PragmaParserError, parse_pragma

if TYPE_CHECKING:
    from pylint.lint import PyLinter


_KEYWORD_TOKENS = {
    "assert",
    "del",
    "elif",
    "except",
    "for",
    "if",
    "in",
    "not",
    "raise",
    "return",
    "while",
    "yield",
    "with",
    "=",
    ":=",
}
_JUNK_TOKENS = {tokenize.COMMENT, tokenize.NL}


class FloatFormatterHelper:

    @classmethod
    def standardize(
        cls,
        number: float,
        original_string: str,
        scientific: bool = True,
        engineering: bool = True,
        pep515: bool = True,
    ) -> str:
        dec_number = Decimal(original_string)
        sig_figs = len(dec_number.as_tuple().digits)

        suggested = set()
        if scientific:
            suggested.add(cls.to_standard_scientific_notation(dec_number, sig_figs))
        if engineering:
            suggested.add(cls.to_standard_engineering_notation(dec_number, sig_figs))
        if pep515:
            suggested.add(cls.to_standard_underscore_grouping(number))
        return "' or '".join(sorted(suggested))

    @classmethod
    def to_standard_or_engineering_base(cls, number: float) -> tuple[str, str]:
        """Calculate scientific notation components (base, exponent) for a number.

        Returns a tuple (base, exponent) where:
        - base is a number between 1 and 10 (or exact 0)
        - exponent is the power of 10 needed to represent the original number
        """
        if number == 0:
            return "0", "0"
        if number == math.inf:
            return "math.inf", "0"
        exponent = math.floor(math.log10(abs(number)))
        if exponent == 0:
            return str(number), "0"
        base_value = number / (10**exponent)
        # 15 significant digits because if we add more precision then
        # we get into rounding errors territory
        base_str = f"{base_value:.15g}".rstrip("0").rstrip(".")
        exp_str = str(exponent)
        return base_str, exp_str

    @classmethod
    def to_standard_scientific_notation(cls, dec_number: Decimal, sig_figs: int) -> str:
        if dec_number == 0:
            return "0.0"
        if dec_number == Decimal("Infinity") or dec_number == Decimal("-Infinity"):
            return "math.inf"

        exponent = dec_number.adjusted()

        if exponent == 0:
            base_str = f"{float(dec_number):.{min(sig_figs, 15)}g}"
            if "." not in base_str:
                base_str += ".0"
            return base_str

        with localcontext() as ctx:
            ctx.prec = 50
            try:
                base_value = dec_number / (Decimal(10) ** exponent)
            except decimal.Overflow:
                # Extreme exponents (e.g. 1e12_000_000) overflow Decimal arithmetic;
                # fall back to float-based computation.
                base, exp_str = cls.to_standard_or_engineering_base(float(dec_number))
                return f"{base}e{exp_str}" if exp_str != "0" else base
        # Cap at 15 significant digits (float precision limit) to avoid
        # g-format switching to scientific notation for intermediate values.
        base_str = f"{float(base_value):.{min(sig_figs, 15)}g}"

        if "." not in base_str and "e" not in base_str.lower():
            base_str += ".0"

        return f"{base_str}e{exponent}"

    @classmethod
    def to_standard_engineering_notation(
        cls, dec_number: Decimal, sig_figs: int
    ) -> str:
        if dec_number == 0:
            return "0.0"
        if dec_number == Decimal("Infinity") or dec_number == Decimal("-Infinity"):
            return "math.inf"

        exponent = dec_number.adjusted()

        remainder = exponent % 3

        with localcontext() as ctx:
            ctx.prec = 50
            try:
                if exponent < 0:
                    adjustment = 3 - ((-exponent) % 3)
                    if adjustment == 3:
                        adjustment = 0
                    exp_value = exponent - adjustment
                    base_value = dec_number / (Decimal(10) ** exp_value)
                elif remainder != 0:
                    exp_value = exponent - remainder
                    base_value = dec_number / (Decimal(10) ** exp_value)
                else:
                    exp_value = exponent
                    base_value = dec_number / (Decimal(10) ** exponent)
            except decimal.Overflow:
                # Extreme exponents overflow Decimal arithmetic; fall back to
                # float-based scientific notation.
                base, exp_str = cls.to_standard_or_engineering_base(float(dec_number))
                return f"{base}e{exp_str}" if exp_str != "0" else base

        # Use at least 3 significant digits to prevent g-format from switching
        # to scientific notation (engineering base is always < 1000), and cap
        # at 15 (float precision limit).
        precision = max(min(sig_figs, 15), 3)
        base_str = f"{float(base_value):.{precision}g}"

        if "." not in base_str and "e" not in base_str.lower():
            base_str += ".0"

        if exp_value != 0:
            return f"{base_str}e{exp_value}"
        return base_str

    @classmethod
    def to_standard_underscore_grouping(cls, number: float) -> str:
        number_str = str(number)
        if "e" in number_str or "E" in number_str:
            # python itself want to display this as exponential there's no reason to
            # not use exponential notation for very small number even for strict
            # underscore grouping notation
            return number_str
        if "." in number_str:
            int_part, dec_part = number_str.split(".")
        else:
            int_part = number_str
            dec_part = "0"
        grouped_int_part = ""
        for i, digit in enumerate(reversed(int_part)):
            if i > 0 and i % 3 == 0:
                grouped_int_part = "_" + grouped_int_part
            grouped_int_part = digit + grouped_int_part
        return f"{grouped_int_part}.{dec_part}"

    @classmethod
    def to_standard_non_decimal_grouping(
        cls, string: str, group_size: int, prefix_length: int = 2
    ) -> str:
        clean = string.replace("_", "")
        prefix = clean[:prefix_length].lower() if prefix_length else ""
        digits = clean[prefix_length:]
        if len(digits) <= group_size:
            return f"{prefix}{digits}"
        grouped = ""
        for i, digit in enumerate(reversed(digits)):
            if i > 0 and i % group_size == 0:
                grouped = "_" + grouped
            grouped = digit + grouped
        return f"{prefix}{grouped}"


MSGS: dict[str, MessageDefinitionTuple] = {
    "C0301": (
        "Line too long (%s/%s)",
        "line-too-long",
        "Used when a line is longer than a given number of characters.",
    ),
    "C0302": (
        "Too many lines in module (%s/%s)",  # was W0302
        "too-many-lines",
        "Used when a module has too many lines, reducing its readability.",
    ),
    "C0303": (
        "Trailing whitespace",
        "trailing-whitespace",
        "Used when there is whitespace between the end of a line and the newline.",
    ),
    "C0304": (
        "Final newline missing",
        "missing-final-newline",
        "Used when the last line in a file is missing a newline.",
    ),
    "C0305": (
        "Trailing newlines",
        "trailing-newlines",
        "Used when there are trailing blank lines in a file.",
    ),
    "W0311": (
        "Bad indentation. Found %s %s, expected %s",
        "bad-indentation",
        "Used when an unexpected number of indentation's tabulations or "
        "spaces has been found.",
    ),
    "W0301": (
        "Unnecessary semicolon",  # was W0106
        "unnecessary-semicolon",
        'Used when a statement is ended by a semi-colon (";"), which '
        "isn't necessary (that's python, not C ;).",
    ),
    "C0321": (
        "More than one statement on a single line",
        "multiple-statements",
        "Used when more than one statement is found on the same line.",
        {"scope": WarningScope.NODE},
    ),
    "C0325": (
        "Unnecessary parens after %r keyword",
        "superfluous-parens",
        "Used when a single item in parentheses follows an if, for, or "
        "other keyword.",
    ),
    "C0327": (
        "Mixed line endings LF and CRLF",
        "mixed-line-endings",
        "Used when there are mixed (LF and CRLF) newline signs in a file.",
    ),
    "C0328": (
        "Unexpected line ending format. There is '%s' while it should be '%s'.",
        "unexpected-line-ending-format",
        "Used when there is different newline than expected.",
    ),
    "C0329": (
        "'%s' %s, and it should be written as '%s' instead",
        "bad-number-notation",
        "Emitted when a number is written in a non-standard notation. The three "
        "allowed notation above the threshold are the scientific notation, the "
        "engineering notation, and the underscore grouping notation defined in PEP515.",
    ),
}


def _last_token_on_line_is(tokens: TokenWrapper, line_end: int, token: str) -> bool:
    return (line_end > 0 and tokens.token(line_end - 1) == token) or (
        line_end > 1
        and tokens.token(line_end - 2) == token
        and tokens.type(line_end - 1) == tokenize.COMMENT
    )


class TokenWrapper:
    """A wrapper for readable access to token information."""

    def __init__(self, tokens: list[tokenize.TokenInfo]) -> None:
        self._tokens = tokens

    def token(self, idx: int) -> str:
        return self._tokens[idx][1]

    def type(self, idx: int) -> int:
        return self._tokens[idx][0]

    def start_line(self, idx: int) -> int:
        return self._tokens[idx][2][0]

    def start_col(self, idx: int) -> int:
        return self._tokens[idx][2][1]

    def line(self, idx: int) -> str:
        return self._tokens[idx][4]


class FormatChecker(BaseTokenChecker, BaseRawFileChecker):
    """Formatting checker.

    Checks for :
    * unauthorized constructions
    * strict indentation
    * line length
    """

    # configuration section name
    name = "format"
    # messages
    msgs = MSGS
    # configuration options
    # for available dict keys/values see the optik parser 'add_option' method
    options = (
        (
            "max-line-length",
            {
                "default": 100,
                "type": "int",
                "metavar": "<int>",
                "help": (
                    "Maximum number of characters on a single line. "
                    "Pylint's default of 100 is based on PEP 8's guidance that teams "
                    "may choose line lengths up to 99 characters."
                ),
            },
        ),
        (
            "ignore-long-lines",
            {
                "type": "regexp",
                "metavar": "<regexp>",
                "default": r"^\s*(# )?<?https?://\S+>?$",
                "help": (
                    "Regexp for a line that is allowed to be longer than the limit."
                ),
            },
        ),
        (
            "ignore-pattern-in-long-lines",
            {
                "type": "regexp",
                "metavar": "<regexp>",
                "default": None,
                "help": (
                    "Regexp for a part of a line that will not be counted when "
                    "calculating the line length."
                ),
            },
        ),
        (
            "single-line-if-stmt",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y or n>",
                "help": (
                    "Allow the body of an if to be on the same "
                    "line as the test if there is no else."
                ),
            },
        ),
        (
            "single-line-class-stmt",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y or n>",
                "help": (
                    "Allow the body of a class to be on the same "
                    "line as the declaration if body contains "
                    "single statement."
                ),
            },
        ),
        (
            "max-module-lines",
            {
                "default": 1000,
                "type": "int",
                "metavar": "<int>",
                "help": "Maximum number of lines in a module.",
            },
        ),
        (
            "indent-string",
            {
                "default": "    ",
                "type": "non_empty_string",
                "metavar": "<string>",
                "help": "String used as indentation unit. This is usually "
                '"    " (4 spaces) or "\\t" (1 tab).',
            },
        ),
        (
            "indent-after-paren",
            {
                "type": "int",
                "metavar": "<int>",
                "default": 4,
                "help": "Number of spaces of indent required inside a hanging "
                "or continued line.",
            },
        ),
        (
            "expected-line-ending-format",
            {
                "type": "choice",
                "metavar": "<empty or LF or CRLF>",
                "default": "",
                "choices": ["", "LF", "CRLF"],
                "help": (
                    "Expected format of line ending, "
                    "e.g. empty (any line ending), LF or CRLF."
                ),
            },
        ),
        (
            "float-notation-threshold",
            {
                # default big enough to not trigger on pixel perfect web design
                # on big screen
                "default": "1e6",
                "type": "float",
                "metavar": "<float>",
                "help": (
                    "Threshold for float literals to be expected to be written "
                    "using the scientific, engineering or underscore notation."
                    " If the absolute value of a float literal is greater than this "
                    "value (or smaller than the inverse of this value for scientific "
                    "and engineering notation), it will be checked."
                ),
            },
        ),
        (
            "float-notation-style",
            {
                "type": "choice",
                "metavar": "<style>",
                "default": "",
                "choices": ["", "scientific", "engineering", "underscore"],
                "help": (
                    "Enforce a specific notation for number literals above "
                    "'float-notation-threshold'. Choices: empty (allow all "
                    "standard notations), 'scientific', 'engineering', or "
                    "'underscore' (PEP 515)."
                ),
            },
        ),
    )

    def open(self) -> None:
        self._lines: dict[int, str] = {}
        self._visited_lines: dict[int, Literal[1, 2]] = {}
        style = self.linter.config.float_notation_style
        self.all_float_notation_allowed = style == ""
        self.strict_scientific = style == "scientific"
        self.strict_engineering = style == "engineering"
        self.strict_underscore = style == "underscore"
        if self.strict_scientific:
            if self.linter.config.float_notation_threshold < 10:
                raise ValueError(
                    "'float-notation-threshold' must be at least 10 "
                    "when 'float-notation-style' is 'scientific', got "
                    f"{self.linter.config.float_notation_threshold}."
                )
        elif self.linter.config.float_notation_threshold < 1000:
            raise ValueError(
                "'float-notation-threshold' must be at least 1000, got "
                f"{self.linter.config.float_notation_threshold}."
            )

    def new_line(self, tokens: TokenWrapper, line_end: int, line_start: int) -> None:
        """A new line has been encountered, process it if necessary."""
        if _last_token_on_line_is(tokens, line_end, ";"):
            self.add_message("unnecessary-semicolon", line=tokens.start_line(line_end))

        line_num = tokens.start_line(line_start)
        line = tokens.line(line_start)
        if tokens.type(line_start) not in _JUNK_TOKENS:
            self._lines[line_num] = line.split("\n")[0]
        self.check_lines(tokens, line_start, line, line_num)

    def process_module(self, node: nodes.Module) -> None:
        pass

    # pylint: disable-next = too-many-return-statements, too-many-branches
    def _check_keyword_parentheses(
        self, tokens: list[tokenize.TokenInfo], start: int
    ) -> None:
        """Check that there are not unnecessary parentheses after a keyword.

        Parens are unnecessary if there is exactly one balanced outer pair on a
        line and contains no commas (i.e. is not a tuple).

        Args:
        tokens: The entire list of Tokens.
        start: The position of the keyword in the token list.
        """
        # If the next token is not a paren, we're fine.
        if tokens[start + 1].string != "(":
            return
        if (
            tokens[start].string == "not"
            and start > 0
            and tokens[start - 1].string == "is"
        ):
            # If this is part of an `is not` expression, we have a binary operator
            # so the parentheses are not necessarily redundant.
            return
        found_and_or = False
        contains_walrus_operator = False
        walrus_operator_depth = 0
        contains_double_parens = 0
        depth = 0
        keyword_token = str(tokens[start].string)
        line_num = tokens[start].start[0]
        for i in range(start, len(tokens) - 1):
            token = tokens[i]

            # If we hit a newline, then assume any parens were for continuation.
            if token.type == tokenize.NL:
                return
            # Since the walrus operator doesn't exist below python3.8, the tokenizer
            # generates independent tokens
            if (
                token.string == ":="  # <-- python3.8+ path
                or token.string + tokens[i + 1].string == ":="
            ):
                contains_walrus_operator = True
                walrus_operator_depth = depth
            if token.string == "(":
                depth += 1
                if tokens[i + 1].string == "(":
                    contains_double_parens = 1
            elif token.string == ")":
                depth -= 1
                if depth:
                    if contains_double_parens and tokens[i + 1].string == ")":
                        # For walrus operators in `if (not)` conditions and comprehensions
                        if keyword_token in {"in", "if", "not"}:
                            continue
                        return
                    contains_double_parens -= 1
                    continue
                # ')' can't happen after if (foo), since it would be a syntax error.
                if tokens[i + 1].string in {":", ")", "]", "}", "in"} or tokens[
                    i + 1
                ].type in {tokenize.NEWLINE, tokenize.ENDMARKER, tokenize.COMMENT}:
                    if contains_walrus_operator and walrus_operator_depth - 1 == depth:
                        return
                    # The empty tuple () is always accepted.
                    if i == start + 2:
                        return
                    if found_and_or:
                        return
                    if keyword_token == "in":
                        # This special case was added in https://github.com/pylint-dev/pylint/pull/4948
                        # but it could be removed in the future. Avoid churn for now.
                        return
                    self.add_message(
                        "superfluous-parens", line=line_num, args=keyword_token
                    )
                return
            elif depth == 1:
                match token[1]:
                    case ",":
                        # This is a tuple, which is always acceptable.
                        return
                    case "and" | "or":
                        # 'and' and 'or' are the only boolean operators with lower precedence
                        # than 'not', so parens are only required when they are found.
                        found_and_or = True
                    case "yield":
                        # A yield inside an expression must always be in parentheses,
                        # quit early without error.
                        return
                    case "for":
                        # A generator expression always has a 'for' token in it, and
                        # the 'for' token is only legal inside parens when it is in a
                        # generator expression.  The parens are necessary here, so bail
                        # without an error.
                        return
                    case "else":
                        # A generator expression can have an 'else' token in it.
                        # We check the rest of the tokens to see if any problems occur after
                        # the 'else'.
                        if "(" in (i.string for i in tokens[i:]):
                            self._check_keyword_parentheses(tokens[i:], 0)
                        return

    def process_tokens(self, tokens: list[tokenize.TokenInfo]) -> None:
        """Process tokens and search for:

        - too long lines (i.e. longer than <max_chars>)
        - optionally bad construct (if given, bad_construct must be a compiled
          regular expression).
        """
        indents = [0]
        check_equal = False
        line_num = 0
        self._lines = {}
        self._visited_lines = {}
        self._last_line_ending: str | None = None
        last_blank_line_num = 0
        for idx, (tok_type, string, start, _, line) in enumerate(tokens):
            if start[0] != line_num:
                line_num = start[0]
                # A tokenizer oddity: if an indented line contains a multi-line
                # docstring, the line member of the INDENT token does not contain
                # the full line; therefore we check the next token on the line.
                if tok_type == tokenize.INDENT:
                    self.new_line(TokenWrapper(tokens), idx - 1, idx + 1)
                else:
                    self.new_line(TokenWrapper(tokens), idx - 1, idx)

            match tok_type:
                case tokenize.NEWLINE:
                    # a program statement, or ENDMARKER, will eventually follow,
                    # after some (possibly empty) run of tokens of the form
                    #     (NL | COMMENT)* (INDENT | DEDENT+)?
                    # If an INDENT appears, setting check_equal is wrong, and will
                    # be undone when we see the INDENT.
                    check_equal = True
                    self._check_line_ending(string, line_num)
                case tokenize.INDENT:
                    check_equal = False
                    self.check_indent_level(string, indents[-1] + 1, line_num)
                    indents.append(indents[-1] + 1)
                case tokenize.DEDENT:
                    # there's nothing we need to check here!  what's important is
                    # that when the run of DEDENTs ends, the indentation of the
                    # program statement (or ENDMARKER) that triggered the run is
                    # equal to what's left at the top of the indents stack
                    check_equal = True
                    if len(indents) > 1:
                        del indents[-1]
                case tokenize.NL:
                    if not line.strip("\r\n"):
                        last_blank_line_num = line_num
                case tokenize.COMMENT | tokenize.ENCODING:
                    pass
                case _:
                    # This is the first concrete token following a NEWLINE, so it
                    # must be the first token of the next program statement, or an
                    # ENDMARKER; the "line" argument exposes the leading white-space
                    # for this statement; in the case of ENDMARKER, line is an empty
                    # string, so will properly match the empty string with which the
                    # "indents" stack was seeded
                    if check_equal:
                        check_equal = False
                        self.check_indent_level(line, indents[-1], line_num)

            if tok_type == tokenize.NUMBER:
                if (
                    self.linter.is_message_enabled("bad-number-notation")
                    and "j" not in string  # complex number, not handled
                ):
                    self._check_number_notation(line_num, start, string)

            if string in _KEYWORD_TOKENS:
                self._check_keyword_parentheses(tokens, idx)

        line_num -= 1  # to be ok with "wc -l"
        if line_num > self.linter.config.max_module_lines:
            # Get the line where the too-many-lines (or its message id)
            # was disabled or default to 1.
            message_definition = self.linter.msgs_store.get_message_definitions(
                "too-many-lines"
            )[0]
            names = (message_definition.msgid, "too-many-lines")
            lineno = next(
                filter(None, (self.linter._pragma_lineno.get(name) for name in names)),
                1,
            )
            self.add_message(
                "too-many-lines",
                args=(line_num, self.linter.config.max_module_lines),
                line=lineno,
            )

        # See if there are any trailing lines.  Do not complain about empty
        # files like __init__.py markers.
        if line_num == last_blank_line_num and line_num > 0:
            self.add_message("trailing-newlines", line=line_num)

    def _check_number_notation(
        self, line_num: int, start: tuple[int, int], string: str
    ) -> None:
        match string[1:2].lower():
            case "x":
                self._check_non_decimal_notation(
                    line_num, start, string, 4, r"[0-9a-fA-F]", "hex digits"
                )
            case "b":
                self._check_non_decimal_notation(
                    line_num, start, string, 4, r"[01]", "binary digits"
                )
            case "o":
                self._check_non_decimal_notation(
                    line_num, start, string, 3, r"[0-7]", "octal digits"
                )
            case _ if "." in string or "e" in string or "E" in string:
                self._check_bad_float_notation(line_num, start, string)
            case _:
                self._check_non_decimal_notation(
                    line_num, start, string, 3, r"[0-9]", "digits", "", 0
                )

    def _check_bad_float_notation(  # pylint: disable=too-many-locals
        self, line_num: int, start: tuple[int, int], string: str
    ) -> None:

        has_exponent = "e" in string or "E" in string
        value = float(string.replace("_", ""))
        engineering = self.all_float_notation_allowed or self.strict_engineering
        scientific = self.all_float_notation_allowed or self.strict_scientific
        pep515 = self.all_float_notation_allowed or self.strict_underscore

        def add_bad_notation_message(reason: str) -> None:
            suggestion = FloatFormatterHelper.standardize(
                value,
                string,
                scientific,
                engineering,
                pep515,
            )
            self.add_message(
                "bad-number-notation",
                line=line_num,
                col_offset=start[1],
                end_lineno=line_num,
                end_col_offset=start[1] + len(string),
                args=(string, reason, suggestion),
                confidence=HIGH,
            )

        if string in {"0", "0.0", "0."}:
            # 0 is a special case because it is used very often, and float approximation
            # being what they are it needs to be special cased anyway for scientific and
            # engineering notation when checking if a number is under 1/threshold
            return None
        has_underscore = "_" in string
        abs_value = abs(value)
        under_threshold = abs_value < self.linter.config.float_notation_threshold
        should_not_be_checked_because_of_threshold = under_threshold and (
            # Underscore notation doesn't need to check close-to-zero values
            self.strict_underscore
            # For scientific/engineering: also skip if not in the close-to-zero range
            # (values like 0.00012e-26 that are < 1/threshold should still be checked)
            or abs_value >= 1 / self.linter.config.float_notation_threshold
        )
        if not (has_underscore or has_exponent):
            if should_not_be_checked_because_of_threshold:
                # This number is free style, we do not have to check it, unless it's
                # written complexly, then it could be badly written
                return None
            threshold = self.linter.config.float_notation_threshold
            dec_threshold = Decimal(str(threshold))
            dec_close = Decimal(str(1 / threshold))
            close_to_zero_threshold = (
                FloatFormatterHelper.to_standard_scientific_notation(
                    dec_close, len(dec_close.as_tuple().digits)
                )
            )
            threshold = FloatFormatterHelper.to_standard_scientific_notation(
                dec_threshold, len(dec_threshold.as_tuple().digits)
            )
            if under_threshold:
                return add_bad_notation_message(
                    f"is smaller than {close_to_zero_threshold}"
                )
            return add_bad_notation_message(f"is bigger than {threshold}")
        if has_exponent:
            if self.strict_underscore or has_underscore:
                # If we have exponent it means it's not proper underscore
                return add_bad_notation_message(
                    "has exponent and underscore at the same time"
                )
            base_as_str, exponent_as_str = string.lower().split("e")
            base = float(base_as_str)
            wrong_scientific_notation = not (1 <= base < 10)
            if self.strict_scientific and wrong_scientific_notation:
                return add_bad_notation_message(
                    f"has a base, '{base}', that is not strictly inferior to 10"
                    if base == 10
                    else f"has a base, '{base}', that is not between 1 and 10"
                )
            wrong_engineering_notation = not (
                1 <= base < 1000 and int(exponent_as_str) % 3 == 0
            )
            if (self.strict_engineering and wrong_engineering_notation) or (
                wrong_scientific_notation and wrong_engineering_notation
            ):
                return add_bad_notation_message(
                    f"has an exponent '{exponent_as_str}' that is not a multiple of 3"
                    if 1 <= base < 1000
                    else (
                        f"has a base, '{base}', that is not strictly inferior to 1000"
                        if base == 1000
                        else f"has a base, '{base}', that is not between 1 and 1000"
                    )
                )
        elif has_underscore:
            if self.strict_scientific or self.strict_engineering:
                return add_bad_notation_message(
                    "has underscores instead of scientific notation"
                    if self.strict_scientific
                    else "has underscores instead of engineering notation"
                )
            wrong_underscore_notation = not re.match(
                r"^\d{0,3}(_\d{3})*\.?\d*([eE]-?\d{0,3}(_\d{3})*)?$", string
            )
            if pep515 and wrong_underscore_notation:
                return add_bad_notation_message(
                    "has underscores that are not delimiting packs of three digits"
                )
        return None

    def _check_non_decimal_notation(
        self,
        line_num: int,
        start: tuple[int, int],
        string: str,
        group_size: int,
        digit_pattern: str,
        group_name: str,
        prefix_pattern: str = "0[a-zA-Z]_?",
        prefix_length: int = 2,
    ) -> None:
        has_underscore = "_" in string
        value = int(string.replace("_", ""), 0)
        if has_underscore:
            pattern = rf"^{prefix_pattern}{digit_pattern}{{1,{group_size}}}(_{digit_pattern}{{{group_size}}})*$"
            if not re.match(pattern, string):
                suggestion = FloatFormatterHelper.to_standard_non_decimal_grouping(
                    string, group_size, prefix_length
                )
                self.add_message(
                    "bad-number-notation",
                    line=line_num,
                    col_offset=start[1],
                    end_lineno=line_num,
                    end_col_offset=start[1] + len(string),
                    args=(
                        string,
                        f"has underscores that are not grouping {group_name} by {group_size}",
                        suggestion,
                    ),
                    confidence=HIGH,
                )
        elif value >= self.linter.config.float_notation_threshold:
            suggestion = FloatFormatterHelper.to_standard_non_decimal_grouping(
                string, group_size, prefix_length
            )
            threshold = self.linter.config.float_notation_threshold
            dec_threshold = Decimal(str(threshold))
            threshold_str = FloatFormatterHelper.to_standard_scientific_notation(
                dec_threshold, len(dec_threshold.as_tuple().digits)
            )
            self.add_message(
                "bad-number-notation",
                line=line_num,
                col_offset=start[1],
                end_lineno=line_num,
                end_col_offset=start[1] + len(string),
                args=(
                    string,
                    f"is bigger than {threshold_str}",
                    suggestion,
                ),
                confidence=HIGH,
            )

    def _check_line_ending(self, line_ending: str, line_num: int) -> None:
        # check if line endings are mixed
        if self._last_line_ending is not None:
            # line_ending == "" indicates a synthetic newline added at
            # the end of a file that does not, in fact, end with a
            # newline.
            if line_ending and line_ending != self._last_line_ending:
                self.add_message("mixed-line-endings", line=line_num)

        self._last_line_ending = line_ending

        # check if line ending is as expected
        expected = self.linter.config.expected_line_ending_format
        if expected:
            # reduce multiple \n\n\n\n to one \n
            line_ending = reduce(lambda x, y: x + y if x != y else x, line_ending, "")
            line_ending = "LF" if line_ending == "\n" else "CRLF"
            if line_ending != expected:
                self.add_message(
                    "unexpected-line-ending-format",
                    args=(line_ending, expected),
                    line=line_num,
                )

    @only_required_for_messages("multiple-statements")
    def visit_default(self, node: nodes.NodeNG) -> None:
        """Check the node line number and check it if not yet done."""
        if not node.is_statement:
            return
        if not node.root().pure_python:
            return
        prev_sibl = node.previous_sibling()
        if prev_sibl is not None:
            prev_line = prev_sibl.fromlineno
        elif isinstance(
            node.parent, nodes.Try
        ) and self._is_first_node_in_else_finally_body(node, node.parent):
            prev_line = self._infer_else_finally_line_number(node, node.parent)
        elif isinstance(node.parent, nodes.Module):
            prev_line = 0
        else:
            prev_line = node.parent.statement().fromlineno
        line = node.fromlineno
        assert line, node
        if prev_line == line and self._visited_lines.get(line) != 2:
            self._check_multi_statement_line(node, line)
            return
        if line in self._visited_lines:
            return
        try:
            tolineno = node.blockstart_tolineno
        except AttributeError:
            tolineno = node.tolineno
        assert tolineno, node
        lines: list[str] = []
        for line in range(line, tolineno + 1):  # noqa: B020
            self._visited_lines[line] = 1
            try:
                lines.append(self._lines[line].rstrip())
            except KeyError:
                lines.append("")

    def _is_first_node_in_else_finally_body(
        self, node: nodes.NodeNG, parent: nodes.Try
    ) -> bool:
        if parent.orelse and node == parent.orelse[0]:
            return True
        if parent.finalbody and node == parent.finalbody[0]:
            return True
        return False

    def _infer_else_finally_line_number(
        self, node: nodes.NodeNG, parent: nodes.Try
    ) -> int:
        last_line_of_prev_block = 0
        if node in parent.finalbody and parent.orelse:
            last_line_of_prev_block = parent.orelse[-1].tolineno
        elif parent.handlers and parent.handlers[-1].body:
            last_line_of_prev_block = parent.handlers[-1].body[-1].tolineno
        elif parent.body:
            last_line_of_prev_block = parent.body[-1].tolineno

        return last_line_of_prev_block + 1 if last_line_of_prev_block else 0

    def _check_multi_statement_line(self, node: nodes.NodeNG, line: int) -> None:
        """Check for lines containing multiple statements."""
        match node:
            case nodes.With():
                # Do not warn about multiple nested context managers in with statements.
                return
            case nodes.NodeNG(
                parent=nodes.If(orelse=[])
            ) if self.linter.config.single_line_if_stmt:
                return
            case nodes.NodeNG(
                parent=nodes.ClassDef(body=[_])
            ) if self.linter.config.single_line_class_stmt:
                return
            case nodes.Expr(
                parent=nodes.FunctionDef() | nodes.ClassDef(),
                value=nodes.Const(value=value),
            ) if (
                value is Ellipsis
            ):
                # Functions stubs and class with ``Ellipsis`` as body are exempted.
                return

        self.add_message("multiple-statements", node=node, confidence=HIGH)
        self._visited_lines[line] = 2

    def check_trailing_whitespace_ending(self, line: str, i: int) -> None:
        """Check that there is no trailing white-space."""
        # exclude \f (formfeed) from the rstrip
        stripped_line = line.rstrip("\t\n\r\v ")
        if line[len(stripped_line) :] not in ("\n", "\r\n"):
            self.add_message(
                "trailing-whitespace",
                line=i,
                col_offset=len(stripped_line),
                confidence=HIGH,
            )

    def check_line_length(self, line: str, i: int, checker_off: bool) -> None:
        """Check that the line length is less than the authorized value."""
        max_chars = self.linter.config.max_line_length
        ignore_long_line = self.linter.config.ignore_long_lines
        line = line.rstrip()
        if len(line) > max_chars and not ignore_long_line.search(line):
            if checker_off:
                self.linter.add_ignored_message("line-too-long", i)
            else:
                self.add_message("line-too-long", line=i, args=(len(line), max_chars))

    @staticmethod
    def remove_pylint_option_from_lines(options_pattern_obj: Match[str]) -> str:
        """Remove the `# pylint ...` pattern from lines."""
        lines = options_pattern_obj.string
        purged_lines = (
            lines[: options_pattern_obj.start(1)].rstrip()
            + lines[options_pattern_obj.end(1) :]
        )
        return purged_lines

    @staticmethod
    def is_line_length_check_activated(pylint_pattern_match_object: Match[str]) -> bool:
        """Return True if the line length check is activated."""
        try:
            for pragma in parse_pragma(pylint_pattern_match_object.group(2)):
                if pragma.action == "disable" and "line-too-long" in pragma.messages:
                    return False
        except PragmaParserError:
            # Printing useful information dealing with this error is done in the lint package
            pass
        return True

    @staticmethod
    def specific_splitlines(lines: str) -> list[str]:
        """Split lines according to universal newlines except those in a specific
        sets.
        """
        unsplit_ends = {
            "\x0b",  # synonym of \v
            "\x0c",  # synonym of \f
            "\x1c",
            "\x1d",
            "\x1e",
            "\x85",
            "\u2028",
            "\u2029",
        }
        res: list[str] = []
        buffer = ""
        for atomic_line in lines.splitlines(True):
            if atomic_line[-1] not in unsplit_ends:
                res.append(buffer + atomic_line)
                buffer = ""
            else:
                buffer += atomic_line
        return res

    def check_lines(
        self, tokens: TokenWrapper, line_start: int, lines: str, lineno: int
    ) -> None:
        """Check given lines for potential messages.

        Check if lines have:
        - a final newline
        - no trailing white-space
        - less than a maximum number of characters
        """
        # we're first going to do a rough check whether any lines in this set
        # go over the line limit. If none of them do, then we don't need to
        # parse out the pylint options later on and can just assume that these
        # lines are clean

        # we'll also handle the line ending check here to avoid double-iteration
        # unless the line lengths are suspect

        max_chars = self.linter.config.max_line_length

        split_lines = self.specific_splitlines(lines)

        for offset, line in enumerate(split_lines):
            if not line.endswith("\n"):
                self.add_message("missing-final-newline", line=lineno + offset)
                continue
            # We don't test for trailing whitespaces in strings
            # See https://github.com/pylint-dev/pylint/issues/6936
            # and https://github.com/pylint-dev/pylint/issues/3822
            if tokens.type(line_start) != tokenize.STRING:
                self.check_trailing_whitespace_ending(line, lineno + offset)

        # This check is purposefully simple and doesn't rstrip since this is running
        # on every line you're checking it's advantageous to avoid doing a lot of work
        potential_line_length_warning = any(
            len(line) > max_chars for line in split_lines
        )

        # if there were no lines passing the max_chars config, we don't bother
        # running the full line check (as we've met an even more strict condition)
        if not potential_line_length_warning:
            return

        # Line length check may be deactivated through `pylint: disable` comment
        mobj = OPTION_PO.search(lines)
        checker_off = False
        if mobj:
            if not self.is_line_length_check_activated(mobj):
                checker_off = True
            # The 'pylint: disable whatever' should not be taken into account for line length count
            lines = self.remove_pylint_option_from_lines(mobj)

        ignore_pattern_in_long_lines = self.linter.config.ignore_pattern_in_long_lines
        if ignore_pattern_in_long_lines:
            lines = ignore_pattern_in_long_lines.sub("", lines)

        # here we re-run specific_splitlines since we have filtered out pylint options above
        for offset, line in enumerate(self.specific_splitlines(lines)):
            self.check_line_length(line, lineno + offset, checker_off)

    def check_indent_level(self, string: str, expected: int, line_num: int) -> None:
        """Return the indent level of the string."""
        indent = self.linter.config.indent_string
        if indent == "\\t":  # \t is not interpreted in the configuration file
            indent = "\t"
        level = 0
        unit_size = len(indent)
        while string[:unit_size] == indent:
            string = string[unit_size:]
            level += 1
        suppl = ""
        while string and string[0] in " \t":
            suppl += string[0]
            string = string[1:]
        if level != expected or suppl:
            i_type = "spaces"
            if indent[0] == "\t":
                i_type = "tabs"
            self.add_message(
                "bad-indentation",
                line=line_num,
                args=(level * unit_size + len(suppl), i_type, expected * unit_size),
            )


def register(linter: PyLinter) -> None:
    linter.register_checker(FormatChecker(linter))
