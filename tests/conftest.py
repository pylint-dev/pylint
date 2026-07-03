# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

# pylint: disable=redefined-outer-name

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path

import pytest

from pylint import checkers
from pylint.checkers import BaseChecker
from pylint.lint import PyLinter
from pylint.lint.run import _cpu_count
from pylint.reporters import BaseReporter
from pylint.testutils import MinimalTestReporter

HERE = Path(__file__).parent


@pytest.fixture()
def tests_directory() -> Path:
    return HERE


@pytest.fixture
def linter(
    checker: type[BaseChecker] | None,
    register: Callable[[PyLinter], None] | None,
    enable: str | None,
    disable: str | None,
    reporter: type[BaseReporter],
) -> PyLinter:
    _linter = PyLinter()
    _linter.set_reporter(reporter())
    checkers.initialize(_linter)
    if register:
        register(_linter)
    if checker:
        _linter.register_checker(checker(_linter))
    if disable:
        for msg in disable:
            _linter.disable(msg)
    if enable:
        for msg in enable:
            _linter.enable(msg)
    os.environ.pop("PYLINTRC", None)
    return _linter


@pytest.fixture(scope="module")
def checker() -> None:
    return None


@pytest.fixture(scope="module")
def register() -> None:
    return None


@pytest.fixture(scope="module")
def enable() -> None:
    return None


@pytest.fixture(scope="module")
def disable() -> None:
    return None


@pytest.fixture(scope="module")
def reporter() -> type[MinimalTestReporter]:
    return MinimalTestReporter


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--primer-stdlib",
        action="store_true",
        default=False,
        help="Run primer stdlib tests",
    )
    parser.addoption(
        "--minimal-messages-config",
        action="store_true",
        default=False,
        help=(
            "Disable all messages that are not explicitly expected when running functional tests. "
            "This is useful for finding problems with the @only_required_for_messages / @check_messages "
            "decorator, but can also produce false negatives if a functional test file only tests for "
            "false positive of messages and thus does not declare which messages are expected."
        ),
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Function]
) -> None:
    """Convert command line options to markers."""
    # Add skip_primer_stdlib mark
    if not config.getoption("--primer-stdlib"):
        skip_primer_stdlib = pytest.mark.skip(
            reason="need --primer-stdlib option to run"
        )
        for item in items:
            if "primer_stdlib" in item.keywords:
                item.add_marker(skip_primer_stdlib)

    # Add skip_cpu_cores mark
    if _cpu_count() < 2:
        skip_cpu_cores = pytest.mark.skip(
            reason="Need 2 or more cores for test to be meaningful"
        )
        for item in items:
            if "needs_two_cores" in item.keywords:
                item.add_marker(skip_cpu_cores)
