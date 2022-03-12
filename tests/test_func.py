# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

"""Functional/non regression tests for pylint."""

import re
import sys
from os.path import abspath, dirname, join
from typing import List, Optional, Tuple

import pytest

from pylint.testutils import UPDATE_FILE, UPDATE_OPTION, _get_tests_info, linter

INPUT_DIR = join(dirname(abspath(__file__)), "input")
MSG_DIR = join(dirname(abspath(__file__)), "messages")


FILTER_RGX = None
INFO_TEST_RGX = re.compile(r"^func_i\d\d\d\d$")


def exception_str(self, ex) -> str:  # pylint: disable=unused-argument
    """Function used to replace default __str__ method of exception instances
    This function is not typed because it is legacy code
    """
    return f"in {ex.file}\n:: {', '.join(ex.args)}"


class LintTestUsingModule:
    INPUT_DIR: Optional[str] = None
    DEFAULT_PACKAGE = "input"
    package = DEFAULT_PACKAGE
    linter = linter
    module: Optional[str] = None
    depends: Optional[List[Tuple[str, str]]] = None
    output: Optional[str] = None

    def _test_functionality(self) -> None:
        if self.module:
            tocheck = [self.package + "." + self.module]
        if self.depends:
            tocheck += [
                self.package + f".{name.replace('.py', '')}" for name, _ in self.depends
            ]
        self._test(tocheck)

    def _check_result(self, got: str) -> None:
        error_msg = (
            f"Wrong output for '{self.output}':\n"
            "You can update the expected output automatically with: '"
            f"python tests/test_func.py {UPDATE_OPTION}'\n\n"
        )
        assert self._get_expected() == got, error_msg

    def _test(self, tocheck: List[str]) -> None:
        if self.module and INFO_TEST_RGX.match(self.module):
            self.linter.enable("I")
        else:
            self.linter.disable("I")
        try:
            self.linter.check(tocheck)
        except Exception as ex:
            print(f"Exception: {ex} in {tocheck}:: {'‚ '.join(ex.args)}")
            ex.file = tocheck  # type: ignore[attr-defined] # This is legacy code we're trying to remove, not worth it to type correctly
            print(ex)
            ex.__str__ = exception_str  # type: ignore[assignment] # This is legacy code we're trying to remove, impossible to type correctly
            raise
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
    def _check_result(self, got):
        if not self._has_output():
            return
        try:
            expected = self._get_expected()
        except OSError:
            expected = ""
        if got != expected:
            with open(self.output, "w", encoding="utf-8") as f:
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


def __test_functionality(
    module_file: str, messages_file: str, dependencies: List[Tuple[str, str]]
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
