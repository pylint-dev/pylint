# Copyright (c) 2015-2018 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import astroid

from pylint.checkers import strings
from pylint.testutils import CheckerTestCase


class TestStringChecker(CheckerTestCase):
    CHECKER_CLASS = strings.StringFormatChecker

    def test_format_bytes(self):
        code = "b'test'.format(1, 2)"
        node = astroid.extract_node(code)
        with self.assertNoMessages():
            self.checker.visit_call(node)
