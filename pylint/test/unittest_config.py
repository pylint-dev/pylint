# -*- coding: utf-8 -*-
# Copyright (c) 2015 Aru Sahni <arusahni@gmail.com>
# Copyright (c) 2016-2018 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2017 Ville Skyttä <ville.skytta@iki.fi>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unit tests for the config module."""

from argparse import Namespace
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
def test_make_set_args_default():
    """Test IniFileParser.make_set_args comments default values."""
    assert (
        list(config.IniFileParser.make_set_args(
            {
                'validate': {
                    'help': 'Validate something.',
                    'group': 'checks',
                    'default': 'strictly'
                }
            },
            Namespace(validate='strictly')
        )) ==
        [
            ('CHECKS', '# Validate something.'),
            ('CHECKS', '# validate', 'strictly'),
        ]
    )


@pytest.mark.comments
def test_make_set_args_long():
    """Test IniFileParser.make_set_args wraps long help comments."""
    assert (
        list(config.IniFileParser.make_set_args(
            {
                'check': {
                    'help': (
                        'Check something. I am continuing to type '
                        'because I want a long line to test multiline '
                        'comments.'
                    ),
                    'group': 'checks'
                }
            },
            Namespace(check='1')
        )) ==
        [
            (
                'CHECKS',
                (
                    '# Check something. I am continuing to type '
                    'because I want a long line to'
                )
            ),
            ('CHECKS', '# test multiline comments.'),
            ('CHECKS', 'check', '1'),
        ]
    )


@pytest.mark.comments
def test_make_set_args_csv():
    """Test IniFileParser.make_set_args writes multiline csv values."""
    assert (
        list(config.IniFileParser.make_set_args(
            {
                'assess': {
                    'help': 'Assess something.',
                    'group': 'checks',
                    'type': 'csv'
                }
            },
            Namespace(assess=['somewhat', 'completely'])
        )) ==
        [
            ('CHECKS', '# Assess something.'),
            ('CHECKS', 'assess', 'somewhat,\ncompletely'),
        ]
    )


@pytest.mark.comments
def test_make_set_args_comment_csv():
    """Test IniFileParser.make_set_args comments out every line."""
    assert (
        list(config.IniFileParser.make_set_args(
            {
                'confirm': {
                    'help': 'Confirm something.',
                    'group': 'checks',
                    'type': 'csv',
                    'default': ['present', 'accurate']
                }
            },
            Namespace(confirm=['present', 'accurate'])
        )) ==
        [
            ('CHECKS', '# Confirm something.'),
            ('CHECKS', '# confirm', 'present,\n# accurate'),
        ]
    )


@pytest.mark.comments
def test_write(tmpdir):
    """Test IniFileParser.write writes and INI file with comments."""
    parser = config.IniFileParser()
    parser.add_option_definitions(
        (
            (
                'check',
                {
                    'help': 'Check something.',
                    'group': 'checks'
                }
            ),
        )
    )
    config_path = tmpdir.join('config.cfg')
    config_path.write(
        '[CHECKS]\n'
        'check = 1'
    )
    parser.parse(str(config_path), config.Configuration())
    output_path = tmpdir.join('output.cfg')
    with output_path.open('w') as output:
        parser.write(stream=output)
    assert output_path.read() == (
        '[CHECKS]\n'
        '# Check something.\n'
        'check = 1\n'
        '\n'
    )
