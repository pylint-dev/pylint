# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import contextlib
import importlib
import os
import shutil
import sys
import tempfile
from collections.abc import Iterator
from pathlib import Path
from unittest import mock

import pytest
from pytest import CaptureFixture

from pylint import config, testutils
from pylint.config.find_default_config_files import (
    _cfg_or_ini_has_config,
    _toml_has_config,
)
from pylint.lint.run import Run


@pytest.fixture
def pop_pylintrc() -> None:
    """Remove the PYLINTRC environment variable."""
    os.environ.pop("PYLINTRC", None)


# pylint: disable=duplicate-code
if os.name == "java":
    if os.name == "nt":
        HOME = "USERPROFILE"
    else:
        HOME = "HOME"
elif sys.platform == "win32":
    HOME = "USERPROFILE"
else:
    HOME = "HOME"


@contextlib.contextmanager
def fake_home() -> Iterator[None]:
    """Fake a home directory."""
    folder = tempfile.mkdtemp("fake-home")
    old_home = os.environ.get(HOME)
    try:
        os.environ[HOME] = folder
        yield
    finally:
        os.environ.pop("PYLINTRC", "")
        if old_home is None:
            del os.environ[HOME]
        else:
            os.environ[HOME] = old_home
        shutil.rmtree(folder, ignore_errors=True)


# pylint: enable=duplicate-code


@contextlib.contextmanager
def tempdir() -> Iterator[str]:
    """Create a temp directory and change the current location to it.

    This is supposed to be used with a *with* statement.
    """
    tmp = tempfile.mkdtemp()

    # Get real path of tempfile, otherwise test fail on mac os x
    current_dir = os.getcwd()
    os.chdir(tmp)
    abs_tmp = os.path.abspath(".")

    try:
        yield abs_tmp
    finally:
        os.chdir(current_dir)
        shutil.rmtree(abs_tmp)


@pytest.mark.usefixtures("pop_pylintrc")
def test_pylintrc() -> None:
    """Test that the environment variable is checked for existence."""
    with fake_home():
        current_dir = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(sys.executable)))
        try:
            assert not list(config.find_default_config_files())
            os.environ["PYLINTRC"] = os.path.join(tempfile.gettempdir(), ".pylintrc")
            assert not list(config.find_default_config_files())
            os.environ["PYLINTRC"] = "."
            assert not list(config.find_default_config_files())
        finally:
            os.chdir(current_dir)
            importlib.reload(config)


@pytest.mark.usefixtures("pop_pylintrc")
def test_pylintrc_parentdir() -> None:
    """Test that the first pylintrc we find is the first parent directory."""
    # pylint: disable=duplicate-code
    with tempdir() as chroot:
        chroot_path = Path(chroot)
        testutils.create_files(
            [
                "a/pylintrc",
                "a/b/__init__.py",
                "a/b/pylintrc",
                "a/b/c/__init__.py",
                "a/b/c/d/__init__.py",
                "a/b/c/d/e/.pylintrc",
            ]
        )

        with fake_home():
            assert not list(config.find_default_config_files())

        results = {
            "a": chroot_path / "a" / "pylintrc",
            "a/b": chroot_path / "a" / "b" / "pylintrc",
            "a/b/c": chroot_path / "a" / "b" / "pylintrc",
            "a/b/c/d": chroot_path / "a" / "b" / "pylintrc",
            "a/b/c/d/e": chroot_path / "a" / "b" / "c" / "d" / "e" / ".pylintrc",
        }
        for basedir, expected in results.items():
            os.chdir(chroot_path / basedir)
            assert next(config.find_default_config_files()) == expected


@pytest.mark.usefixtures("pop_pylintrc")
def test_pylintrc_toml_parentdir() -> None:
    """Test that the first pylintrc.toml we find is the first parent directory."""
    # pylint: disable=duplicate-code
    with tempdir() as chroot:
        chroot_path = Path(chroot)
        files = [
            "a/pylintrc.toml",
            "a/b/__init__.py",
            "a/b/pylintrc.toml",
            "a/b/c/__init__.py",
            "a/b/c/d/__init__.py",
            "a/b/c/d/e/.pylintrc.toml",
        ]
        testutils.create_files(files)
        for config_file in files:
            if config_file.endswith("pylintrc.toml"):
                with open(config_file, "w", encoding="utf-8") as fd:
                    fd.write('[tool.pylint."messages control"]\n')

        with fake_home():
            assert not list(config.find_default_config_files())

        results = {
            "a": chroot_path / "a" / "pylintrc.toml",
            "a/b": chroot_path / "a" / "b" / "pylintrc.toml",
            "a/b/c": chroot_path / "a" / "b" / "pylintrc.toml",
            "a/b/c/d": chroot_path / "a" / "b" / "pylintrc.toml",
            "a/b/c/d/e": chroot_path / "a" / "b" / "c" / "d" / "e" / ".pylintrc.toml",
        }
        for basedir, expected in results.items():
            os.chdir(chroot_path / basedir)
            assert next(config.find_default_config_files()) == expected


