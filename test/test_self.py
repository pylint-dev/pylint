# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import sys
from os.path import join, dirname, abspath
from cStringIO import StringIO
import tempfile
import unittest

from pylint.lint import Run
from pylint.reporters import BaseReporter
from pylint.reporters.text import *
from pylint.reporters.html import HTMLReporter

HERE = abspath(dirname(__file__))


class MultiReporter(BaseReporter):
    def __init__(self, reporters):
        self._reporters = reporters

    def on_set_current_module(self, *args, **kwargs):
        for rep in self._reporters:
            rep.on_set_current_module(*args, **kwargs)

    def add_message(self, *args, **kwargs):
        for rep in self._reporters:
            rep.add_message(*args, **kwargs)

    def display_results(self, layout):
        pass

    @property
    def out(self):
        return self._reporters[0].out

    @property
    def linter(self):
        return self._linter

    @linter.setter
    def linter(self, value):
        self._linter = value
        for rep in self._reporters:
            rep.linter = value


class RunTC(unittest.TestCase):

    def _runtest(self, args, reporter=None, out=None, code=28):
        if out is None:
            out = StringIO()
        try:
            sys.stderr = sys.stdout = out
            try:
                Run(args, reporter=reporter)
            except SystemExit as ex:
                if reporter:
                    output = reporter.out.getvalue()
                elif hasattr(out, 'getvalue'):
                    output = out.getvalue()
                else:
                    output = None
                msg = 'expected output status %s, got %s' % (code, ex.code)
                if output is not None:
                    msg = '%s. Below pylint output: \n%s' % (msg, output)
                self.assertEqual(ex.code, code, msg)
            else:
                self.fail('expected system exit')
        finally:
            sys.stderr = sys.__stderr__
            sys.stdout = sys.__stdout__

    def test_pkginfo(self):
        """Make pylint check itself."""
        self._runtest(['pylint.__pkginfo__'], reporter=TextReporter(StringIO()),
                      code=0)

    def test_all(self):
        """Make pylint check itself."""
        reporters = [
            TextReporter(StringIO()),
            HTMLReporter(StringIO()),
            ColorizedTextReporter(StringIO())
        ]
        self._runtest(['pylint.lint'], reporter=MultiReporter(reporters))

    def test_no_ext_file(self):
        self._runtest([join(HERE, 'input', 'noext')], code=0)

    def test_w0704_ignored(self):
        self._runtest([join(HERE, 'input', 'ignore_except_pass_by_default.py')], code=0)

    def test_generate_config_option(self):
        self._runtest(['--generate-rcfile'], code=0)

    def test_help_message_option(self):
        self._runtest(['--help-msg', 'W0101'], code=0)

    def test_error_help_message_option(self):
        self._runtest(['--help-msg', 'WX101'], code=0)

    def test_error_missing_arguments(self):
        self._runtest([], code=32)

    def test_no_out_encoding(self):
        """test redirection of stdout with non ascii caracters
        """
        #This test reproduces bug #48066 ; it happens when stdout is redirected
        # through '>' : the sys.stdout.encoding becomes then None, and if the
        # output contains non ascii, pylint will crash
        if sys.version_info < (3, 0):
            strio = tempfile.TemporaryFile()
        else:
            strio = StringIO()
        assert strio.encoding is None
        self._runtest([join(HERE, 'regrtest_data/no_stdout_encoding.py')],
                      out=strio)


if __name__ == '__main__':
    unittest.main()
