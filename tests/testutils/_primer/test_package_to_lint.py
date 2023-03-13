# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from pylint.testutils._primer import PRIMER_DIRECTORY_PATH, PackageToLint


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
    )
    assert package_to_lint.pylintrc == ""
    expected_path_to_lint = (
        PRIMER_DIRECTORY_PATH / "pallets" / "flask" / "src" / "flask"
    )
    assert package_to_lint.pylint_args == [str(expected_path_to_lint), "--rcfile="]
