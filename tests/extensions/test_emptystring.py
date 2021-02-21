# Copyright (c) 2016 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2016 Alexander Todorov <atodorov@otb.bg>
# Copyright (c) 2017-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2017 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Damien Baty <damien.baty@polyconseil.fr>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the pylint checker in :mod:`pylint.extensions.emptystring
"""
from os import path as osp

import pytest

from pylint.extensions.emptystring import CompareToEmptyStringChecker


@pytest.fixture(scope="module")
def checker():
    return CompareToEmptyStringChecker


@pytest.fixture(scope="module")
def disable():
    return ["I"]


def test_emptystring_message(linter):
    elif_test = osp.join(
        osp.dirname(osp.abspath(__file__)), "data", "empty_string_comparison.py"
    )
    linter.check([elif_test])
    msgs = linter.reporter.messages
    expected_lineno = [6, 9, 12, 15]
    assert len(msgs) == len(expected_lineno)
    for msg, lineno in zip(msgs, expected_lineno):
        assert msg.symbol == "compare-to-empty-string"
        assert msg.msg == "Avoid comparisons to empty string"
        assert msg.line == lineno
