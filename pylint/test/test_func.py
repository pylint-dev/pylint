# Copyright (c) 2003-2014 LOGILAB S.A. (Paris, FRANCE).
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
"""functional/non regression tests for pylint"""

import unittest
import sys
import re

from os import getcwd
from os.path import abspath, dirname, join

from pylint.testutils import (make_tests, LintTestUsingModule, LintTestUsingFile,
    LintTestUpdate, cb_test_gen, linter, test_reporter)

PY3K = sys.version_info >= (3, 0)

# Configure paths
INPUT_DIR = join(dirname(abspath(__file__)), 'input')
MSG_DIR = join(dirname(abspath(__file__)), 'messages')

# Classes

quote = "'" if sys.version_info >= (3, 3) else ''

class LintTestNonExistentModuleTC(LintTestUsingModule):
    module = 'nonexistent'
    _get_expected = lambda self: 'F:  1: No module named %snonexistent%s\n' % (quote, quote)


def gen_tests(filter_rgx):
    if UPDATE:
        callbacks = [cb_test_gen(LintTestUpdate)]
    else:
        callbacks = [cb_test_gen(LintTestUsingModule)]
    tests = make_tests(INPUT_DIR, MSG_DIR, filter_rgx, callbacks)
    if UPDATE:
        return tests

    if filter_rgx:
        is_to_run = re.compile(filter_rgx).search
    else:
        is_to_run = lambda x: 1

    if is_to_run('nonexistent'):
        tests.append(LintTestNonExistentModuleTC)

    assert len(tests) < 196, "Please do not add new test cases here."
    return tests

# Create suite

FILTER_RGX = None
UPDATE = False

def suite():
    return unittest.TestSuite([unittest.makeSuite(test, suiteClass=unittest.TestSuite)
                              for test in gen_tests(FILTER_RGX)])


def load_tests(loader, tests, pattern):
    return suite()


if __name__=='__main__':
    if '-u' in sys.argv:
        UPDATE = True
        sys.argv.remove('-u')

    if len(sys.argv) > 1:
        FILTER_RGX = sys.argv[1]
        del sys.argv[1]
    unittest.main(defaultTest='suite')
