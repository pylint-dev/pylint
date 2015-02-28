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

import contextlib
import sys
import os
from os.path import join, dirname, abspath
import tempfile
import textwrap
import unittest

import six

from pylint.lint import Run
from pylint.reporters import BaseReporter
from pylint.reporters.text import *
from pylint.reporters.html import HTMLReporter
from pylint.reporters.json import JSONReporter

HERE = abspath(dirname(__file__))



@contextlib.contextmanager
def _patch_streams(out):
    sys.stderr = sys.stdout = out
    try:
        yield
    finally:
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__


class MultiReporter(BaseReporter):
    def __init__(self, reporters):
        self._reporters = reporters
        self.path_strip_prefix = os.getcwd() + os.sep

    def on_set_current_module(self, *args, **kwargs):
        for rep in self._reporters:
            rep.on_set_current_module(*args, **kwargs)

    def handle_message(self, msg):
        for rep in self._reporters:
            rep.handle_message(msg)

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
            out = six.StringIO()
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

    def _test_output(self, args, expected_output):
        out = six.StringIO()
        with _patch_streams(out):
            with self.assertRaises(SystemExit):
                Run(args)

            actual_output = out.getvalue()
            self.assertEqual(expected_output.strip(), actual_output.strip())

    def test_pkginfo(self):
        """Make pylint check itself."""
        self._runtest(['pylint.__pkginfo__'], reporter=TextReporter(six.StringIO()),
                      code=0)

    def test_all(self):
        """Make pylint check itself."""
        reporters = [
            TextReporter(six.StringIO()),
            HTMLReporter(six.StringIO()),
            ColorizedTextReporter(six.StringIO()),
            JSONReporter(six.StringIO())
        ]
        self._runtest(['pylint/test/functional/arguments.py'],
                      reporter=MultiReporter(reporters), code=1)

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
            strio = six.StringIO()
        assert strio.encoding is None
        self._runtest([join(HERE, 'regrtest_data/no_stdout_encoding.py')],
                      out=strio)

    def test_parallel_execution(self):
        self._runtest(['-j 2', 'pylint/test/functional/arguments.py',
                       'pylint/test/functional/bad_continuation.py'], code=1)

    def test_parallel_execution_missing_arguments(self):
        self._runtest(['-j 2', 'not_here', 'not_here_too'], code=1)

    def test_py3k_option(self):
        # Test that --py3k flag works.
        rc_code = 2 if six.PY2 else 0
        self._runtest([join(HERE, 'functional', 'unpacked_exceptions.py'),
                       '--py3k'],
                      code=rc_code)

    def test_py3k_jobs_option(self):
        rc_code = 2 if six.PY2 else 0
        self._runtest([join(HERE, 'functional', 'unpacked_exceptions.py'),
                       '--py3k', '-j 2'],
                      code=rc_code)

    @unittest.skipIf(sys.version_info[0] > 2, "Requires the --py3k flag.")
    def test_py3k_commutative_with_errors_only(self):

        # Test what gets emitted with -E only
        module = join(HERE, 'regrtest_data', 'py3k_error_flag.py')
        expected = textwrap.dedent("""
        No config file found, using default configuration
        ************* Module py3k_error_flag
        Explicit return in __init__
        """)
        self._test_output([module, "-E", "--msg-template='{msg}'"],
                          expected_output=expected)

        # Test what gets emitted with -E --py3k
        expected = textwrap.dedent("""
        No config file found, using default configuration
        ************* Module py3k_error_flag
        Use raise ErrorClass(args) instead of raise ErrorClass, args.
        """)
        self._test_output([module, "-E", "--py3k", "--msg-template='{msg}'"],
                          expected_output=expected)

        # Test what gets emitted with --py3k -E
        self._test_output([module, "--py3k", "-E", "--msg-template='{msg}'"],
                          expected_output=expected)


if __name__ == '__main__':
    unittest.main()
