# pylint: disable=redefined-outer-name
# pylint: disable=no-name-in-module
import os
import sys
from unittest.mock import patch

import pytest

from pylint import checkers, testutils
from pylint.lint import PyLinter
from pylint.testutils import MinimalTestReporter

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_PYLINTRC = os.path.join(REPO_ROOT, "pylintrc")
ORIG_ENVIRON = os.environ.copy()

if os.name == "java":
    # pylint: disable=no-member
    # os._name is valid see https://www.programcreek.com/python/example/3842/os._name
    if os._name == "nt":
        HOME = "USERPROFILE"
    else:
        HOME = "HOME"
elif sys.platform == "win32":
    HOME = "USERPROFILE"
else:
    HOME = "HOME"


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
def chroot(tmpdir):
    """Each test gets its own, hermetic working directory."""
    with testutils.cwd(tmpdir) as chroot:
        yield chroot


@pytest.fixture(scope="module")
def pylintrc_path():
    return REPO_PYLINTRC


@pytest.fixture()
@pytest.mark.usefixtures("fake_home")
def pylintrc(environ, pylintrc_path, fake_home):
    """Control which pylintrc is used."""
    del fake_home
    with patch.dict(environ, PYLINTRC=str(pylintrc_path)):
        # patch.dict has no facility for unsetting a key?
        if pylintrc_path is None:
            del environ["PYLINTRC"]
        yield pylintrc_path


@pytest.fixture
def fake_home(environ, chroot):
    environ[HOME] = str(chroot)
    yield
