# Copyright (c) 2006-2010, 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2012 FELD Boris <lothiraldan@gmail.com>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2014-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Michal Nowikowski <godfryd@gmail.com>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2017 Michka Popoff <michkapopoff@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""functional/non regression tests for pylint"""

import re
import sys
from os.path import abspath, dirname, join

import pytest

from pylint.testutils import UPDATE_FILE, UPDATE_OPTION, _get_tests_info, linter

# Configure paths
INPUT_DIR = join(dirname(abspath(__file__)), "input")
MSG_DIR = join(dirname(abspath(__file__)), "messages")


FILTER_RGX = None
INFO_TEST_RGX = re.compile(r"^func_i\d\d\d\d$")

# Classes


def exception_str(self, ex):  # pylint: disable=unused-argument
    """function used to replace default __str__ method of exception instances"""
    return "in {}\n:: {}".format(ex.file, ", ".join(ex.args))


class LintTestUsingModule:
    INPUT_DIR = None
    DEFAULT_PACKAGE = "input"
    package = DEFAULT_PACKAGE
    linter = linter
    module = None
    depends = None
    output = None

    def _test_functionality(self):
        tocheck = [self.package + "." + self.module]
        # pylint: disable=not-an-iterable; can't handle boolean checks for now
        if self.depends:
            tocheck += [
                self.package + ".%s" % name.replace(".py", "")
                for name, _ in self.depends
            ]
        self._test(tocheck)

    def _check_result(self, got):
        error_msg = (
            f"Wrong output for '{self.output}':\n"
            "You can update the expected output automatically with: '"
            f"python tests/test_func.py {UPDATE_OPTION}'\n\n"
        )
        assert self._get_expected() == got, error_msg

    def _test(self, tocheck):
        if INFO_TEST_RGX.match(self.module):
            self.linter.enable("I")
        else:
            self.linter.disable("I")
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
        return not self.module.startswith("func_noerror_")

    def _get_expected(self):
        if self._has_output() and self.output:
            with open(self.output) as fobj:
                return fobj.read().strip() + "\n"
        else:
            return ""


class LintTestUpdate(LintTestUsingModule):
    def _check_result(self, got):
        if not self._has_output():
            return
        try:
            expected = self._get_expected()
        except OSError:
            expected = ""
        if got != expected:
            with open(self.output, "w") as f:
                f.write(got)


def gen_tests(filter_rgx):
    if filter_rgx:
        is_to_run = re.compile(filter_rgx).search
    else:
        is_to_run = lambda x: 1  # noqa: E731 We're going to throw all this anyway
    tests = []
    for module_file, messages_file in _get_tests_info(INPUT_DIR, MSG_DIR, "func_", ""):
        if not is_to_run(module_file) or module_file.endswith((".pyc", "$py.class")):
            continue
        base = module_file.replace(".py", "").split("_")[1]
        dependencies = _get_tests_info(INPUT_DIR, MSG_DIR, base, ".py")
        tests.append((module_file, messages_file, dependencies))
    if UPDATE_FILE.exists():
        return tests
    assert len(tests) < 53, "Please do not add new test cases here."
    return tests


TEST_WITH_EXPECTED_DEPRECATION = ["func_excess_escapes.py"]


@pytest.mark.parametrize(
    "module_file,messages_file,dependencies",
    gen_tests(FILTER_RGX),
    ids=[o[0] for o in gen_tests(FILTER_RGX)],
)
def test_functionality(module_file, messages_file, dependencies, recwarn):
    __test_functionality(module_file, messages_file, dependencies)
    warning = None
    try:
        # Catch <unknown>:x: DeprecationWarning: invalid escape sequence
        # so it's not shown during tests
        warning = recwarn.pop()
    except AssertionError:
        pass
    if warning is not None:
        if module_file in TEST_WITH_EXPECTED_DEPRECATION and sys.version_info.minor > 5:
            assert issubclass(warning.category, DeprecationWarning)
            assert "invalid escape sequence" in str(warning.message)


def __test_functionality(module_file, messages_file, dependencies):
    lint_test = LintTestUpdate() if UPDATE_FILE.exists() else LintTestUsingModule()
    lint_test.module = module_file.replace(".py", "")
    lint_test.output = messages_file
    lint_test.depends = dependencies or None
    lint_test.INPUT_DIR = INPUT_DIR
    lint_test._test_functionality()


if __name__ == "__main__":
    if UPDATE_OPTION in sys.argv:
        UPDATE_FILE.touch()
        sys.argv.remove(UPDATE_OPTION)
    if len(sys.argv) > 1:
        FILTER_RGX = sys.argv[1]
        del sys.argv[1]
    try:
        pytest.main(sys.argv)
    finally:
        if UPDATE_FILE.exists():
            UPDATE_FILE.unlink()
