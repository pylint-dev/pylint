# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

# pylint: disable=redefined-outer-name

from __future__ import annotations

import itertools
from collections.abc import Callable
from pathlib import Path
from typing import cast

import astroid
import pytest
from astroid import AstroidBuildingError, nodes

import pylint.checkers.unicode
import pylint.interfaces
import pylint.testutils

from . import CODEC_AND_MSG, FakeNode


@pytest.fixture()
def bad_char_file_generator(tmp_path: Path) -> Callable[[str, bool, str], Path]:
    """Generates a test file for bad chars.

    The generator also ensures that file generated is correct
    """

    def encode_without_bom(string: str, encoding: str) -> bytes:
        return pylint.checkers.unicode._encode_without_bom(string, encoding)

    # All lines contain a not extra checked invalid character
    lines = (
        "# Example File containing bad ASCII",
        "# invalid char backspace: \b",
        "# Bad carriage-return \r # not at the end",
        "# Invalid char sub: \x1a",
        "# Invalid char esc: \x1b",
    )

    def _bad_char_file_generator(
        codec: str, add_invalid_bytes: bool, line_ending: str
    ) -> Path:
        byte_suffix = b""
        if add_invalid_bytes:
            if codec == "utf-8":
                byte_suffix = b"BAD:\x80abc"
            elif codec == "utf-16":
                byte_suffix = b"BAD:\n"  # Generates Truncated Data
            else:
                byte_suffix = b"BAD:\xc3\x28 "
            byte_suffix = encode_without_bom(" foobar ", codec) + byte_suffix

        line_ending_encoded = encode_without_bom(line_ending, codec)

        # Start content with BOM / codec definition and two empty lines
        content = f"# coding: {codec} \n # \n ".encode(codec)

        # Generate context with the given codec and line ending
        for lineno, line in enumerate(lines):
            byte_line = encode_without_bom(line, codec)
            byte_line += byte_suffix + line_ending_encoded
            content += byte_line

            # Directly test the generated content
            if not add_invalid_bytes:
                # Test that the content is correct and gives no errors
                try:
                    byte_line.decode(codec, "strict")
                except UnicodeDecodeError as e:
                    raise ValueError(
                        f"Line {lineno} did raise unexpected error: {byte_line!r}\n{e}"
                    ) from e
            else:
                try:
                    # But if there was a byte_suffix we expect an error
                    # because that is what we want to test for
                    byte_line.decode(codec, "strict")
                except UnicodeDecodeError:
                    ...
                else:
                    raise ValueError(
                        f"Line {lineno} did not raise decode error: {byte_line!r}"
                    )

        file = tmp_path / "bad_chars.py"
        file.write_bytes(content)
        return file

    return _bad_char_file_generator


class TestBadCharsChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = pylint.checkers.unicode.UnicodeChecker

    checker: pylint.checkers.unicode.UnicodeChecker

    @pytest.mark.parametrize(
        "codec_and_msg, line_ending, add_invalid_bytes",
        [
            pytest.param(
                codec_and_msg,
                line_ending[0],
                suffix[0],
                id=f"{codec_and_msg[0]}_{line_ending[1]}_{suffix[1]}",
            )
            for codec_and_msg, line_ending, suffix in itertools.product(
                CODEC_AND_MSG,
                (("\n", "linux"), ("\r\n", "windows")),
                ((False, "valid_line"), (True, "not_decode_able_line")),
            )
            # Only utf8 can drop invalid lines
            if codec_and_msg[0].startswith("utf") or not suffix[0]
        ],
    )
    def test_find_bad_chars(
        self,
        bad_char_file_generator: Callable[[str, bool, str], Path],
        codec_and_msg: tuple[str, tuple[pylint.testutils.MessageTest]],
        line_ending: str,
        add_invalid_bytes: bool,
    ) -> None:
        """All combinations of bad characters that are accepted by Python at the moment
        are tested in all possible combinations of
          - line ending
          - encoding
          - including not encode-able byte (or not)
        """
        codec, start_msg = codec_and_msg

        start_lines = 2

        file = bad_char_file_generator(codec, add_invalid_bytes, line_ending)

        try:
            # We need to use ast from file as only this function reads bytes and not
            # string
            module = astroid.MANAGER.ast_from_string(file)
        except AstroidBuildingError:
            # pylint: disable-next=redefined-variable-type
            module = cast(nodes.Module, FakeNode(file.read_bytes()))

        expected = [
            *start_msg,
            pylint.testutils.MessageTest(
                msg_id="invalid-character-backspace",
                line=2 + start_lines,
                end_line=2 + start_lines,
                # node=module,
                args=None,
                confidence=pylint.interfaces.HIGH,
                col_offset=27,
                end_col_offset=28,
            ),
            pylint.testutils.MessageTest(
                msg_id="invalid-character-carriage-return",
                line=3 + start_lines,
                end_line=3 + start_lines,
                # node=module,
                args=None,
                confidence=pylint.interfaces.HIGH,
                col_offset=23,
                end_col_offset=24,
            ),
            pylint.testutils.MessageTest(
                msg_id="invalid-character-sub",
                line=4 + start_lines,
                end_line=4 + start_lines,
                # node=module,
                args=None,
                confidence=pylint.interfaces.HIGH,
                col_offset=21,
                end_col_offset=22,
            ),
            pylint.testutils.MessageTest(
                msg_id="invalid-character-esc",
                line=5 + start_lines,
                end_line=5 + start_lines,
                # node=module,
                args=None,
                confidence=pylint.interfaces.HIGH,
                col_offset=21,
                end_col_offset=22,
            ),
        ]
        with self.assertAddsMessages(*expected):
            self.checker.process_module(module)

    @pytest.mark.parametrize(
        "codec_and_msg, char, msg_id",
        [
            pytest.param(
                codec_and_msg,
                char_msg[0],
                char_msg[1],
                id=f"{char_msg[1]}_{codec_and_msg[0]}",
            )
            for codec_and_msg, char_msg in itertools.product(
                CODEC_AND_MSG,
                (
                    ("\0", "invalid-character-nul"),
                    ("\N{ZERO WIDTH SPACE}", "invalid-character-zero-width-space"),
                ),
            )
            # Only utf contains zero width space
            if (
                char_msg[0] != "\N{ZERO WIDTH SPACE}"
                or codec_and_msg[0].startswith("utf")
            )
        ],
    )
    def test_bad_chars_that_would_currently_crash_python(
        self,
        char: str,
        msg_id: str,
        codec_and_msg: tuple[str, tuple[pylint.testutils.MessageTest]],
    ) -> None:
        """Special test for a file containing chars that lead to
        Python or Astroid crashes (which causes Pylint to exit early).
        """
        codec, start_msg = codec_and_msg
        # Create file that will fail loading in astroid.
        # We still want to check this, in case this behavior changes
        content = f"# # coding: {codec}\n# file containing {char} <-\n"
        module = FakeNode(content.encode(codec))

        expected = [
            *start_msg,
            pylint.testutils.MessageTest(
                msg_id=msg_id,
                line=2,
                end_line=2,
                # node=module,
                args=None,
                confidence=pylint.interfaces.HIGH,
                col_offset=19,
                end_col_offset=20,
            ),
        ]

        with self.assertAddsMessages(*expected):
            self.checker.process_module(cast(nodes.Module, module))

    @pytest.mark.parametrize(
        "char, msg, codec",
        [
            pytest.param(
                char.unescaped,
                char.human_code(),
                codec_and_msg[0],
                id=f"{char.name}_{codec_and_msg[0]}",
            )
            for char, codec_and_msg in itertools.product(
                pylint.checkers.unicode.BAD_CHARS, CODEC_AND_MSG
            )
            # Only utf contains zero width space
            if (
                char.unescaped != "\N{ZERO WIDTH SPACE}"
                or codec_and_msg[0].startswith("utf")
            )
        ],
    )
    def test___check_invalid_chars(self, char: str, msg: str, codec: str) -> None:
        """Check function should deliver correct column no matter which codec we used."""
        with self.assertAddsMessages(
            pylint.testutils.MessageTest(
                msg_id=msg,
                line=55,
                args=None,
                confidence=pylint.interfaces.HIGH,
                end_line=55,
                col_offset=5,
                end_col_offset=6,
            )
        ):
            self.checker._check_invalid_chars(f"#234{char}".encode(codec), 55, codec)
