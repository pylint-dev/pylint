# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import itertools
import unicodedata
from pathlib import Path
from typing import cast

import astroid
import pytest
from astroid import nodes

import pylint.checkers.unicode
import pylint.interfaces
import pylint.testutils

from . import FakeNode

UNICODE_TESTS = Path(__file__).parent.parent.parent / "regrtest_data" / "unicode"


class TestBidirectionalUnicodeChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = pylint.checkers.unicode.UnicodeChecker

    checker: pylint.checkers.unicode.UnicodeChecker

    def test_finds_bidirectional_unicode_that_currently_not_parsed(self) -> None:
        """Test an example from https://github.com/nickboucher/trojan-source/tree/main/Python
        that is currently not working Python but producing a syntax error.

        So we test this to make sure it stays like this
        """
        test_file = UNICODE_TESTS / "invisible_function.txt"

        with pytest.raises(astroid.AstroidSyntaxError):
            astroid.MANAGER.ast_from_string(test_file.read_text("utf-8"))

        with pytest.raises(AssertionError):
            # The following errors are not risen at the moment,
            # But we keep this in order to allow writing the test fast, if
            # the condition above isn't met anymore.
            module = FakeNode(test_file.read_bytes())
            with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="bidirectional-unicode",
                    confidence=pylint.interfaces.HIGH,
                    # node=module,
                    line=6,
                    end_line=10,
                    col_offset=0,
                    end_col_offset=17,
                ),
                pylint.testutils.MessageTest(
                    msg_id="bidirectional-unicode",
                    confidence=pylint.interfaces.HIGH,
                    line=10,
                    # node=module,
                    end_line=10,
                    col_offset=0,
                    end_col_offset=20,
                ),
            ):
                self.checker.process_module(cast(nodes.Module, module))

    @pytest.mark.parametrize(
        "bad_string, codec",
        [
            pytest.param(
                char,
                codec,
                id=f"{unicodedata.name(char)}_{codec}".replace(" ", "_"),
            )
            for char, codec in itertools.product(
                pylint.checkers.unicode.BIDI_UNICODE,
                ("utf-8", "utf-16le", "utf-16be", "utf-32le", "utf-32be"),
            )
        ],
    )
    def test_find_bidi_string(self, bad_string: str, codec: str) -> None:
        """Ensure that all Bidirectional strings are detected.

        Tests also UTF-16 and UTF-32.
        """
        expected = pylint.testutils.MessageTest(
            msg_id="bidirectional-unicode",
            confidence=pylint.interfaces.HIGH,
            line=1,
            # node=module,
            end_line=1,
            col_offset=0,
            end_col_offset=3,
        )

        with self.assertAddsMessages(expected):
            self.checker._check_bidi_chars(f"# {bad_string}".encode(codec), 1, codec)
