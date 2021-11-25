# Copyright (c) 2006-2011, 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2012 FELD Boris <lothiraldan@gmail.com>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016-2017 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Reverb C <reverbc@users.noreply.github.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Damien Baty <damien.baty@polyconseil.fr>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Andrew Haigh <hello@nelf.in>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""non regression tests for pylint, which requires a too specific configuration
to be incorporated in the automatic functional test framework
"""
# pylint: disable=redefined-outer-name

import os
import signal
import sys
from contextlib import contextmanager
from os.path import abspath, dirname, join
from typing import Callable, Iterator, List, cast

import astroid
import pytest

from pylint import testutils
from pylint.lint.pylinter import PyLinter

REGR_DATA = join(dirname(abspath(__file__)), "regrtest_data")
sys.path.insert(1, REGR_DATA)


@pytest.fixture(scope="module")
def reporter():
    return testutils.GenericTestReporter


@pytest.fixture(scope="module")
def disable():
    return ["I"]


@pytest.fixture
def finalize_linter(linter: PyLinter) -> Iterator[PyLinter]:
    """call reporter.finalize() to cleanup
    pending messages if a test finished badly
    """
    yield linter
    linter.reporter = cast(  # Due to fixture
        testutils.GenericTestReporter, linter.reporter
    )
    linter.reporter.finalize()


def Equals(expected):
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
    finalize_linter: PyLinter, file_names: List[str], check: Callable
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
def test_crash(finalize_linter: PyLinter, file_names: List[str]) -> None:
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
def modify_path() -> Iterator:
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


def test_pylint_config_attr() -> None:
    mod = astroid.MANAGER.ast_from_module_name("pylint.lint.pylinter")
    pylinter = mod["PyLinter"]
    expect = [
        "OptionsManagerMixIn",
        "object",
        "ReportsHandlerMixIn",
        "BaseTokenChecker",
        "BaseChecker",
        "OptionsProviderMixIn",
    ]
    assert [c.name for c in pylinter.ancestors()] == expect
    assert list(astroid.Instance(pylinter).getattr("config"))
    inferred = list(astroid.Instance(pylinter).igetattr("config"))
    assert len(inferred) == 1
    assert inferred[0].root().name == "optparse"
    assert inferred[0].name == "Values"


@contextmanager
def timeout(timeout_s: float):
    def _handle(_signum, _frame):
        pytest.fail("timed out")

    signal.signal(signal.SIGALRM, _handle)
    signal.setitimer(signal.ITIMER_REAL, timeout_s)
    yield
    signal.setitimer(signal.ITIMER_REAL, 0)
    signal.signal(signal.SIGALRM, signal.SIG_DFL)


@pytest.mark.skipif(not hasattr(signal, "setitimer"), reason="Assumes POSIX signals")
@pytest.mark.parametrize(
    "file_names,timeout_s",
    [
        ([join(REGR_DATA, "hang", "pkg4972.string")], 30.0),
    ],
)
def test_hang(
    finalize_linter: PyLinter, file_names: List[str], timeout_s: float
) -> None:
    with timeout(timeout_s):
        finalize_linter.check(file_names)
