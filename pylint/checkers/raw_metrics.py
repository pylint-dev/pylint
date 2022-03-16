# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import sys
import tokenize
from typing import TYPE_CHECKING, Any, Optional, cast

from pylint.checkers import BaseTokenChecker
from pylint.interfaces import ITokenChecker
from pylint.reporters.ureports.nodes import Table
from pylint.utils import LinterStats, diff_string

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def report_raw_stats(
    sect,
    stats: LinterStats,
    old_stats: Optional[LinterStats],
) -> None:
    """Calculate percentage of code / doc / comment / empty."""
    total_lines = stats.code_type_count["total"]
    sect.description = f"{total_lines} lines have been analyzed"
    lines = ["type", "number", "%", "previous", "difference"]
    for node_type in ("code", "docstring", "comment", "empty"):
        node_type = cast(Literal["code", "docstring", "comment", "empty"], node_type)
        total = stats.code_type_count[node_type]
        percent = float(total * 100) / total_lines if total_lines else None
        old = old_stats.code_type_count[node_type] if old_stats else None
        diff_str = diff_string(old, total) if old else None
        lines += [
            node_type,
            str(total),
            f"{percent:.2f}" if percent is not None else "NC",
            str(old) if old else "NC",
            diff_str if diff_str else "NC",
        ]
    sect.append(Table(children=lines, cols=5, rheaders=1))


class RawMetricsChecker(BaseTokenChecker):
    """Checker that provides raw metrics instead of checking anything.

    Provides:
    * total number of lines
    * total number of code lines
    * total number of docstring lines
    * total number of comments lines
    * total number of empty lines
    """

    __implements__ = (ITokenChecker,)

    # configuration section name
    name = "metrics"
    # configuration options
    options = ()
    # messages
    msgs: Any = {}
    # reports
    reports = (("RP0701", "Raw metrics", report_raw_stats),)

    def __init__(self, linter):
        super().__init__(linter)

    def open(self):
        """Init statistics."""
        self.linter.stats.reset_code_count()

    def process_tokens(self, tokens):
        """Update stats."""
        i = 0
        tokens = list(tokens)
        while i < len(tokens):
            i, lines_number, line_type = get_type(tokens, i)
            self.linter.stats.code_type_count["total"] += lines_number
            self.linter.stats.code_type_count[line_type] += lines_number


JUNK = (tokenize.NL, tokenize.INDENT, tokenize.NEWLINE, tokenize.ENDMARKER)


def get_type(tokens, start_index):
    """Return the line type : docstring, comment, code, empty."""
    i = start_index
    start = tokens[i][2]
    pos = start
    line_type = None
    while i < len(tokens) and tokens[i][2][0] == start[0]:
        tok_type = tokens[i][0]
        pos = tokens[i][3]
        if line_type is None:
            if tok_type == tokenize.STRING:
                line_type = "docstring"
            elif tok_type == tokenize.COMMENT:
                line_type = "comment"
            elif tok_type in JUNK:
                pass
            else:
                line_type = "code"
        i += 1
    if line_type is None:
        line_type = "empty"
    elif i < len(tokens) and tokens[i][0] == tokenize.NEWLINE:
        i += 1
    return i, pos[0] - start[0] + 1, line_type


def register(linter: "PyLinter") -> None:
    linter.register_checker(RawMetricsChecker(linter))