@pytest.mark.usefixtures("pop_pylintrc")
def test_pyproject_toml_parentdir() -> None:
    """Test the search of pyproject.toml file in parent directories."""
    with tempdir() as chroot:
        with fake_home():
            chroot_path = Path(chroot)
            files = [
                "pyproject.toml",
                "git/pyproject.toml",
                "git/a/pyproject.toml",
                "git/a/.git",
                "git/a/b/c/__init__.py",
                "hg/pyproject.toml",
                "hg/a/pyproject.toml",
                "hg/a/.hg",
                "hg/a/b/c/__init__.py",
                "none/sub/__init__.py",
            ]
            testutils.create_files(files)
            for config_file in files:
                if config_file.endswith("pyproject.toml"):
                    with open(config_file, "w", encoding="utf-8") as fd:
                        fd.write('[tool.pylint."messages control"]\n')
            results = {
                "": chroot_path / "pyproject.toml",
                "git": chroot_path / "git" / "pyproject.toml",
                "git/a": chroot_path / "git" / "a" / "pyproject.toml",
                "git/a/b": chroot_path / "git" / "a" / "pyproject.toml",
                "git/a/b/c": chroot_path / "git" / "a" / "pyproject.toml",
                "hg": chroot_path / "hg" / "pyproject.toml",
                "hg/a": chroot_path / "hg" / "a" / "pyproject.toml",
                "hg/a/b": chroot_path / "hg" / "a" / "pyproject.toml",
                "hg/a/b/c": chroot_path / "hg" / "a" / "pyproject.toml",
                "none": chroot_path / "pyproject.toml",
                "none/sub": chroot_path / "pyproject.toml",
            }
            for basedir, expected in results.items():
                os.chdir(chroot_path / basedir)
                assert next(config.find_default_config_files(), None) == expected


@pytest.mark.usefixtures("pop_pylintrc")
def test_pylintrc_parentdir_no_package() -> None:
    """Test that we don't find a pylintrc in sub-packages."""
    with tempdir() as chroot:
        with fake_home():
            chroot_path = Path(chroot)
            testutils.create_files(
                ["a/pylintrc", "a/b/pylintrc", "a/b/c/d/__init__.py"]
            )
            results = {
                "a": chroot_path / "a" / "pylintrc",
                "a/b": chroot_path / "a" / "b" / "pylintrc",
                "a/b/c": None,
                "a/b/c/d": None,
            }
            for basedir, expected in results.items():
                os.chdir(chroot_path / basedir)
                assert next(config.find_default_config_files(), None) == expected


@pytest.mark.usefixtures("pop_pylintrc")
def test_verbose_output_no_config(capsys: CaptureFixture) -> None:
    """Test that we print a log message in verbose mode with no file."""
    with tempdir() as chroot:
        with fake_home():
            chroot_path = Path(chroot)
            testutils.create_files(["a/b/c/d/__init__.py"])
            os.chdir(chroot_path / "a/b/c")
            with pytest.raises(SystemExit):
                Run(["--verbose"])
            out = capsys.readouterr()
            assert "No config file found, using default configuration" in out.err


@pytest.mark.usefixtures("pop_pylintrc")
def test_verbose_abbreviation(capsys: CaptureFixture) -> None:
    """Test that we correctly handle an abbreviated pre-processable option."""
    with tempdir() as chroot:
        with fake_home():
            chroot_path = Path(chroot)
            testutils.create_files(["a/b/c/d/__init__.py"])
            os.chdir(chroot_path / "a/b/c")
            with pytest.raises(SystemExit):
                Run(["--ve"])
            out = capsys.readouterr()
            # This output only exists when launched in verbose mode
            assert "No config file found, using default configuration" in out.err


@pytest.mark.parametrize(
    "content,expected",
    [
        ["", False],
        ["(not toml valid)", False],
        [
            """
[build-system]
requires = ["setuptools ~= 58.0", "cython ~= 0.29.0"]
""",
            False,
        ],
        [
            """
[tool.pylint]
missing-member-hint = true
""",
            True,
        ],
    ],
)
def test_toml_has_config(content: str, expected: bool, tmp_path: Path) -> None:
    """Test that a toml file has a pylint config."""
    fake_toml = tmp_path / "fake.toml"
    with open(fake_toml, "w", encoding="utf8") as f:
        f.write(content)
    assert _toml_has_config(fake_toml) == expected


@pytest.mark.parametrize(
    "content,expected",
    [
        ["", False],
        ["(not valid .cfg)", False],
        [
            """
[metadata]
name = pylint
""",
            False,
        ],
        [
            """
[metadata]
name = pylint

[pylint.messages control]
disable = logging-not-lazy,logging-format-interpolation
""",
            True,
        ],
    ],
)
def test_has_config(content: str, expected: bool, tmp_path: Path) -> None:
    """Test that a .cfg file or .ini file has a pylint config."""
    for file_name in ("fake.cfg", "tox.ini"):
        fake_conf = tmp_path / file_name
        with open(fake_conf, "w", encoding="utf8") as f:
            f.write(content)
        assert _cfg_or_ini_has_config(fake_conf) == expected


def test_non_existent_home() -> None:
    """Test that we handle a non-existent home directory.

    Reported in https://github.com/pylint-dev/pylint/issues/6802.
    """
    with mock.patch("pathlib.Path.home", side_effect=RuntimeError):
        current_dir = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(sys.executable)))

        assert not list(config.find_default_config_files())

        os.chdir(current_dir)


def test_permission_error() -> None:
    """Test that we handle PermissionError correctly in find_default_config_files.

    Reported in https://github.com/pylint-dev/pylint/issues/7169.
    """
    with mock.patch("pathlib.Path.is_file", side_effect=PermissionError):
        list(config.find_default_config_files())
