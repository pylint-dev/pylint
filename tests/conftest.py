# pylint: disable=redefined-outer-name
# pylint: disable=no-name-in-module
import os
from unittest.mock import patch

import pytest

from pylint import checkers, testutils
from pylint.lint import PyLinter
from pylint.testutils import MinimalTestReporter

ORIG_ENVIRON = os.environ.copy()


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


@pytest.fixture(autouse=True)
def environ():
    """All tests get the same, fixed environ vars."""
    with patch.dict(os.environ, ORIG_ENVIRON, clear=True):
        yield os.environ


@pytest.fixture(autouse=True)
def cwd(tmp_path):
    """Each test gets its own, hermetic working dir."""
    with testutils.cwd(tmp_path):
        yield tmp_path
