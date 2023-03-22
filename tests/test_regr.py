# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Non regression tests for pylint, which requires a too specific configuration
to be incorporated in the automatic functional test framework
"""

# pylint: disable=redefined-outer-name

from __future__ import annotations

import os
import sys
from collections.abc import Callable, Iterator
from os.path import abspath, dirname, join
from typing import cast

import pytest

from pylint import testutils
from pylint.lint.pylinter import PyLinter

REGR_DATA = join(dirname(abspath(__file__)), "regrtest_data")
sys.path.insert(1, REGR_DATA)


@pytest.fixture(scope="module")
def reporter() -> type[testutils.GenericTestReporter]:
    return testutils.GenericTestReporter


@pytest.fixture(scope="module")
def disable() -> list[str]:
    return ["I"]


@pytest.fixture
def finalize_linter(linter: PyLinter) -> Iterator[PyLinter]:
    """Call reporter.finalize() to clean up pending messages if a test
    finished badly.
    """
    yield linter
    linter.reporter = cast(  # Due to fixture
        testutils.GenericTestReporter, linter.reporter
    )
    linter.reporter.finalize()


def Equals(expected: str) -> Callable[[str], bool]:
    return lambda got: got == expected


@pytest.mark.parametrize(
    "file_names, check",
    [
        (["package.__init__"], Equals("")),
        (["precedence_test"], Equals("")),
        (["import_package_subpackage_module"], Equals("")),
        (["pylint.checkers.__init__"], lambda x: "__path__" not in x),
        ([join(REGR_DATA, "classdoc_usage.py")], Equals("")),
        ([join(REGR_DATA, "module_global.py")], Equals("")),
        ([join(REGR_DATA, "decimal_inference.py")], Equals("")),
        ([join(REGR_DATA, "absimp", "string.py")], Equals("")),
        ([join(REGR_DATA, "bad_package")], lambda x: "Unused import missing" in x),
    ],
)
def test_package(
    finalize_linter: PyLinter, file_names: list[str], check: Callable[[str], bool]
) -> None:
    finalize_linter.check(file_names)
    finalize_linter.reporter = cast(  # Due to fixture
        testutils.GenericTestReporter, finalize_linter.reporter
    )
    got = finalize_linter.reporter.finalize().strip()
    assert check(got)


@pytest.mark.parametrize(
    "file_names",
    [
        [join(REGR_DATA, "import_assign.py")],
        [join(REGR_DATA, "special_attr_scope_lookup_crash.py")],
        [join(REGR_DATA, "try_finally_disable_msg_crash")],
    ],
)
def test_crash(finalize_linter: PyLinter, file_names: list[str]) -> None:
    finalize_linter.check(file_names)


@pytest.mark.parametrize(
    "fname", [x for x in os.listdir(REGR_DATA) if x.endswith("_crash.py")]
)
def test_descriptor_crash(fname: str, finalize_linter: PyLinter) -> None:
    finalize_linter.check([join(REGR_DATA, fname)])
    finalize_linter.reporter = cast(  # Due to fixture
        testutils.GenericTestReporter, finalize_linter.reporter
    )
    finalize_linter.reporter.finalize().strip()


@pytest.fixture
def modify_path() -> Iterator[None]:
    cwd = os.getcwd()
    sys.path.insert(0, "")
    yield
    sys.path.pop(0)
    os.chdir(cwd)


@pytest.mark.usefixtures("modify_path")
def test_check_package___init__(finalize_linter: PyLinter) -> None:
    filename = ["package.__init__"]
    finalize_linter.check(filename)
    checked = list(finalize_linter.stats.by_module.keys())
    assert sorted(checked) == sorted(filename)

    os.chdir(join(REGR_DATA, "package"))
    finalize_linter.check(["__init__"])
    checked = list(finalize_linter.stats.by_module.keys())
    assert checked == ["__init__"]


@pytest.mark.timeout(30)
@pytest.mark.parametrize("file_names", ([join(REGR_DATA, "hang", "pkg4972.string")],))
def test_hang(finalize_linter: PyLinter, file_names: list[str]) -> None:
    finalize_linter.check(file_names)
