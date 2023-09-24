# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import codecs
import io
import shutil
from pathlib import Path
from typing import cast

import pytest
from astroid import nodes

import pylint.checkers.unicode
import pylint.interfaces
import pylint.testutils

from . import CODEC_AND_MSG, FakeNode

UNICODE_TESTS = Path(__file__).parent.parent.parent / "regrtest_data" / "unicode"


class TestInvalidEncoding(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = pylint.checkers.unicode.UnicodeChecker
    checker: pylint.checkers.unicode.UnicodeChecker

    @pytest.mark.parametrize(
        "test_file, line_no",
        [
            pytest.param(
                "pep_bidirectional_utf_16_le_no_bom.txt",
                2,
                marks=pytest.mark.xfail(
                    reason="Python currently doesn't support UTF-16 code detection"
                ),
            ),
            pytest.param(
                "pep_bidirectional_utf_32_le_no_bom.txt",
                2,
                marks=pytest.mark.xfail(
                    reason="Python currently doesn't support UTF-32 code detection"
                ),
            ),
            # A note to the xfails above: If you open these files in an editor, you
            # only will see garbage if you don't select the correct encoding by hand.
            # Still maybe in the future the python way of defining the encoding could
            # work - even so it is unlikely as the first line is not ASCII and would
            # have to be treated differently anyway...
            ("pep_bidirectional_utf_16_bom.txt", 1),
            ("pep_bidirectional_utf_32_bom.txt", 1),
        ],
    )
    def test_invalid_unicode_files(
        self, tmp_path: Path, test_file: str, line_no: int
    ) -> None:
        test_file_path = UNICODE_TESTS / test_file
        target = shutil.copy(
            test_file_path, tmp_path / test_file.replace(".txt", ".py")
        )

        # Fake node as otherwise we get syntax errors etc...
        # So currently the UTF-16/UTF-32 tests does not work, as UTF-16 / UTF-32
        # is not really working at all in in Python, but checking it now already
        # is future save in case that changes....

        module = FakeNode(Path(target).read_bytes())

        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id="invalid-unicode-codec",
                confidence=pylint.interfaces.HIGH,
                # node=module,
                line=line_no,
                end_line=1,
                col_offset=None,
                end_col_offset=None,
            ),
            pylint.testutils.MessageTest(
                msg_id="bidirectional-unicode",
                confidence=pylint.interfaces.HIGH,
                # node=module,
                line=line_no + 2,
                end_line=line_no + 2,
                col_offset=0,
                end_col_offset=37,
            ),
        ):
            self.checker.process_module(cast(nodes.Module, module))

    @pytest.mark.parametrize(
        "content, codec, line",
        [
            pytest.param(b"# Nothing", "utf-8", 1, id="default_utf8"),
            pytest.param(b"# coding: latin-1", "iso-8859-1", 1, id="pep263_latin1"),
            pytest.param(
                b"#!/usr/bin/python\n# coding: latin-1",
                "iso-8859-1",
                2,
                id="pep263_latin1_multiline",
            ),
            pytest.param(b"# coding: ascii", "ascii", 1, id="pep263_ascii"),
            pytest.param(b"# coding: UTF-8", "utf-8", 1, id="pep263_utf-8"),
            # This looks correct but is actually wrong. If you would try to decode
            # the byte to utf-16be it would fail
            pytest.param(
                b"# coding: UTF-16le", "utf-16le", 1, id="pep263_utf-16le_fake"
            ),
            # This contains no bom but a correct encoding line in none ascii
            # So this fails at the moment
            pytest.param(
                "# coding: UTF-16le".encode("utf-16le"),
                "utf-16le",
                1,
                id="pep263_utf-16le_real",
                marks=pytest.mark.xfail(reason="Currently not supported by Python"),
            ),
            *(
                pytest.param(bom, codec, 1, id=f"bom_{codec}")
                for codec, bom in (
                    ("utf-8", codecs.BOM_UTF8),
                    ("utf-16le", codecs.BOM_UTF16_LE),
                    ("utf-16be", codecs.BOM_UTF16_BE),
                    ("utf-32le", codecs.BOM_UTF32_LE),
                    ("utf-32be", codecs.BOM_UTF32_BE),
                )
            ),
        ],
    )
    def test__determine_codec(self, content: bytes, codec: str, line: int) -> None:
        """The codec determined should be exact no matter what we throw at it."""
        assert self.checker._determine_codec(io.BytesIO(content)) == (codec, line)

    def test__determine_codec_raises_syntax_error_on_invalid_input(self) -> None:
        """Invalid input should lead to a SyntaxError."""
        with pytest.raises(SyntaxError):
            self.checker._determine_codec(io.BytesIO(b"\x80abc"))

    @pytest.mark.parametrize(
        "codec, msg",
        (pytest.param(codec, msg, id=codec) for codec, msg in CODEC_AND_MSG),
    )
    def test___check_codec(
        self, codec: str, msg: tuple[pylint.testutils.MessageTest]
    ) -> None:
        with self.assertAddsMessages(*msg):
            self.checker._check_codec(codec, 1)
