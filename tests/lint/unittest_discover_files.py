# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from unittest import mock

import pytest

from pylint.lint import PyLinter


@pytest.fixture(name="initialized_linter")
def _initialized_linter(linter: PyLinter) -> PyLinter:
    linter.open()

    return linter


def mock_isdir(path: str) -> bool:
    """
    Mock of os.path.isdir() for the following tests:
    - test_discover_files_does_not_ignore_similarly_named_package
    - test_discover_files_does_not_ignore_similarly_named_package_even_if_first_is_ignored
    """
    if path == ".":
        return True
    raise ValueError(f"Not expecting an isdir call on {path}")


def mock_isfile(path: str) -> bool:
    """
    Mock of os.path.isfile() for the following tests:
    - test_discover_files_does_not_ignore_similarly_named_package
    - test_discover_files_does_not_ignore_similarly_named_package_even_if_first_is_ignored
    """
    if path == "./__init__.py":
        return False
    if path == "./manage.py":
        return True
    raise ValueError(f"Not expecting an isfile call on {path}")


@pytest.fixture(name="mock_tree")
def _mock_tree() -> list[tuple[str, list[str], list[str]]]:
    return [
        (
            ".",
            ["applications", "applications_api"],
            ["pyproject.toml", "manage.py"],
        ),
        (
            "./applications",
            ["tests"],
            ["views.py", "models.py", "admin.py", "apps.py", "__init__.py"],
        ),
        ("./applications/tests", [], ["test1.py", "test2.py", "__init__.py"]),
        (
            "./applications_api",
            ["tests"],
            ["views.py", "models.py", "admin.py", "apps.py", "__init__.py"],
        ),
        (
            "./applications_api/tests",
            [],
            ["test1.py", "test2.py", "__init__.py"],
        ),
    ]


def test_does_not_ignore_similarly_named_package(
        initialized_linter,
        mock_tree,
) -> None:
    """
    Test to see if we return the expected package/file list even if a shorter named package is processed
    first and does not match an ignore config value.
    """
    with mock.patch("os.walk") as mock_walk:
        with mock.patch.multiple(
                "os.path", isdir=mock.DEFAULT, isfile=mock.DEFAULT
        ) as mock_path:
            mock_walk.return_value = mock_tree
            mock_path["isdir"].side_effect = mock_isdir
            mock_path["isfile"].side_effect = mock_isfile

            results = tuple(initialized_linter._discover_files(["."]))

            assert mock_path["isdir"].call_count == 1
            assert mock_path["isdir"].call_args_list == [mock.call(".")]
            assert mock_path["isfile"].call_count == 1
            assert mock_path["isfile"].call_args_list == [
                mock.call("./__init__.py"),
            ]

    assert len(results) == 3
    assert results == ("./manage.py", "./applications", "./applications_api")


def test_does_not_ignore_similarly_named_package_even_if_first_ignored(
        initialized_linter,
        mock_tree,
) -> None:
    """
    Test to see if we return the expected package/file list even if the shorter named package is processed
    first and matches an ignore config value.

    NOTE: manage.py probably should be ignored.
    """
    with mock.patch("os.walk") as mock_walk:
        with mock.patch.multiple(
                "os.path", isdir=mock.DEFAULT, isfile=mock.DEFAULT
        ) as mock_path:
            initialized_linter.config.ignore = [
                ".venv",
                "applications",
                "node_modules",
                "manage.py",
            ]
            mock_walk.return_value = mock_tree
            mock_path["isdir"].side_effect = mock_isdir
            mock_path["isfile"].side_effect = mock_isfile

            results = tuple(initialized_linter._discover_files(["."]))

            assert mock_path["isdir"].call_count == 1
            assert mock_path["isdir"].call_args_list == [mock.call(".")]
            assert mock_path["isfile"].call_count == 1
            assert mock_path["isfile"].call_args_list == [
                mock.call("./__init__.py"),
            ]

    assert len(results) == 2
    assert results == ("./manage.py", "./applications_api")
