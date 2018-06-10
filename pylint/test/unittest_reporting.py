# Copyright (c) 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Calin Don <calin.don@gmail.com>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016-2017 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import warnings

from io import StringIO

import pylint.config
from pylint.lint import PluginRegistry, PyLinter
from pylint import checkers
from pylint.reporters.text import TextReporter
import pytest


@pytest.fixture(scope='module')
def reporter(reporter):
    return TextReporter


@pytest.fixture(scope='module')
def disable(disable):
    return ['I']


def test_template_option(linter):
    output = StringIO()
    linter.reporter.set_output(output)
    linter.set_option('msg-template', '{msg_id}:{line:03d}')
    linter.open()
    linter.set_current_module('0123')
    linter.add_message('C0301', line=1, args=(1, 2))
    linter.add_message('line-too-long', line=2, args=(3, 4))
    assert output.getvalue() == \
        '************* Module 0123\n' \
        'C0301:001\n' \
        'C0301:002\n'


def test_display_results_is_renamed():
    class CustomReporter(TextReporter):
        def _display(self, layout):
            return None

    reporter = CustomReporter()
    with pytest.raises(AttributeError):
        reporter.display_results
