# Copyright (c) 2003-2015 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import sys
import unittest

from astroid import test_utils

from pylint.checkers import strings
from pylint.testutils import CheckerTestCase


class StringCheckerTest(CheckerTestCase):
    CHECKER_CLASS = strings.StringMethodsChecker

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
