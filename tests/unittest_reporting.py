# Copyright (c) 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Calin Don <calin.don@gmail.com>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016-2017 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE
# pylint: disable=redefined-outer-name

import warnings
from io import StringIO

import pytest

from pylint import checkers
from pylint.lint import PyLinter
from pylint.reporters.text import ParseableTextReporter, TextReporter


@pytest.fixture(scope="module")
def reporter():
    return TextReporter


@pytest.fixture(scope="module")
def disable():
    return ["I"]


def test_template_option(linter):
    output = StringIO()
    linter.reporter.set_output(output)
    linter.set_option("msg-template", "{msg_id}:{line:03d}")
    linter.open()
    linter.set_current_module("0123")
    linter.add_message("C0301", line=1, args=(1, 2))
    linter.add_message("line-too-long", line=2, args=(3, 4))
    assert output.getvalue() == "************* Module 0123\nC0301:001\nC0301:002\n"


def test_parseable_output_deprecated():
    with warnings.catch_warnings(record=True) as cm:
        warnings.simplefilter("always")
        ParseableTextReporter()

    assert len(cm) == 1
    assert isinstance(cm[0].message, DeprecationWarning)


def test_parseable_output_regression():
    output = StringIO()
    with warnings.catch_warnings(record=True):
        linter = PyLinter(reporter=ParseableTextReporter())

    checkers.initialize(linter)
    linter.config.persistent = 0
    linter.reporter.set_output(output)
    linter.set_option("output-format", "parseable")
    linter.open()
    linter.set_current_module("0123")
    linter.add_message("line-too-long", line=1, args=(1, 2))
    assert (
        output.getvalue() == "************* Module 0123\n"
        "0123:1: [C0301(line-too-long), ] "
        "Line too long (1/2)\n"
    )


def test_display_results_is_renamed():
    class CustomReporter(TextReporter):
        def _display(self, layout):
            return None

    reporter = CustomReporter()
    with pytest.raises(AttributeError) as exc:
        # pylint: disable=no-member
        reporter.display_results()
    assert "no attribute 'display_results'" in str(exc)
