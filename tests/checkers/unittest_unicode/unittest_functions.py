# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import itertools
from pathlib import Path

import pytest

import pylint.checkers.unicode

SEARCH_DICT_BYTE_UTF8 = {
    char.unescaped.encode("utf-8"): char for char in pylint.checkers.unicode.BAD_CHARS
}


@pytest.mark.parametrize(
    "line, expected, search_dict",
    [
        # Test special carrier return cases
        pytest.param(
            "valid windows\r\n",
            {},
            pylint.checkers.unicode.BAD_ASCII_SEARCH_DICT,
            id="valid-windows",
        ),
        pytest.param(
            b"TOTO = ('Caf\xe9', 'Caf\xe9', 'Caf\xe9')\r\n",
            {},
            SEARCH_DICT_BYTE_UTF8,
            id="valid-windows-bytes",
        ),
        pytest.param(
            "invalid\r windows\r\n",
            {7: pylint.checkers.unicode.BAD_ASCII_SEARCH_DICT["\r"]},
            pylint.checkers.unicode.BAD_ASCII_SEARCH_DICT,
            id="invalid-carrier-return-windows",
        ),
        pytest.param(
            "invalid\r linux\n",
            {7: pylint.checkers.unicode.BAD_ASCII_SEARCH_DICT["\r"]},
            pylint.checkers.unicode.BAD_ASCII_SEARCH_DICT,
            id="invalid-carrier-return-linux",
        ),
        pytest.param(
            b"invalid\r windows\r\n",
            {7: pylint.checkers.unicode.BAD_ASCII_SEARCH_DICT["\r"]},
            SEARCH_DICT_BYTE_UTF8,
            id="invalid-carrier-return-windows-bytes",
        ),
        pytest.param(
            b"invalid\r linux\n",
            {7: pylint.checkers.unicode.BAD_ASCII_SEARCH_DICT["\r"]},
            SEARCH_DICT_BYTE_UTF8,
            id="invalid-carrier-return-linux-bytes",
        ),
        # Auto test Linux all remaining Linux cases ...
        *(
            pytest.param(
                f"invalid{char.unescaped} back\n",
                {7: char},
                pylint.checkers.unicode.BAD_ASCII_SEARCH_DICT,
                id=f"invalid-{char.name}-linux",
            )
            for char in pylint.checkers.unicode.BAD_CHARS
            if char.unescaped != "\r"
        ),
        # ... also byte encoded
        *(
            pytest.param(
                f"invalid{char.unescaped} back\n".encode("ASCII"),
                {7: char},
                SEARCH_DICT_BYTE_UTF8,
                id=f"invalid-{char.name}-linux-bytes",
            )
            for char in pylint.checkers.unicode.BAD_CHARS[:-1]
            if char.unescaped != "\r"
        ),
        # Test all remaining windows cases ...
        *(
            pytest.param(
                f"invalid{char.unescaped} back\r\n",
                {7: char},
                pylint.checkers.unicode.BAD_ASCII_SEARCH_DICT,
                id=f"invalid-{char.name}-windows",
            )
            for char in pylint.checkers.unicode.BAD_CHARS
            if char.unescaped != "\r"
        ),
        # ... also byte encoded
        *(
            pytest.param(
                f"invalid{char.unescaped} back\r\n".encode("ASCII"),
                {7: char},
                SEARCH_DICT_BYTE_UTF8,
                id=f"invalid-{char.name}-windows-bytes",
            )
            for char in pylint.checkers.unicode.BAD_CHARS[:-1]
            if char.unescaped != "\r"
        ),
    ],
)
def test_map_positions_to_result(
    line: pylint.checkers.unicode._StrLike,
    expected: dict[int, pylint.checkers.unicode._BadChar],
    search_dict: dict[
        pylint.checkers.unicode._StrLike, pylint.checkers.unicode._BadChar
    ],
) -> None:
    """Test all possible outcomes for map position function in UTF-8 and ASCII."""
    if isinstance(line, bytes):
        newline = b"\n"
    else:
        newline = "\n"
    assert (
        pylint.checkers.unicode._map_positions_to_result(
            line, search_dict, new_line=newline
        )
        == expected
    )


