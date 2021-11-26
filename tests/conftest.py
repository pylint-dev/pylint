# pylint: disable=redefined-outer-name
import os
from pathlib import Path

import pytest

from pylint import checkers
from pylint.lint import PyLinter
from pylint.testutils import MinimalTestReporter


@pytest.fixture()
def tests_directory():
    return Path(__file__).parent


@pytest.fixture
def linter(checker, register, enable, disable, reporter):
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
def checker():
    return None


@pytest.fixture(scope="module")
def register():
    return None


@pytest.fixture(scope="module")
def enable():
    return None


@pytest.fixture(scope="module")
def disable():
    return None


@pytest.fixture(scope="module")
def reporter():
    return MinimalTestReporter


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--primer-stdlib",
        action="store_true",
        default=False,
        help="Run primer stdlib tests",
    )
    parser.addoption(
        "--primer-external",
        action="store_true",
        default=False,
        help="Run primer external tests",
    )


def pytest_collection_modifyitems(config, items) -> None:
    """Convert command line options to markers"""
    # Add skip_primer_stdlib mark
    if not config.getoption("--primer-external"):
        skip_primer_external = pytest.mark.skip(
            reason="need --primer-external option to run"
        )
        for item in items:
            if "primer_external" in item.keywords:
                item.add_marker(skip_primer_external)

    # Add skip_primer_stdlib mark
    if not config.getoption("--primer-stdlib"):
        skip_primer_stdlib = pytest.mark.skip(
            reason="need --primer-stdlib option to run"
        )
        for item in items:
            if "primer_stdlib" in item.keywords:
                item.add_marker(skip_primer_stdlib)
