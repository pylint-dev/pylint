# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt
"""
Unit tests specifically targeting PyLinter._discover_files() and its use of
the os.walk() function.
"""

import os
import platform
import subprocess
from collections.abc import Generator, Iterator
from pathlib import Path
from typing import Any
from unittest import mock

import pytest

from pylint.lint import PyLinter


@pytest.fixture(name="initialized_linter")
def _initialized_linter(linter: PyLinter) -> PyLinter:
    linter.open()

    return linter


@pytest.fixture(name="setup_test_file_tree")
def _setup_test_file_tree(tmp_path: Path) -> Generator[Path]:
    """
    Produce a standardized fake file system for testing _discover_files() using
    a list of files.
    """
    # A list of file names (represented by strings) and symlinks (represented
    # by a sub-list containing the name and what it points to).
    tree = [
        "test/manage.py",
        "test/pyproject.toml",
        "test/applications/static/applications/js/applications.js",
        "test/applications/static/applications/css/applications.css",
        "test/applications/views.py",
        "test/applications/management/commands/__init__.py",
        "test/applications/management/__init__.py",
        "test/applications/models.py",
        "test/applications/admin.py",
        "test/applications/apps.py",
        "test/applications/templates/ApplicationDetails.html",
        "test/applications/templates/ApplicationList.html",
        "test/applications/tests/__init__.py",
        "test/applications/tests/test_models.py",
        "test/applications/tests/test_unauthenticated_user.py",
        "test/applications/tests/test_authenticated_user.py",
        "test/applications/migrations/0003_alter_jobapplication_posting.py",
        "test/applications/migrations/__init__.py",
        "test/applications/migrations/0002_alter_jobapplication_user.py",
        "test/applications/migrations/0001_initial.py",
        "test/applications/migrations/__pycache__/0004_jobapplication_created_at_cpython-313.pyc",
        "test/applications/migrations/__pycache__/0002_alter_jobapplication_when.cpython-313.pyc",
        "test/applications/migrations/__pycache__/0002_alter_jobapplication_user_id.cpython-313.pyc",
        "test/applications/migrations/__pycache__/__init__.cpython-313.pyc",
        "test/applications/migrations/__pycache__/0001_initial.cpython-313.pyc",
        "test/applications/urls.py",
        "test/applications/__init__.py",
        "test/applications/forms.py",
        ["test/.venv/bin/python", "test/.venv/bin/python3.13"],
        ["test/.venv/bin/python3", "test/.venv/bin/python3.13"],
        ["test/.venv/bin/python3.13", "/usr/bin/python3.13"],
        "test/.venv/bin/pytest",
        "test/.venv/bin/pylint",
        "test/.venv/bin/pip",
        "test/.venv/bin/pip3",
        "test/.venv/bin/pip3.13",
        "test/.venv/lib/python3.13/site-packages/package_a",
        "test/.venv/lib/python3.13/site-packages/package_b",
        "test/applications_api/tests/test_unauthenticated_user.py",
        "test/applications_api/tests/__init__.py",
        "test/applications_api/tests/fixtures/job_applications.json",
        "test/applications_api/tests/test_authenticated_user.py",
        "test/applications_api/views.py",
        "test/applications_api/serializers.py",
        "test/applications_api/__init__.py",
        "test/applications_api/apps.py",
        "test/applications_api/admin.py",
        "test/applications_api/urls.py",
        "test/applications_api/models.py",
        "test/applications_api/migrations/__init__.py",
        "test/node_modules/node-package-a/file",
        "test/node_modules/node-package-b/file",
    ]

    # Save the current working directory
    original_cwd = os.getcwd()

    # Setup our directory tree
    for f in tree:
        linkto = None
        if isinstance(f, list):
            path = tmp_path / f[0]
            linkto = tmp_path / f[1]
        else:
            path = tmp_path / str(f)

        # Create parent directories if they don't exist.
        path.parent.mkdir(parents=True, exist_ok=True)

        if linkto:
            path.symlink_to(linkto)
        else:
            path.touch()

    # Change directory into our new test directory
    os.chdir(tmp_path / "test")

    # Run the test.
    yield tmp_path

    # Return to the original directory
    os.chdir(original_cwd)


