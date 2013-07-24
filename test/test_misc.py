# Copyright 2013 Google Inc. All Rights Reserved.
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
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""
Tests for the misc checker.
"""

import tempfile

from logilab.common.testlib import unittest_main
from astroid import test_utils
from pylint.checkers import misc
from pylint.testutils import CheckerTestCase, Message


class FixmeTest(CheckerTestCase):
    CHECKER_CLASS = misc.EncodingChecker

    def create_file_backed_module(self, code):
        tmp = tempfile.NamedTemporaryFile()
        tmp.write(code)
        tmp.flush()
        module = test_utils.build_module(code)
        module.file = tmp.name
        # Just make sure to keep a reference to the file
        # so it isn't deleted.
        module._tmpfile = tmp
        return module

    def test_fixme(self):
        module = self.create_file_backed_module(
            """a = 1
            # FIXME
            """)
        with self.assertAddsMessages(
            Message(msg_id='W0511', line=2, args=u'FIXME')):
            self.checker.process_module(module)

    def test_emtpy_fixme_regex(self):
        self.checker.config.notes = []
        module = self.create_file_backed_module(
            """a = 1
            # fixme
            """)
        with self.assertNoMessages():
            self.checker.process_module(module)


if __name__ == '__main__':
    unittest_main()
