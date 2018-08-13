# -*- coding: utf-8 -*-
# Copyright (c) 2015 Aru Sahni <arusahni@gmail.com>
# Copyright (c) 2016-2018 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2017 Ville Skyttä <ville.skytta@iki.fi>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unit tests for the config module."""

import re
import sre_constants

from pylint import config
import pytest


RE_PATTERN_TYPE = getattr(re, 'Pattern', getattr(re, '_pattern_type', None))


def test__regexp_validator_valid():
    result = config._regexp_validator(None, None, "test_.*")
    assert isinstance(result, RE_PATTERN_TYPE)
    assert result.pattern == "test_.*"

def test__regexp_validator_invalid():
    with pytest.raises(sre_constants.error):
        config._regexp_validator(None, None, "test_)")

def test__csv_validator_no_spaces():
    values = ["One", "Two", "Three"]
    result = config._csv_validator(None, None, ",".join(values))
    assert isinstance(result, list)
    assert len(result) == 3
    for i, value in enumerate(values):
        assert result[i] == value

def test__csv_validator_spaces():
    values = ["One", "Two", "Three"]
    result = config._csv_validator(None, None, ", ".join(values))
    assert isinstance(result, list)
    assert len(result) == 3
    for i, value in enumerate(values):
        assert result[i] == value

def test__regexp_csv_validator_valid():
    pattern_strings = ["test_.*", "foo\\.bar", "^baz$"]
    result = config._regexp_csv_validator(None, None, ",".join(pattern_strings))
    for i, regex in enumerate(result):
        assert isinstance(regex, RE_PATTERN_TYPE)
        assert regex.pattern == pattern_strings[i]

def test__regexp_csv_validator_invalid():
    pattern_strings = ["test_.*", "foo\\.bar", "^baz)$"]
    with pytest.raises(sre_constants.error):
        config._regexp_csv_validator(None, None, ",".join(pattern_strings))
