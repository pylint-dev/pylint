import pytest

from pylint.utils.pragma_parser import (
    OPTION_PO,
    InvalidPragmaError,
    UnRecognizedOptionError,
    parse_pragma,
)


def test_simple_pragma():
    comment = "#pylint: disable = missing-docstring"
    match = OPTION_PO.search(comment)
    for pragma_repr in parse_pragma(match.group(2)):
        assert pragma_repr.action == "disable"
        assert pragma_repr.messages == ["missing-docstring"]


def test_disable_checker_with_number_in_name():
    comment = "#pylint: disable = j3-custom-checker"
    match = OPTION_PO.search(comment)
    for pragma_repr in parse_pragma(match.group(2)):
        assert pragma_repr.action == "disable"
        assert pragma_repr.messages == ["j3-custom-checker"]


def test_simple_pragma_no_messages():
    comment = "#pylint: skip-file"
    match = OPTION_PO.search(comment)
    for pragma_repr in parse_pragma(match.group(2)):
        assert pragma_repr.action == "skip-file"
        assert pragma_repr.messages == []


def test_simple_pragma_multiple_messages():
    comment = "#pylint: disable = missing-docstring, invalid-name"
    match = OPTION_PO.search(comment)
    for pragma_repr in parse_pragma(match.group(2)):
        assert pragma_repr.action == "disable"
        assert pragma_repr.messages == ["missing-docstring", "invalid-name"]


def test_multiple_pragma_multiple_messages():
    comment = "#pylint: disable = missing-docstring, invalid-name, enable = R0202, no-self-use"
    match = OPTION_PO.search(comment)
    res = list(parse_pragma(match.group(2)))
    assert res[0].action == "disable"
    assert res[0].messages == ["missing-docstring", "invalid-name"]
    assert res[1].action == "enable"
    assert res[1].messages == ["R0202", "no-self-use"]


def test_missing_assignment():
    comment = "#pylint: disable missing-docstring"
    match = OPTION_PO.search(comment)
    with pytest.raises(InvalidPragmaError):
        list(parse_pragma(match.group(2)))


def test_missing_keyword():
    comment = "#pylint: = missing-docstring"
    match = OPTION_PO.search(comment)
    with pytest.raises(InvalidPragmaError):
        list(parse_pragma(match.group(2)))


def test_unsupported_assignment():
    comment = "#pylint: disable-all = missing-docstring"
    match = OPTION_PO.search(comment)
    with pytest.raises(UnRecognizedOptionError):
        list(parse_pragma(match.group(2)))


def test_unknown_keyword_with_messages():
    comment = "#pylint: unknown-keyword = missing-docstring"
    match = OPTION_PO.search(comment)
    with pytest.raises(UnRecognizedOptionError):
        list(parse_pragma(match.group(2)))


def test_unknown_keyword_without_messages():
    comment = "#pylint: unknown-keyword"
    match = OPTION_PO.search(comment)
    with pytest.raises(UnRecognizedOptionError):
        list(parse_pragma(match.group(2)))


def test_missing_message():
    comment = "#pylint: disable = "
    match = OPTION_PO.search(comment)
    with pytest.raises(InvalidPragmaError):
        list(parse_pragma(match.group(2)))


def test_parse_message_with_dash():
    comment = "#pylint: disable = raw_input-builtin"
    match = OPTION_PO.search(comment)
    res = list(parse_pragma(match.group(2)))
    assert res[0].action == "disable"
    assert res[0].messages == ["raw_input-builtin"]
