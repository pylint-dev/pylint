# -*- coding: utf-8 -*-
# Copyright (c) 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2013-2014, 2016 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

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
