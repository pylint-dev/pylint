from __future__ import annotations

import os
import sys
from collections.abc import Callable
from os.path import abspath, dirname, join

from pylint import checkers
from pylint.lint.pylinter import PyLinter
from pylint.testutils import GenericTestReporter

REGR_DATA = join(dirname(abspath(__file__)), "regrtest_data")
sys.path.insert(1, REGR_DATA)


def Equals(expected: str) -> Callable[[str], bool]:
    return lambda got: got == expected


def test_package() -> None:
    for file_names, check in [
        (["package.__init__"], Equals("")),
        (["precedence_test"], Equals("")),
        (["import_package_subpackage_module"], Equals("")),
        (["pylint.checkers.__init__"], lambda x: "__path__" not in x),
        ([join(REGR_DATA, "classdoc_usage.py")], Equals("")),
        ([join(REGR_DATA, "module_global.py")], Equals("")),
        ([join(REGR_DATA, "decimal_inference.py")], Equals("")),
        ([join(REGR_DATA, "absimp", "string.py")], Equals("")),
        ([join(REGR_DATA, "bad_package")], lambda x: "Unused import missing" in x),
    ]:
        finalize_linter = PyLinter()
        finalize_linter.set_reporter(GenericTestReporter())
        checkers.initialize(finalize_linter)
        os.environ.pop("PYLINTRC", None)
        finalize_linter.reporter.finalize()
        finalize_linter.check(file_names)
        got = finalize_linter.reporter.finalize().strip()
        assert check(got), str(got) + str(check)
        print(f"Checked {file_names} successfully")


if __name__ == "__main__":
    test_package()
