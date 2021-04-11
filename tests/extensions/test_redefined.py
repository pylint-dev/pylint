# Copyright (c) 2016-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016-2017 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Damien Baty <damien.baty@polyconseil.fr>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""Tests for the pylint checker in :mod:`pylint.extensions.check_elif"""
from os import path as osp

import pytest

from pylint.extensions.redefined_variable_type import MultipleTypesChecker
from pylint.lint import fix_import_path

EXPECTED = [
    "Redefinition of self.var1 type from int to float",
    "Redefinition of a_str type from bool to float",
    "Redefinition of var type from int to str",
    "Redefinition of myint type from int to bool",
    "Redefinition of _OK type from bool to str",
    "Redefinition of instance type from redefined.MyClass to bool",
    "Redefinition of SOME_FLOAT type from float to int",
    "Redefinition of var3 type from str to int",
    "Redefinition of var type from bool to int",
    "Redefinition of var4 type from float to str",
]


@pytest.fixture(scope="module")
def checker():
    return MultipleTypesChecker


@pytest.fixture(scope="module")
def disable():
    return ["I"]


def test_types_redefined(linter):
    elif_test = osp.join(osp.dirname(osp.abspath(__file__)), "data", "redefined.py")
    with fix_import_path([elif_test]):
        linter.check([elif_test])
    msgs = sorted(linter.reporter.messages, key=lambda item: item.line)
    assert len(msgs) == 10
    for msg, expected in zip(msgs, EXPECTED):
        assert msg.symbol == "redefined-variable-type"
        assert msg.msg == expected
