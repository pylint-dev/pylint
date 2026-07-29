# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import os
from pathlib import Path
from unittest import mock

import pytest

from pylint.lint import PyLinter


@pytest.fixture(name="initialized_linter")
def _initialized_linter(linter: PyLinter) -> PyLinter:
    linter.open()

    return linter


@pytest.fixture(name="package_with_non_package_subdirectories")
def _package_with_non_package_subdirectories(tmp_path: Path) -> tuple[Path, set[Path]]:
    package = tmp_path / "root_package"
    files = {
        package / "__init__.py",
        package / "module.py",
        package / "nested_package" / "__init__.py",
        package / "nested_package" / "module.py",
        package / "nested_package" / "tools" / "tool.py",
        package / "scripts" / "script.py",
        package / "scripts" / "helper.pyi",
        package / "scripts" / "extra_package" / "__init__.py",
        package / "scripts" / "extra_package" / "module.py",
        package / "scripts" / "extra_package" / "resources" / "data.py",
    }
    for file in files:
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch()
    return package, files


def test_discover_files_below_package_root(
    initialized_linter: PyLinter,
    package_with_non_package_subdirectories: tuple[Path, set[Path]],
) -> None:
    package, _ = package_with_non_package_subdirectories

    discovered = {
        Path(path) for path in initialized_linter._discover_files([str(package)])
    }

    assert discovered == {
        package,
        package / "nested_package" / "tools" / "tool.py",
        package / "scripts" / "script.py",
        package / "scripts" / "helper.pyi",
        package / "scripts" / "extra_package",
        package / "scripts" / "extra_package" / "resources" / "data.py",
    }


@pytest.mark.parametrize("trailing_separator", [False, True])
def test_expanded_files_below_package_root_are_not_duplicated(
    initialized_linter: PyLinter,
    package_with_non_package_subdirectories: tuple[Path, set[Path]],
    trailing_separator: bool,
) -> None:
    package, expected_files = package_with_non_package_subdirectories
    package_argument = str(package) + (os.sep if trailing_separator else "")

    discovered = tuple(initialized_linter._discover_files([package_argument]))
    file_descriptions = tuple(initialized_linter._iterate_file_descrs(discovered))
    expanded_files = [Path(item.filepath) for item in file_descriptions]

    assert set(expanded_files) == expected_files
    assert len(expanded_files) == len(expected_files)


def test_ignore_non_package_subdirectory_below_package_root(
    initialized_linter: PyLinter,
    package_with_non_package_subdirectories: tuple[Path, set[Path]],
) -> None:
    package, _ = package_with_non_package_subdirectories
    initialized_linter.config.ignore = ["scripts"]

    discovered = {
        Path(path) for path in initialized_linter._discover_files([str(package)])
    }

    assert discovered == {
        package,
        package / "nested_package" / "tools" / "tool.py",
    }


def mock_isdir(path: str) -> bool:
    """
    Mock of os.path.isdir() for the following tests:
    - test_discover_files_does_not_ignore_similarly_named_package
    - test_discover_files_does_not_ignore_similarly_named_package_even_if_first_is_ignored
    """
    if path == ".":
        return True
    raise ValueError(f"Not expecting an isdir call on {path}")


@pytest.fixture(name="mock_tree")
def _mock_tree() -> list[tuple[str, list[str], list[str]]]:
    return [
        (
            ".",
            ["applications", "applications_api"],
            ["pyproject.toml", "manage.py"],
        ),
        (
            f".{os.sep}applications",
            ["tests"],
            ["views.py", "models.py", "admin.py", "apps.py", "__init__.py"],
        ),
        (
            f".{os.sep}applications{os.sep}tests",
            [],
            ["test1.py", "test2.py", "__init__.py"],
        ),
        (
            f".{os.sep}applications_api",
            ["tests"],
            ["views.py", "models.py", "admin.py", "apps.py", "__init__.py"],
        ),
        (
            f".{os.sep}applications_api{os.sep}tests",
            [],
            ["test1.py", "test2.py", "__init__.py"],
        ),
    ]


def test_does_not_ignore_similarly_named_package(
    initialized_linter: PyLinter,
    mock_tree: list[tuple[str, list[str], list[str]]],
) -> None:
    """
    Test to see if we return the expected package/file list even if a shorter named package is processed
    first and does not match an ignore config value.
    """
    with mock.patch("os.walk") as mock_walk:
        with mock.patch("os.path.isdir", side_effect=mock_isdir) as mock_isdir_method:
            mock_walk.return_value = mock_tree

            results = tuple(initialized_linter._discover_files(["."]))

            assert mock_isdir_method.call_count == 1
            assert mock_isdir_method.call_args_list == [mock.call(".")]

    assert len(results) == 3
    assert results == (
        f".{os.sep}manage.py",
        f".{os.sep}applications",
        f".{os.sep}applications_api",
    )


def test_does_not_ignore_similarly_named_package_even_if_first_ignored(
    initialized_linter: PyLinter,
    mock_tree: list[tuple[str, list[str], list[str]]],
) -> None:
    """
    Test to see if we return the expected package/file list even if the shorter named package is processed
    first and matches an ignore config value.

    NOTE: manage.py probably should be ignored.
    """
    with mock.patch("os.walk") as mock_walk:
        with mock.patch("os.path.isdir", side_effect=mock_isdir) as mock_isdir_method:
            initialized_linter.config.ignore = [
                ".venv",
                "applications",
                "node_modules",
                "manage.py",
            ]
            mock_walk.return_value = mock_tree

            results = tuple(initialized_linter._discover_files(["."]))

            assert mock_isdir_method.call_count == 1
            assert mock_isdir_method.call_args_list == [mock.call(".")]

    assert len(results) == 2
    assert results == (f".{os.sep}manage.py", f".{os.sep}applications_api")
