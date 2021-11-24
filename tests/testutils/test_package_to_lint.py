# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
from pathlib import Path

from pylint.testutils.primer import PRIMER_DIRECTORY_PATH, PackageToLint


def test_package_to_lint() -> None:
    """Test that the PackageToLint is instantiated correctly."""
    package_to_lint = PackageToLint(
        url="https://github.com/vimeo/graph-explorer.git",
        branch="main",
        directories=["graph_explorer"],
        pylintrc_relpath=".pylintrcui",
        pylint_additional_args=["--ignore-pattern='re*'"],
    )
    assert package_to_lint.url == "https://github.com/vimeo/graph-explorer.git"
    assert package_to_lint.branch == "main"
    assert package_to_lint.directories == ["graph_explorer"]
    assert package_to_lint.pylintrc_relpath == ".pylintrcui"
    assert package_to_lint.pylint_additional_args == ["--ignore-pattern='re*'"]
    assert package_to_lint.paths_to_lint == [
        f"{PRIMER_DIRECTORY_PATH}/vimeo/graph-explorer/graph_explorer"
    ]
    assert package_to_lint.clone_directory == Path(
        f"{PRIMER_DIRECTORY_PATH}/vimeo/graph-explorer"
    )
    assert package_to_lint.pylintrc == Path(
        f"{PRIMER_DIRECTORY_PATH}/vimeo/graph-explorer/.pylintrcui"
    )
    assert package_to_lint.pylint_args == [
        f"{PRIMER_DIRECTORY_PATH}/vimeo/graph-explorer/graph_explorer",
        f"--rcfile={PRIMER_DIRECTORY_PATH}/vimeo/graph-explorer/.pylintrcui",
        "--ignore-pattern='re*'",
    ]


def test_package_to_lint_default_value() -> None:
    """Test that the PackageToLint is instantiated correctly with default value."""
    package_to_lint = PackageToLint(
        url="https://github.com/pallets/flask.git",
        branch="main",
        directories=["src/flask"],
    )
    assert package_to_lint.pylintrc is None
    assert package_to_lint.pylint_args == [
        f"{PRIMER_DIRECTORY_PATH}/pallets/flask/src/flask"
    ]
