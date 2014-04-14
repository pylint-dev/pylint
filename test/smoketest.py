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

from logilab.common.testlib import TestCase, unittest_main, tag

from pylint.lint import Run
from pylint.reporters.text import *
from pylint.reporters.html import HTMLReporter

HERE = abspath(dirname(__file__))

class RunTC(TestCase):

    def _runtest(self, args, reporter=None, out=None, code=28):
        if out is None:
            out = StringIO()
        if args and args[-1].startswith('pylint.lint'):
            try:
                import cProfile, pstats
            except ImportError:
                code += 1
        try:
            sys.stderr = sys.stdout = out
            try:
                Run(args, reporter=reporter)
            except SystemExit, ex:
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

    @tag('smoke')
    def test0(self):
        """make pylint checking itself"""
        self._runtest(['pylint.__pkginfo__'], reporter=TextReporter(StringIO()),
                      code=0)

    @tag('smoke')
    def test1(self):
        """make pylint checking itself"""
        self._runtest(['pylint.lint'], reporter=TextReporter(StringIO()))

    @tag('smoke')
    def test2(self):
        """make pylint checking itself"""
        self._runtest(['pylint.lint'], reporter=HTMLReporter(StringIO()))

    @tag('smoke')
    def test3(self):
        """make pylint checking itself"""
        self._runtest(['pylint.lint'], reporter=ColorizedTextReporter(StringIO()))

    @tag('smoke')
    def test_no_ext_file(self):
        self._runtest([join(HERE, 'input', 'noext')], code=0)

    @tag('smoke')
    def test_generated_members(self):
        # XXX dual end quotation since optparse buggily remove one...
        self._runtest(['--generated-members=objects,DoesNotExist,delay,retry,"[a-zA-Z]+_set{1,2}""', 'pylint.lint'])

    @tag('smoke')
    def test_w0704_ignored(self):
        self._runtest([join(HERE, 'input', 'ignore_except_pass_by_default.py')], code=0)

    @tag('smoke', 'help', 'config')
    def test_generate_config_option(self):
        """make pylint checking itself"""
        self._runtest(['--generate-rcfile'], reporter=HTMLReporter(StringIO()),
                      code=0)

    @tag('smoke', 'help')
    def test_help_message_option(self):
        """make pylint checking itself"""
        self._runtest(['--help-msg', 'W0101'], reporter=HTMLReporter(StringIO()),
                      code=0)

    @tag('smoke', 'help')
    def test_error_help_message_option(self):
        self._runtest(['--help-msg', 'WX101'], reporter=HTMLReporter(StringIO()),
                      code=0)

    @tag('smoke', 'usage')
    def test_error_missing_arguments(self):
        self._runtest([], reporter=HTMLReporter(StringIO()),
                      code=32)

    @tag('smoke', 'encoding')
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
    unittest_main()
