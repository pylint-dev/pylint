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
"""
Tests for the misc checker.
"""
from __future__ import with_statement

import sys
import tempfile
import os
import contextlib

from astroid import test_utils
from pylint.checkers import misc
from pylint.testutils import CheckerTestCase, Message, set_config


@contextlib.contextmanager
def create_file_backed_module(code):
    # Can't use tempfile.NamedTemporaryFile here
    # because on Windows the file must be closed before writing to it,
    # see http://bugs.python.org/issue14243
    fd, tmp = tempfile.mkstemp()
    if sys.version_info >= (3, 0):
        # erff
        os.write(fd, bytes(code, 'ascii'))
    else:
        os.write(fd, code)

    try:
        module = test_utils.build_module(code)
        module.file = tmp
        yield module
    finally:
        os.close(fd)
        os.remove(tmp)


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
    from logilab.common.testlib import unittest_main
    unittest_main()