@pytest.mark.parametrize(
    "line",
    [
        pytest.param("1234567890", id="no_line_ending"),
        pytest.param(b"1234567890", id="no_line_ending_byte"),
        pytest.param("1234567890\n", id="linux"),
        pytest.param(b"1234567890\n", id="linux_byte"),
        pytest.param("1234567890\r\n", id="windows"),
        pytest.param(b"1234567890\r\n", id="windows_byte"),
        pytest.param("12345678\n\r", id="wrong_order"),
        pytest.param(b"12345678\n\r", id="wrong_order_byte"),
    ],
)
def test_line_length(line: pylint.checkers.unicode._StrLike) -> None:
    assert pylint.checkers.unicode._line_length(line, "utf-8") == 10


@pytest.mark.parametrize(
    "line",
    [
        pytest.param("1234567890", id="no_line_ending"),
        pytest.param("1234567890\n", id="linux"),
        pytest.param("1234567890\r\n", id="windows"),
        pytest.param("12345678\n\r", id="wrong_order"),
    ],
)
def test_line_length_utf16(line: str) -> None:
    assert pylint.checkers.unicode._line_length(line.encode("utf-16"), "utf-16") == 10


@pytest.mark.parametrize(
    "line",
    [
        pytest.param("1234567890", id="no_line_ending"),
        pytest.param("1234567890\n", id="linux"),
        pytest.param("1234567890\r\n", id="windows"),
        pytest.param("12345678\n\r", id="wrong_order"),
    ],
)
def test_line_length_utf32(line: str) -> None:
    assert pylint.checkers.unicode._line_length(line.encode("utf-32"), "utf-32") == 10


@pytest.mark.parametrize(
    "codec, expected",
    [
        ("utf-8sig", "utf-8"),
        ("utf8", "utf-8"),
        ("utf 8", "utf-8"),
        ("utf-8", "utf-8"),
        ("utf-8", "utf-8"),
        ("utf-16", "utf-16"),
        ("utf-32", "utf-32"),
        ("utf 16", "utf-16"),
        ("utf 32", "utf-32"),
        ("utf 16 LE", "utf-16le"),
        ("utf 32-BE", "utf-32be"),
        ("UTF-32", "utf-32"),
        ("UTF-32-le", "utf-32le"),
        ("UTF-16 LE", "utf-16le"),
        ("UTF-16BE", "utf-16be"),
        ("UTF8", "utf-8"),
        ("Latin1", "latin1"),
        ("ASCII", "ascii"),
    ],
)
def test__normalize_codec_name(codec: str, expected: str) -> None:
    assert pylint.checkers.unicode._normalize_codec_name(codec) == expected


@pytest.mark.parametrize(
    "codec, line_ending, final_new_line",
    [
        pytest.param(
            codec,
            line_ending[0],
            final_nl[0],
            id=f"{codec}_{line_ending[1]}_{final_nl[1]}",
        )
        for codec, line_ending, final_nl in itertools.product(
            (
                "utf-8",
                "utf-16",
                "utf-16le",
                "utf-16be",
                "utf-32",
                "utf-32le",
                "utf-32be",
            ),
            (("\n", "linux"), ("\r\n", "windows")),
            ((True, "final_nl"), (False, "no_final_nl")),
        )
    ],
)
def test___fix_utf16_32_line_stream(
    tmp_path: Path, codec: str, line_ending: str, final_new_line: bool
) -> None:
    """Content of stream should be the same as should be the length."""

    def decode_line(line: bytes, codec: str) -> str:
        return line.decode(codec)

    file = tmp_path / "test.txt"

    content = [
        f"line1{line_ending}",
        f"# Line 2{line_ending}",
        f"łöł{line_ending}",
        f"last line{line_ending if final_new_line else ''}",
    ]

    text = "".join(content)
    encoded = text.encode(codec)

    file.write_bytes(encoded)

    gathered = b""
    collected = []
    with file.open("rb") as f:
        for line in pylint.checkers.unicode._fix_utf16_32_line_stream(f, codec):
            gathered += line
            collected.append(decode_line(line, codec))

    # Test content equality
    assert collected == content
    # Test byte equality
    assert gathered == encoded


@pytest.mark.parametrize(
    "codec, expected",
    [
        ("utf-32", 4),
        ("utf-32-le", 4),
        ("utf-16", 2),
        ("utf-8", 1),
        ("latin1", 1),
        ("ascii", 1),
    ],
)
def test__byte_to_str_length(codec: str, expected: int) -> None:
    assert pylint.checkers.unicode._byte_to_str_length(codec) == expected
