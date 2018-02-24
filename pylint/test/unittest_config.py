# -*- coding: utf-8 -*-
# Copyright (c) 2015 Aru Sahni <arusahni@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2016 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2017 Ville Skyttä <ville.skytta@iki.fi>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unit tests for the config module."""

import re
import sre_constants

from pylint import config
import pytest

def test__regexp_validator_valid():
    result = config.VALIDATORS['regex']("test_.*")
    assert isinstance(result, re._pattern_type)
    assert result.pattern == "test_.*"

def test__regexp_validator_invalid():
    with pytest.raises(sre_constants.error):
        config.VALIDATORS['regex']("test_)")

def test__csv_validator_no_spaces():
    values = ["One", "Two", "Three"]
    result = config.VALIDATORS['csv'](",".join(values))
    assert isinstance(result, list)
    assert len(result) == 3
    for i, value in enumerate(values):
        assert result[i] == value

def test__csv_validator_spaces():
    values = ["One", "Two", "Three"]
    result = config.VALIDATORS['csv'](", ".join(values))
    assert isinstance(result, list)
    assert len(result) == 3
    for i, value in enumerate(values):
        assert result[i] == value

def test__regexp_csv_validator_valid():
    pattern_strings = ["test_.*", "foo\\.bar", "^baz$"]
    result = config.VALIDATORS['regexp_csv'](",".join(pattern_strings))
    for i, regex in enumerate(result):
        assert isinstance(regex, re._pattern_type)
        assert regex.pattern == pattern_strings[i]

def test__regexp_csv_validator_invalid():
    pattern_strings = ["test_.*", "foo\\.bar", "^baz)$"]
    with pytest.raises(sre_constants.error):
        config.VALIDATORS['regexp_csv'](",".join(pattern_strings))
