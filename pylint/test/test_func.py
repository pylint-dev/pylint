# Copyright (c) 2006-2010, 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2014 Michal Nowikowski <godfryd@gmail.com>
# Copyright (c) 2014-2016 Claudiu Popa <pcmanticore@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""functional/non regression tests for pylint"""

import sys
import re

import pytest
from os.path import abspath, dirname, join

from pylint.testutils import _get_tests_info, linter

PY3K = sys.version_info >= (3, 0)
SYS_VERS_STR = '%d%d%d' % sys.version_info[:3]

# Configure paths
INPUT_DIR = join(dirname(abspath(__file__)), 'input')
MSG_DIR = join(dirname(abspath(__file__)), 'messages')

FILTER_RGX = None
UPDATE = False
INFO_TEST_RGX = re.compile(r'^func_i\d\d\d\d$')

# Classes

quote = "'" if sys.version_info >= (3, 3) else ''


def exception_str(self, ex): # pylint: disable=unused-argument
    """function used to replace default __str__ method of exception instances"""
    return 'in %s\n:: %s' % (ex.file, ', '.join(ex.args))


class LintTestUsingModule(object):
    INPUT_DIR = None
    DEFAULT_PACKAGE = 'input'
    package = DEFAULT_PACKAGE
    linter = linter
    module = None
    depends = None
    output = None
    _TEST_TYPE = 'module'

    # def runTest(self):
    #     # This is a hack to make ./test/test_func.py work under pytest.
    #     pass

    def _test_functionality(self):
        tocheck = [self.package+'.'+self.module]
        # pylint: disable=not-an-iterable; can't handle boolean checks for now
        if self.depends:
            tocheck += [self.package+'.%s' % name.replace('.py', '')
                        for name, _ in self.depends]
        self._test(tocheck)

    def _check_result(self, got):
        assert self._get_expected().strip()+'\n' == got.strip()+'\n'

    def _test(self, tocheck):
        if INFO_TEST_RGX.match(self.module):
            self.linter.enable('I')
        else:
            self.linter.disable('I')
        try:
            self.linter.check(tocheck)
        except Exception as ex:
            # need finalization to restore a correct state
            self.linter.reporter.finalize()
            ex.file = tocheck
            print(ex)
            ex.__str__ = exception_str
            raise
        self._check_result(self.linter.reporter.finalize())

    def _has_output(self):
        return not self.module.startswith('func_noerror_')

    def _get_expected(self):
        if self._has_output() and self.output:
            with open(self.output, 'U') as fobj:
                return fobj.read().strip() + '\n'
        else:
            return ''


class LintTestUpdate(LintTestUsingModule):

    _TEST_TYPE = 'update'

    def _check_result(self, got):
        if self._has_output():
            try:
                expected = self._get_expected()
            except IOError:
                expected = ''
            if got != expected:
                with open(self.output, 'w') as fobj:
                    fobj.write(got)


def gen_tests(filter_rgx):
    if filter_rgx:
        is_to_run = re.compile(filter_rgx).search
    else:
        is_to_run = lambda x: 1
    tests = []
    for module_file, messages_file in (
            _get_tests_info(INPUT_DIR, MSG_DIR, 'func_', '')
    ):
        if not is_to_run(module_file) or module_file.endswith(('.pyc', "$py.class")):
            continue
        base = module_file.replace('.py', '').split('_')[1]
        dependencies = _get_tests_info(INPUT_DIR, MSG_DIR, base, '.py')
        tests.append((module_file, messages_file, dependencies))

    if UPDATE:
        return tests

    assert len(tests) < 196, "Please do not add new test cases here."
    return tests


@pytest.mark.parametrize("module_file,messages_file,dependencies", gen_tests(FILTER_RGX),
                         ids=[o[0] for o in gen_tests(FILTER_RGX)])
def test_functionality(module_file, messages_file, dependencies,):

    LT = LintTestUpdate() if UPDATE else LintTestUsingModule()

    LT.module = module_file.replace('.py', '')
    LT.output = messages_file
    LT.depends = dependencies or None
    LT.INPUT_DIR = INPUT_DIR
    LT._test_functionality()

if __name__ == '__main__':
    if '-u' in sys.argv:
        UPDATE = True
        sys.argv.remove('-u')

    if len(sys.argv) > 1:
        FILTER_RGX = sys.argv[1]
        del sys.argv[1]
    pytest.main(sys.argv)