@pytest.mark.usefixtures("setup_test_file_tree")
def test_does_not_ignore_similarly_named_package(
    initialized_linter: PyLinter,
) -> None:
    """
    Test to see if we return the expected package/file list even if a shorter named package is processed
    first and does not match an ignore config value.
    """
    # Variables used by debug_walk.
    os_walk_visited: list[str] = []
    orig_walk = os.walk

    def debug_walk(
        top: str, **kwargs: Any
    ) -> Iterator[tuple[str, list[str], list[str]]]:
        """
        Wrap the original os.walk generator function so that we can inspect the
        values returned for `dirpath`, which will tell us which directories have
        been visited.

        NOTE: This method is necessary since due to the nature of os.walk,
        and it being a generator, neither unittest's mock.patch or pytest's
        mocker.spy give us access to the values returned.

        WARNING: Rather than make this and its associated variables file-level
        globals, duplicate them to avoid potential parallel execution issues
        in the future.
        """
        for dirpath, dirnames, filenames in orig_walk(top, **kwargs):
            os_walk_visited.append(dirpath)

            yield dirpath, dirnames, filenames

    with mock.patch("os.walk", side_effect=debug_walk) as mock_walk:
        results = tuple(initialized_linter._discover_files(["."]))
        mock_walk.assert_called_with(".", topdown=True)

    # Create our OS specific paths for applications and applications_api directories
    applications_path = f".{os.sep}applications"
    applications_api_path = f".{os.sep}applications_api"

    # Make sure that the OS has not re-ordered their order on how we visited
    # them, capturing extra diagnostics if the assertion fails.
    try:
        assert os_walk_visited.index(applications_path) < os_walk_visited.index(
            applications_api_path
        ), "os.walk() traversed the tree in an unexpected order..."
    except AssertionError as e:

        # Warn that this is a possible false failure caused by the fact that
        # `os.warn()` relies on the underlying file system for determining the
        # order for the entries in a directory.
        #
        # Just double-check the order of the entries in the `tree` list in the
        # `setup_test_file_tree()` fixture to make sure that `applications_api`
        # entries come after those for `applications`.
        print("This is a possible false error, due to the nature of os.walk()... see the test for more info.")

        # Collect some additional diagnostics
        if platform.system() != "Windows":
            print("Additional diagnostics for unexpected os.walk() traversal...")
            subprocess.run(["ls", "-f"])
            subprocess.run(["df", "-Th", "."])
        else:
            print("Additional diagnostics are not available for this OS.")

        # Re-raise the assertion
        raise e

    # Assert that we got the correct results.
    assert len(results) == 3
    assert f".{os.sep}manage.py" in results
    assert applications_path in results
    assert applications_api_path in results


@pytest.mark.usefixtures("setup_test_file_tree")
def test_does_not_ignore_similarly_named_package_even_if_first_ignored(
    initialized_linter: PyLinter,
) -> None:
    """
    Test to see if we return the expected package/file list even if the shorter named package is processed
    first and matches an ignore config value.

    NOTE: manage.py could be ignored here, but it is ignored later in the call to expand_modules.
    """
    initialized_linter.config.ignore = [
        ".venv",
        "applications",
        "node_modules",
        "manage.py",
    ]

    # Variables used by debug_walk.
    os_walk_visited: list[str] = []
    orig_walk = os.walk

    def debug_walk(
        top: str, **kwargs: Any
    ) -> Iterator[tuple[str, list[str], list[str]]]:
        """
        Wrap the original os.walk generator function so that we can inspect the
        values returned for `dirpath`, which will tell us which directories have
        been visited.

        NOTE: This method is necessary since due to the nature of os.walk,
        and it being a generator, neither unittest's mock.patch or pytest's
        mocker.spy give us access to the values returned.

        WARNING: Rather than make this and its associated variables file-level
        globals, duplicate them to avoid potential parallel execution issues
        in the future.
        """
        for dirpath, dirnames, filenames in orig_walk(top, **kwargs):
            os_walk_visited.append(dirpath)

            yield dirpath, dirnames, filenames

    with mock.patch("os.walk", side_effect=debug_walk) as mock_walk:
        results = tuple(initialized_linter._discover_files(["."]))
        mock_walk.assert_called_with(".", topdown=True)

    # Create our OS specific paths for applications and applications_api directories
    applications_api_path = f".{os.sep}applications_api"

    # Assert that we got the correct results.
    assert len(results) == 2
    assert f".{os.sep}manage.py" in results
    assert applications_api_path in results


@pytest.mark.usefixtures("setup_test_file_tree")
def test_does_not_traverse_into_ignored_directories(
    initialized_linter: PyLinter,
) -> None:
    """
    Verify that _discover_files supplies the correct `topdown=True` argument
    and does not walk the directories which are to be ignored.

    NOTE: manage.py could be ignored here, but it is ignored later in the call to expand_modules.
    """
    initialized_linter.config.ignore = [
        ".venv",
        "applications",
        "node_modules",
        "manage.py",
    ]

    # Variables used by debug_walk.
    os_walk_visited: list[str] = []
    orig_walk = os.walk

    def debug_walk(
        top: str, **kwargs: Any
    ) -> Iterator[tuple[str, list[str], list[str]]]:
        """
        Wrap the original os.walk generator function so that we can inspect the
        values returned for `dirpath`, which will tell us which directories have
        been visited.

        NOTE: This method is necessary since due to the nature of os.walk,
        and it being a generator, neither unittest's mock.patch or pytest's
        mocker.spy give us access to the values returned.

        WARNING: Rather than make this and its associated variables file-level
        globals, duplicate them to avoid potential parallel execution issues
        in the future.
        """
        for dirpath, dirnames, filenames in orig_walk(top, **kwargs):
            os_walk_visited.append(dirpath)

            yield dirpath, dirnames, filenames

    with mock.patch("os.walk", side_effect=debug_walk) as mock_walk:
        results = tuple(initialized_linter._discover_files(["."]))
        mock_walk.assert_called_with(".", topdown=True)

    # Create our OS specific paths for applications and applications_api directories
    applications_path = f".{os.sep}applications"
    applications_api_path = f".{os.sep}applications_api"

    # Assert that we got the correct results.
    assert len(results) == 2
    assert f".{os.sep}manage.py" in results
    assert applications_api_path in results

    # Assert that we did not traverse into ignored directories
    assert applications_path not in os_walk_visited
    assert f".{os.sep}.venv" not in os_walk_visited
    assert f".{os.sep}.venv{os.sep}bin" not in os_walk_visited
    assert f".{os.sep}node_modules" not in os_walk_visited
    assert f".{os.sep}node_modules{os.sep}node-package-a" not in os_walk_visited
    assert f".{os.sep}node_modules{os.sep}node-package-b" not in os_walk_visited
