# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt
"""
Unit tests specifically targeting PyLinter._discover_files() and its use of
the os.walk() function.
"""

import os
from unittest import mock

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem, OSType

from pylint.lint import PyLinter


@pytest.fixture(name="initialized_linter")
def _initialized_linter(linter: PyLinter) -> PyLinter:
    linter.open()

    return linter


# pylint: disable=too-many-statements
def setup_mock_fs(fs: FakeFilesystem) -> FakeFilesystem:
    """
    Produce a standardized fake file system for testing _discover_files().

    NOTE: pyfakefs handles the mapping of Linux/macOS style names into Windows
    style names in the background for us.
    """
    fs.create_file("/test/manage.py")
    fs.create_file("/test/pyproject.toml")
    fs.create_file("/test/applications/static/applications/js/applications.js")
    fs.create_file("/test/applications/static/applications/css/applications.css")
    fs.create_file("/test/applications/views.py")
    fs.create_file("/test/applications/management/commands/__init__.py")
    fs.create_file("/test/applications/management/__init__.py")
    fs.create_file("/test/applications/models.py")
    fs.create_file("/test/applications/admin.py")
    fs.create_file("/test/applications/apps.py")
    fs.create_file("/test/applications/templates/ApplicationDetails.html")
    fs.create_file("/test/applications/templates/ApplicationList.html")
    fs.create_file("/test/applications/tests/__init__.py")
    fs.create_file("/test/applications/tests/test_models.py")
    fs.create_file("/test/applications/tests/test_unauthenticated_user.py")
    fs.create_file("/test/applications/tests/test_authenticated_user.py")
    fs.create_file("/test/applications/migrations/0003_alter_jobapplication_posting.py")
    fs.create_file("/test/applications/migrations/__init__.py")
    fs.create_file("/test/applications/migrations/0002_alter_jobapplication_user.py")
    fs.create_file("/test/applications/migrations/0001_initial.py")
    fs.create_file(
        "/test/applications/migrations/__pycache__/0004_jobapplication_created_at_cpython-313.pyc"
    )
    fs.create_file(
        "/test/applications/migrations/__pycache__/0002_alter_jobapplication_when.cpython-313.pyc"
    )
    fs.create_file(
        "/test/applications/migrations/__pycache__/0002_alter_jobapplication_user_id.cpython-313.pyc"
    )
    fs.create_file("/test/applications/migrations/__pycache__/__init__.cpython-313.pyc")
    fs.create_file(
        "/test/applications/migrations/__pycache__/0001_initial.cpython-313.pyc"
    )
    fs.create_file("/test/applications/urls.py")
    fs.create_file("/test/applications/__init__.py")
    fs.create_file("/test/applications/forms.py")
    fs.create_symlink("/test/.venv/bin/python", "/test/.venv/bin/python3.13")
    fs.create_symlink("/test/.venv/bin/python3", "/test/.venv/bin/python3.13")
    fs.create_symlink("/test/.venv/bin/python3.13", "/usr/bin/python3.13")
    fs.create_file("/test/.venv/bin/pytest")
    fs.create_file("/test/.venv/bin/pylint")
    fs.create_file("/test/.venv/bin/pip")
    fs.create_file("/test/.venv/bin/pip3")
    fs.create_file("/test/.venv/bin/pip3.13")
    fs.create_file("/test/.venv/lib/python3.13/site-packages/package_a")
    fs.create_file("/test/.venv/lib/python3.13/site-packages/package_b")
    fs.create_file("/test/applications_api/tests/test_unauthenticated_user.py")
    fs.create_file("/test/applications_api/tests/__init__.py")
    fs.create_file("/test/applications_api/tests/fixtures/job_applications.json")
    fs.create_file("/test/applications_api/tests/test_authenticated_user.py")
    fs.create_file("/test/applications_api/views.py")
    fs.create_file("/test/applications_api/serializers.py")
    fs.create_file("/test/applications_api/__init__.py")
    fs.create_file("/test/applications_api/apps.py")
    fs.create_file("/test/applications_api/admin.py")
    fs.create_file("/test/applications_api/urls.py")
    fs.create_file("/test/applications_api/models.py")
    fs.create_file("/test/applications_api/migrations/__init__.py")
    fs.create_file("/test/node_modules/node-package-a/file")
    fs.create_file("/test/node_modules/node-package-b/file")

    return fs


@pytest.mark.parametrize("os_type", [OSType.LINUX, OSType.WINDOWS, OSType.MACOS])
def test_does_not_ignore_similarly_named_package(
    initialized_linter: PyLinter,
    fs: FakeFilesystem,
    os_type: str,
) -> None:
    """
    Test to see if we return the expected package/file list even if a shorter named package is processed
    first and does not match an ignore config value.
    """
    # Set our fake OS type and then initialize our mock fs
    fs.os = os_type
    setup_mock_fs(fs)

    # This is affected by mock_fs, and changes the results.
    os.chdir(f"{os.sep}test")

    results = tuple(initialized_linter._discover_files(["."]))

    assert len(results) == 3
    assert f".{os.sep}manage.py" in results
    assert f".{os.sep}applications" in results
    assert f".{os.sep}applications_api" in results


@pytest.mark.parametrize("os_type", [OSType.LINUX, OSType.WINDOWS, OSType.MACOS])
def test_does_not_ignore_similarly_named_package_even_if_first_ignored(
    initialized_linter: PyLinter,
    fs: FakeFilesystem,
    os_type: str,
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

    # Set our fake OS type and then initialize our mock fs
    fs.os = os_type
    setup_mock_fs(fs)

    # This is affected by mock_fs, and affects the results.
    os.chdir(f"{os.sep}test")

    results = tuple(initialized_linter._discover_files(["."]))

    assert len(results) == 2
    assert f".{os.sep}manage.py" in results
    assert f".{os.sep}applications_api" in results


@pytest.mark.parametrize("os_type", [OSType.LINUX, OSType.WINDOWS, OSType.MACOS])
def test_does_not_traverse_into_ignored_directories(
    initialized_linter: PyLinter,
    fs: FakeFilesystem,
    os_type: str,
) -> None:
    """
    Verify that _discover_files supplies the correct "topdown=True" argument
    and does not walk the directories which are to be ignored.

    NOTE: manage.py could be ignored here, but it is ignored later in the call to expand_modules.
    """
    initialized_linter.config.ignore = [
        ".venv",
        "applications",
        "node_modules",
        "manage.py",
    ]

    # Set our fake OS type
    fs.os = os_type
    setup_mock_fs(fs)

    # This is affected by mock_fs, and changes the results.
    os.chdir(f"{os.sep}test")

    # Variables used by debug_walk.
    os_walk_visited: list[str] = []
    orig_walk = os.walk

    def debug_walk(top, **kwargs):
        """
        Wrap the original os.walk generator function so that we can inspect the
        values returned for dirpath, which will tell us which directories have
        been visited.

        NOTE: This method is necessary since due to the nature of os.walk,
        and it being a generator, neither unittest's mock.patch or Pytest's
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

    assert len(results) == 2
    assert f".{os.sep}manage.py" in results
    assert f".{os.sep}applications_api" in results

    assert f".{os.sep}.venv" not in os_walk_visited
    assert f".{os.sep}.venv{os.sep}bin" not in os_walk_visited
    assert f".{os.sep}node_modules" not in os_walk_visited
    assert f".{os.sep}node_modules{os.sep}node-package-a" not in os_walk_visited
    assert f".{os.sep}node_modules{os.sep}node-package-b" not in os_walk_visited
