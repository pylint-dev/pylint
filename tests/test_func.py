# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Functional/non regression tests for pylint."""

from __future__ import annotations

import re
import sys
from os.path import abspath, dirname, join

import pytest

from pylint.testutils import UPDATE_FILE, UPDATE_OPTION, _get_tests_info, linter
from pylint.testutils.reporter_for_tests import GenericTestReporter
from pylint.testutils.utils import _test_cwd

TESTS_DIR = dirname(abspath(__file__))
INPUT_DIR = join(TESTS_DIR, "input")
MSG_DIR = join(TESTS_DIR, "messages")


FILTER_RGX = None
INFO_TEST_RGX = re.compile(r"^func_i\d\d\d\d$")


def exception_str(
    self: Exception, ex: Exception  # pylint: disable=unused-argument
) -> str:
    """Function used to replace default __str__ method of exception instances
    This function is not typed because it is legacy code
    """
    return f"in {ex.file}\n:: {', '.join(ex.args)}"  # type: ignore[attr-defined] # Defined in the caller


class LintTestUsingModule:
    INPUT_DIR: str | None = None
    DEFAULT_PACKAGE = "input"
    package = DEFAULT_PACKAGE
    linter = linter
    module: str | None = None
    depends: list[tuple[str, str]] | None = None
    output: str | None = None

    def _test_functionality(self) -> None:
        if self.module:
            tocheck = [self.package + "." + self.module]
        if self.depends:
            tocheck += [
                self.package + f".{name.replace('.py', '')}" for name, _ in self.depends
            ]
        # given that TESTS_DIR could be treated as a namespace package
        # when under the current directory, cd to it so that "tests." is not
        # prepended to module names in the output of cyclic-import
        with _test_cwd(TESTS_DIR):
            self._test(tocheck)

    def _check_result(self, got: str) -> None:
        error_msg = (
            f"Wrong output for '{self.output}':\n"
            "You can update the expected output automatically with: '"
            f"python tests/test_func.py {UPDATE_OPTION}'\n\n"
        )
        assert self._get_expected() == got, error_msg

    def _test(self, tocheck: list[str]) -> None:
        if self.module and INFO_TEST_RGX.match(self.module):
            self.linter.enable("I")
        else:
            self.linter.disable("I")
        try:
            self.linter.check(tocheck)
        except Exception as ex:
            print(f"Exception: {ex} in {tocheck}:: {', '.join(ex.args)}")
            # This is legacy code we're trying to remove, not worth it to type correctly
            ex.file = tocheck  # type: ignore[attr-defined]
            print(ex)
            # This is legacy code we're trying to remove, not worth it to type correctly
            ex.__str__ = exception_str  # type: ignore[assignment]
            raise
        assert isinstance(self.linter.reporter, GenericTestReporter)
        self._check_result(self.linter.reporter.finalize())

    def _has_output(self) -> bool:
        return isinstance(self.module, str) and not self.module.startswith(
            "func_noerror_"
        )

    def _get_expected(self) -> str:
        if self._has_output() and self.output:
            with open(self.output, encoding="utf-8") as fobj:
                return fobj.read().strip() + "\n"
        else:
            return ""


class LintTestUpdate(LintTestUsingModule):
    def _check_result(self, got: str) -> None:
        if not self._has_output():
            return
        try:
            expected = self._get_expected()
        except OSError:
            expected = ""
        if got != expected:
            with open(self.output or "", "w", encoding="utf-8") as f:
                f.write(got)


def gen_tests(
    filter_rgx: str | re.Pattern[str] | None,
) -> list[tuple[str, str, list[tuple[str, str]]]]:
    if filter_rgx:
        is_to_run = re.compile(filter_rgx).search
    else:
        is_to_run = (  # noqa: E731, We're going to throw all this anyway
            lambda x: 1  # type: ignore[assignment] # pylint: disable=unnecessary-lambda-assignment
        )
    tests: list[tuple[str, str, list[tuple[str, str]]]] = []
    for module_file, messages_file in _get_tests_info(INPUT_DIR, MSG_DIR, "func_", ""):
        if not is_to_run(module_file) or module_file.endswith((".pyc", "$py.class")):
            continue
        base = module_file.replace(".py", "").split("_")[1]
        dependencies = _get_tests_info(INPUT_DIR, MSG_DIR, base, ".py")
        tests.append((module_file, messages_file, dependencies))
    if UPDATE_FILE.exists():
        return tests
    assert len(tests) < 13, "Please do not add new test cases here." + "\n".join(
        str(k) for k in tests if not k[2]
    )
    return tests


TEST_WITH_EXPECTED_DEPRECATION = ["func_excess_escapes.py"]


@pytest.mark.parametrize(
    "module_file,messages_file,dependencies",
    gen_tests(FILTER_RGX),
    ids=[o[0] for o in gen_tests(FILTER_RGX)],
)
def test_functionality(
    module_file: str,
    messages_file: str,
    dependencies: list[tuple[str, str]],
    recwarn: pytest.WarningsRecorder,
) -> None:
    __test_functionality(module_file, messages_file, dependencies)
    if recwarn.list:
        if module_file in TEST_WITH_EXPECTED_DEPRECATION and sys.version_info.minor > 5:
            assert any(
                "invalid escape sequence" in str(i.message)
                for i in recwarn.list
                if issubclass(i.category, DeprecationWarning)
            )


def __test_functionality(
    module_file: str, messages_file: str, dependencies: list[tuple[str, str]]
) -> None:
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
