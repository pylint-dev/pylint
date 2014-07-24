# Copyright (c) 2003-2014 LOGILAB S.A. (Paris, FRANCE).
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

import os
from os.path import join, dirname, abspath
from cStringIO import StringIO

from logilab.common.testlib import TestCase, unittest_main

from pylint.lint import PyLinter
from pylint import checkers
from pylint.reporters.text import TextReporter

HERE = abspath(dirname(__file__))
INPUTDIR = join(HERE, 'input')

class PyLinterTC(TestCase):

    def setUp(self):
        self.linter = PyLinter(reporter=TextReporter())
        self.linter.disable('I')
        self.linter.config.persistent = 0
        # register checkers
        checkers.initialize(self.linter)
        os.environ.pop('PYLINTRC', None)

    def test_template_option(self):
        output = StringIO()
        self.linter.reporter.set_output(output)
        self.linter.set_option('msg-template', '{msg_id}:{line:03d}')
        self.linter.open()
        self.linter.set_current_module('0123')
        self.linter.add_message('C0301', line=1, args=(1, 2))
        self.linter.add_message('line-too-long', line=2, args=(3, 4))
        self.assertMultiLineEqual(output.getvalue(),
                                  '************* Module 0123\n'
                                  'C0301:001\n'
                                  'C0301:002\n')


if __name__ == '__main__':
    unittest_main()
