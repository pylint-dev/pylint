# Copyright (c) 2015-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2016-2017 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Damien Baty <damien.baty@polyconseil.fr>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the pylint checker in :mod:`pylint.extensions.check_elif
"""
from os import path as osp

import pytest

from pylint.extensions.check_elif import ElseifUsedChecker


@pytest.fixture(scope="module")
def checker():
    return ElseifUsedChecker


def test_elseif_message(linter):
    elif_test = osp.join(osp.dirname(osp.abspath(__file__)), "data", "elif.py")
    linter.check([elif_test])
    msgs = linter.reporter.messages
    assert len(msgs) == 2
    for msg in msgs:
        assert msg.symbol == "else-if-used"
        assert msg.msg == 'Consider using "elif" instead of "else if"'
    assert msgs[0].line == 9
    assert msgs[1].line == 21
