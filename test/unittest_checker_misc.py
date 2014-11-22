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
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""Tests for the misc checker."""

import unittest

from pylint.checkers import misc
from pylint.testutils import (
    CheckerTestCase, Message,
    set_config, create_file_backed_module,
)



class FixmeTest(CheckerTestCase):
    CHECKER_CLASS = misc.EncodingChecker

    def test_fixme(self):
        with create_file_backed_module(
            """a = 1
            # FIXME """) as module:
            with self.assertAddsMessages(
                Message(msg_id='fixme', line=2, args=u'FIXME')):
                self.checker.process_module(module)

    @set_config(notes=[])
    def test_empty_fixme_regex(self):
        with create_file_backed_module(
            """a = 1
            # fixme
            """) as module:
            with self.assertNoMessages():
                self.checker.process_module(module)


if __name__ == '__main__':
    unittest.main()
