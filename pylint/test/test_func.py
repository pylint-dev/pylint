# -*- coding: utf-8 -*-
# Copyright (c) 2006-2010, 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2012 FELD Boris <lothiraldan@gmail.com>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2014-2016 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Michal Nowikowski <godfryd@gmail.com>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

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
