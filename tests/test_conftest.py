"""Show that conftest is doing its job(s)."""
import os
from tempfile import gettempdir

import pytest
from conftest import REPO_PYLINTRC

ENVVAR = "ENVVAR"
TEMPDIR = gettempdir()
UNSET = "UNSET"


class TestEnvironFixture:
    """Environment pollution doesn't survive cross tests."""

    def test_environ_polluter_1(self):
        assert ENVVAR not in os.environ
        os.environ[ENVVAR] = "1"
        assert ENVVAR in os.environ


class TestChrootFixture:
    """chdir pollution doesn't survive cross tests."""

    def test_cwd_polluter_1(self):
        assert os.getcwd() != TEMPDIR
        os.chdir(TEMPDIR)
        assert os.getcwd() == TEMPDIR

    test_cwd_polluter_2 = test_cwd_polluter_1

    def test_filesystem_polluter_1(self):
        assert not os.path.exists("afile.txt")
        with open("afile.txt", "w") as f:
            f.write("1")
        assert os.path.exists("afile.txt")

    test_filesystem_polluter_2 = test_filesystem_polluter_1


class TestPylintrcFixture:
    def test_it_sets_envvar(self, pylintrc):
        assert pylintrc == REPO_PYLINTRC
        assert pylintrc == os.environ["PYLINTRC"]

    @pytest.mark.parametrize("pylintrc_path", ["/my/pylintrc"])
    def test_it_can_be_configured(self, pylintrc):
        assert pylintrc == "/my/pylintrc"
        assert pylintrc == os.environ["PYLINTRC"]

    @pytest.mark.parametrize("pylintrc_path", [None])
    def test_it_can_be_unset(self, pylintrc):
        assert pylintrc is None
        assert os.environ.get("PYLINTRC", UNSET) is UNSET
