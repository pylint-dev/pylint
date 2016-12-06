# Copyright (c) 2016 Claudiu Popa <pcmanticore@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the pylint checker in :mod:`pylint.extensions.check_elif
"""

import os.path as osp

from pylint import checkers
from pylint.extensions.redefined_variable_type import MultipleTypesChecker
from pylint.lint import PyLinter, fix_import_path
from pylint.testutils import MinimalTestReporter


class TestCheckElseIfUsed(object):

    expected = [
        'Redefinition of self.var1 type from int to float',
        'Redefinition of var type from int to str',
        'Redefinition of myint type from int to bool',
        'Redefinition of _OK type from bool to str',
        'Redefinition of instance type from redefined.MyClass to bool',
        'Redefinition of SOME_FLOAT type from float to int',
        'Redefinition of var3 type from str to int',
        'Redefinition of var type from bool to int',
        'Redefinition of var4 type from float to str',
    ]

    @classmethod
    def setup_class(cls):
        cls._linter = PyLinter()
        cls._linter.set_reporter(MinimalTestReporter())
        checkers.initialize(cls._linter)
        cls._linter.register_checker(MultipleTypesChecker(cls._linter))
        cls._linter.disable('I')

    def test_types_redefined(self):
        elif_test = osp.join(osp.dirname(osp.abspath(__file__)), 'data',
                             'redefined.py')
        with fix_import_path([elif_test]):
            self._linter.check([elif_test])
        msgs = sorted(self._linter.reporter.messages, key=lambda item: item.line)
        assert len(msgs) == 9
        for msg, expected in zip(msgs, self.expected):
            assert msg.symbol == 'redefined-variable-type'
            assert msg.msg == expected


if __name__ == '__main__':
    import sys
    import pytest
    pytest.main(sys.argv)
