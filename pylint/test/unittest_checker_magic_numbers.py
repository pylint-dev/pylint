# Copyright (c) 2017 Lukasz Rogalski <rogalski.91@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Unittest for the magic numbers checker."""
import astroid

from pylint.checkers import magic_numbers
from pylint.testutils import CheckerTestCase, Message


class TestMagicNumbersChecker(CheckerTestCase):
    CHECKER_CLASS = magic_numbers.MagicNumberChecker

    def test_visit_re_call_posarg_simple(self):
        self._test_re_call('re.compile(pattern, 16)', ('re.DOTALL', '16'))
        self._test_re_call('re.search(pattern, string, 16)', ('re.DOTALL', '16'))
        self._test_re_call('re.match(pattern, string, 16)', ('re.DOTALL', '16'))
        self._test_re_call('re.split(pattern, string, 0, 16)', ('re.DOTALL', '16'))
        self._test_re_call('re.findall(pattern, string, 16)', ('re.DOTALL', '16'))
        self._test_re_call('re.finditer(pattern, string, 16)', ('re.DOTALL', '16'))
        self._test_re_call('re.sub(pattern, repl, string, 0, 16)', ('re.DOTALL', '16'))
        self._test_re_call('re.subn(pattern, repl, string, 0, 16)', ('re.DOTALL', '16'))

    def test_visit_re_call_kwarg_simple(self):
        self._test_re_call('re.compile(pattern, flags=16)', ('re.DOTALL', '16'))
        self._test_re_call('re.search(pattern, string, flags=16)', ('re.DOTALL', '16'))
        self._test_re_call('re.match(pattern, string, flags=16)', ('re.DOTALL', '16'))
        self._test_re_call('re.split(pattern, string, flags=16)', ('re.DOTALL', '16'))
        self._test_re_call('re.findall(pattern, string, flags=16)', ('re.DOTALL', '16'))
        self._test_re_call('re.finditer(pattern, string, flags=16)', ('re.DOTALL', '16'))
        self._test_re_call('re.sub(pattern, repl, string, flags=16)', ('re.DOTALL', '16'))
        self._test_re_call('re.subn(pattern, repl, string, flags=16)', ('re.DOTALL', '16'))

    def test_visit_re_flags_sum(self):
        self._test_re_call('re.compile(pattern, flags=80)', ('re.DOTALL | re.VERBOSE', '80'))

    def _test_re_call(self, call_as_string, expected_args):
        call = astroid.extract_node("""
        import re
        {}  #@
        """.format(call_as_string))
        with self.assertAddsMessages(Message('magic-number-used', node=call,
                                             args=expected_args)):
            self.checker.visit_call(call)

    def test_oserror_errno_compare_eq(self):
        compare = astroid.extract_node("""
        exc = OSError()
        exc.errno == 17  #@
        """)
        with self.assertAddsMessages(Message('magic-number-used', node=compare,
                                             args=('errno.EEXIST', '17'))):
            self.checker.visit_compare(compare)

    def test_oserror_errno_compare_in(self):
        compare = astroid.extract_node("""
        exc = OSError()
        exc.errno in (15, 17)  #@
        """)
        with self.assertAddsMessages(Message('magic-number-used', node=compare,
                                             args=('(errno.ENOTBLK, errno.EEXIST)', '(15, 17)'))):
            self.checker.visit_compare(compare)

    def test_oserror_errno_compare_notin(self):
        compare = astroid.extract_node("""
        exc = OSError()
        exc.errno in (15, 17)  #@
        """)
        with self.assertAddsMessages(Message('magic-number-used', node=compare,
                                             args=('(errno.ENOTBLK, errno.EEXIST)', '(15, 17)'))):
            self.checker.visit_compare(compare)
