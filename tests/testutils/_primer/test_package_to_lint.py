# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from unittest.mock import MagicMock, patch

import pytest
from git import GitCommandError

from pylint.testutils._primer import PRIMER_DIRECTORY_PATH, PackageToLint
from pylint.testutils._primer.package_to_lint import DirtyPrimerDirectoryException


def test_package_to_lint() -> None:
    """Test that the PackageToLint is instantiated correctly."""
    expected_dir_path = PRIMER_DIRECTORY_PATH / "vimeo" / "graph-explorer"
    expected_path_to_lint = expected_dir_path / "graph_explorer"
    expected_pylintrc_path = expected_dir_path / ".pylintrcui"

    args = ["--ignore-pattern='re*'"]
    package_to_lint = PackageToLint(
        url="https://github.com/vimeo/graph-explorer.git",
        branch="main",
        directories=["graph_explorer"],
        commit="abc123",
        pylintrc_relpath=".pylintrcui",
        pylint_additional_args=args,
    )

    assert package_to_lint.url == "https://github.com/vimeo/graph-explorer.git"
    assert package_to_lint.branch == "main"
    assert package_to_lint.directories == ["graph_explorer"]
    assert package_to_lint.pylintrc_relpath == ".pylintrcui"
    assert package_to_lint.pylint_additional_args == args
    assert package_to_lint.paths_to_lint == [str(expected_path_to_lint)]
    assert package_to_lint.clone_directory == expected_dir_path
    assert package_to_lint.pylintrc == expected_pylintrc_path
    expected_args = [
        str(expected_path_to_lint),
        f"--rcfile={expected_pylintrc_path}",
        *args,
    ]
    assert package_to_lint.pylint_args == expected_args


def test_package_to_lint_default_value() -> None:
    """Test that the PackageToLint is instantiated correctly with default value."""
    package_to_lint = PackageToLint(
        url="https://github.com/pallets/flask.git",
        branch="main",
        directories=["src/flask"],  # Must work on Windows (src\\flask)
        commit="abc123",
    )
    assert package_to_lint.pylintrc == ""
    expected_path_to_lint = (
        PRIMER_DIRECTORY_PATH / "pallets" / "flask" / "src" / "flask"
    )
    assert package_to_lint.pylint_args == [str(expected_path_to_lint), "--rcfile="]


FAKE_COMMIT = "abc123def456789"
FAKE_PACKAGE = PackageToLint(
    url="https://github.com/fake/repo",
    branch="main",
    directories=["src"],
    commit=FAKE_COMMIT,
)


@patch("pylint.testutils._primer.package_to_lint.Repo")
def test_clone_repository(mock_repo_cls: MagicMock) -> None:
    """Test _clone_repository initialization, adds remote, and checks out the pinned commit."""
    mock_repo = MagicMock()
    mock_repo.head.object.hexsha = FAKE_COMMIT
    mock_repo_cls.init.return_value = mock_repo

    result = FAKE_PACKAGE._clone_repository()
    mock_repo_cls.init.assert_called_once_with(FAKE_PACKAGE.clone_directory)
    mock_repo.create_remote.assert_called_once_with("origin", FAKE_PACKAGE.url)
    mock_repo.git.fetch.assert_called_once_with("origin", FAKE_COMMIT, depth=1)
    mock_repo.git.checkout.assert_called_once_with(FAKE_COMMIT)
    assert result == FAKE_COMMIT


@patch("pylint.testutils._primer.package_to_lint.Repo")
def test_pull_repository_already_at_commit(mock_repo_cls: MagicMock) -> None:
    """Test _pull_repository short-circuits when already at the pinned commit."""
    mock_repo = MagicMock()
    mock_repo.head.object.hexsha = FAKE_COMMIT
    mock_repo_cls.return_value = mock_repo

    result = FAKE_PACKAGE._pull_repository()
    assert result == FAKE_COMMIT
    mock_repo.git.fetch.assert_not_called()


@patch("pylint.testutils._primer.package_to_lint.Repo")
def test_pull_repository_fetches_new_commit(mock_repo_cls: MagicMock) -> None:
    """Test _pull_repository fetches and checks out when commit differs."""
    mock_repo = MagicMock()
    mock_repo.head.object.hexsha = "old_commit_hash"
    mock_repo.is_dirty.return_value = False
    mock_repo_cls.return_value = mock_repo

    FAKE_PACKAGE._pull_repository()
    mock_repo.is_dirty.assert_called_once()
    mock_repo.git.fetch.assert_called_once_with("origin", FAKE_COMMIT, depth=1)
    mock_repo.git.checkout.assert_called_once_with(FAKE_COMMIT)


@patch("pylint.testutils._primer.package_to_lint.Repo")
def test_pull_repository_dirty_raises(mock_repo_cls: MagicMock) -> None:
    """Test _pull_repository raises when the local clone is dirty."""
    mock_repo = MagicMock()
    mock_repo.head.object.hexsha = "old_commit_hash"
    mock_repo.is_dirty.return_value = True
    mock_repo_cls.return_value = mock_repo

    with pytest.raises(DirtyPrimerDirectoryException):
        FAKE_PACKAGE._pull_repository()


@patch("pylint.testutils._primer.package_to_lint.Repo")
def test_pull_repository_git_error_raises_system_error(
    mock_repo_cls: MagicMock,
) -> None:
    """Test _pull_repository wraps GitCommandError in SystemError."""
    mock_repo = MagicMock()
    mock_repo.head.object.hexsha = "old_commit_hash"
    mock_repo.is_dirty.return_value = False
    mock_repo.git.fetch.side_effect = GitCommandError("git fetch", 128)
    mock_repo_cls.return_value = mock_repo

    with pytest.raises(SystemError, match="Failed to fetch pinned commit"):
        FAKE_PACKAGE._pull_repository()
