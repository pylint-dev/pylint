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

import pytest

from pylint import config


RE_PATTERN_TYPE = getattr(re, 'Pattern', getattr(re, '_pattern_type', None))


def test__regexp_validator_valid():
    result = config.VALIDATORS['regex']("test_.*")
    assert isinstance(result, RE_PATTERN_TYPE)
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
        assert isinstance(regex, RE_PATTERN_TYPE)
        assert regex.pattern == pattern_strings[i]

def test__regexp_csv_validator_invalid():
    pattern_strings = ["test_.*", "foo\\.bar", "^baz)$"]
    with pytest.raises(sre_constants.error):
        config.VALIDATORS['regexp_csv'](",".join(pattern_strings))


@pytest.mark.comments
def test_make_commenter():
    """Test make_commenter."""
    commenter = config.make_commenter(
        (
            'This is a long description, I am trying to test wrapping '
            'works OK. I hope this test passes.'
        )
    )
    match = re.match('^check ', 'check = hey')
    assert (
        commenter(match) ==
        (
            '# This is a long description, I am trying to test '
            'wrapping works OK. I\n'
            '# hope this test passes.\n'
            'check '
        )
    )


@pytest.mark.comments
def test_make_commented_config_text():
    """Test make_commented_config_text."""
    assert (
        config.make_commented_config_text(
            {
                'check': {'help': 'Check something.'},
                'validate': {'help': 'Validate a thing.'},
            },
            'check = 1\nvalidate=2\nother = 3'
        ) ==
        (
            '# Check something.\n'
            'check = 1\n'
            '# Validate a thing.\n'
            'validate=2\n'
            'other = 3'
        )
    )


@pytest.mark.comments
def test_write(tmpdir):
    """Test IniFileParser.write."""
    parser = config.IniFileParser()
    parser.add_option_definitions(
        (
            ('check', {'help': 'Check something.', 'group': 'checks'}),
        )
    )
    config_path = tmpdir.join('config.cfg')
    config_path.write('[checks]\ncheck = 1')
    parser.parse(str(config_path), config.Configuration())
    output_path = tmpdir.join('output.cfg')
    with output_path.open('w') as output:
        parser.write(stream=output)
    assert output_path.read() == '[CHECKS]\n# Check something.\ncheck = 1\n\n'
