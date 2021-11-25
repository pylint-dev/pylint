# Copyright (c) 2015 Aru Sahni <arusahni@gmail.com>
# Copyright (c) 2016-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2017 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Unit tests for the config module."""

import re
import sre_constants
from typing import Dict, Tuple, Type

import pytest

from pylint import config
from pylint.checkers import BaseChecker
from pylint.testutils import CheckerTestCase, set_config
from pylint.utils.utils import get_global_option

RE_PATTERN_TYPE = getattr(re, "Pattern", getattr(re, "_pattern_type", None))


def test__regexp_validator_valid() -> None:
    result = config.option._regexp_validator(None, None, "test_.*")
    assert isinstance(result, RE_PATTERN_TYPE)
    assert result.pattern == "test_.*"


def test__regexp_validator_invalid() -> None:
    with pytest.raises(sre_constants.error):
        config.option._regexp_validator(None, None, "test_)")


def test__csv_validator_no_spaces() -> None:
    values = ["One", "Two", "Three"]
    result = config.option._csv_validator(None, None, ",".join(values))
    assert isinstance(result, list)
    assert len(result) == 3
    for i, value in enumerate(values):
        assert result[i] == value


def test__csv_validator_spaces() -> None:
    values = ["One", "Two", "Three"]
    result = config.option._csv_validator(None, None, ", ".join(values))
    assert isinstance(result, list)
    assert len(result) == 3
    for i, value in enumerate(values):
        assert result[i] == value


def test__regexp_csv_validator_valid() -> None:
    pattern_strings = ["test_.*", "foo\\.bar", "^baz$"]
    result = config.option._regexp_csv_validator(None, None, ",".join(pattern_strings))
    for i, regex in enumerate(result):
        assert isinstance(regex, RE_PATTERN_TYPE)
        assert regex.pattern == pattern_strings[i]


def test__regexp_csv_validator_invalid() -> None:
    pattern_strings = ["test_.*", "foo\\.bar", "^baz)$"]
    with pytest.raises(sre_constants.error):
        config.option._regexp_csv_validator(None, None, ",".join(pattern_strings))


class TestPyLinterOptionSetters(CheckerTestCase):
    """Class to check the set_config decorator and get_global_option util
    for options declared in PyLinter."""

    class Checker(BaseChecker):
        name = "checker"
        msgs: Dict[str, Tuple[str, ...]] = {}
        options = (("An option", {"An option": "dict"}),)

    CHECKER_CLASS: Type = Checker

    @set_config(ignore_paths=".*/tests/.*,.*\\ignore\\.*")
    def test_ignore_paths_with_value(self) -> None:
        """Test ignore-paths option with value"""
        options = get_global_option(self.checker, "ignore-paths")

        assert any(i.match("dir/tests/file.py") for i in options)
        assert any(i.match("dir\\tests\\file.py") for i in options)
        assert any(i.match("dir/ignore/file.py") for i in options)
        assert any(i.match("dir\\ignore\\file.py") for i in options)

    def test_ignore_paths_with_no_value(self) -> None:
        """Test ignore-paths option with no value.
        Compare against actual list to see if validator works."""
        options = get_global_option(self.checker, "ignore-paths")

        assert options == []
