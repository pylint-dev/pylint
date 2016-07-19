# Copyright (c) 2003-2016 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import sys
import unittest

from astroid import test_utils

from pylint.checkers import strings
from pylint.testutils import CheckerTestCase


class StringCheckerTest(CheckerTestCase):
    CHECKER_CLASS = strings.StringFormatChecker

    @unittest.skipUnless(sys.version_info > (3, 0),
                         "Tests that the string formatting checker "
                         "doesn't fail when encountering a bytes "
                         "string with a .format call")
    def test_format_bytes(self):
        code = "b'test'.format(1, 2)"
        node = test_utils.extract_node(code)
        with self.assertNoMessages():
            self.checker.visit_call(node)


if __name__ == '__main__':
    unittest.main()
