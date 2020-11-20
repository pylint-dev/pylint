"""Show that conftest is doing its job(s)."""
import os
from tempfile import gettempdir

ENVVAR = "ENVVAR"
TEMPDIR = gettempdir()


class TestEnvironFixture:
    """Environment pollution doesn't survive cross tests."""

    def test_environ_polluter_1(self):
        assert ENVVAR not in os.environ
        os.environ[ENVVAR] = "1"
        assert ENVVAR in os.environ


class TestCwdFixture:
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
