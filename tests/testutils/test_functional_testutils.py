# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the functional test framework."""

import contextlib
import os
import os.path
import shutil
import tempfile
from collections.abc import Iterator
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from _pytest.outcomes import Skipped

from pylint import testutils
from pylint.testutils.functional import (
    FunctionalTestFile,
    get_functional_test_files_from_directory,
)

HERE = Path(__file__).parent
DATA_DIRECTORY = HERE / "data"


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


@pytest.fixture(name="pytest_config")
def pytest_config_fixture() -> MagicMock:
    def _mock_getoption(option: str) -> bool:
        if option == "minimal_messages_config":
            return True
        return False

    config = MagicMock()
    config.getoption.side_effect = _mock_getoption
    return config


def test_parsing_of_pylintrc_init_hook() -> None:
    """Test that we correctly parse an init-hook in a settings file."""
    with pytest.raises(RuntimeError):
        test_file = FunctionalTestFile(str(DATA_DIRECTORY), "init_hook.py")
        testutils.LintModuleTest(test_file)


def test_get_functional_test_files_from_directory() -> None:
    """Test that we correctly check the functional test directory structures."""
    with pytest.raises(AssertionError) as exc_info:
        get_functional_test_files_from_directory(DATA_DIRECTORY / "u")
    assert exc_info.match("'use_dir.py' should go in 'use'")
    assert exc_info.match(
        "using_dir.py should go in a directory that starts with the "
        "first letters of 'using_dir'"
    )
    assert "incredibly_bold_mischief.py" not in str(exc_info.value)
    # Leading underscore mean that this should not fail the assertion
    get_functional_test_files_from_directory(DATA_DIRECTORY / "u/_no_issue_here")


def test_get_functional_test_files_from_crowded_directory() -> None:
    """Test that we correctly check the functional test directory structures."""
    with pytest.raises(AssertionError) as exc_info:
        get_functional_test_files_from_directory(
            DATA_DIRECTORY / "m", max_file_per_directory=1
        )
    assert exc_info.match("m: 3 when the max is 1")
    assert exc_info.match("max_overflow: 2 when the max is 1")
    assert len(exc_info.value.args[0].splitlines()) == 3
    with pytest.raises(AssertionError) as exc_info:
        get_functional_test_files_from_directory(
            DATA_DIRECTORY / "m", max_file_per_directory=2
        )
    assert exc_info.match("m: 3 when the max is 2")
    assert "max_overflow" not in str(exc_info.value)


@pytest.mark.parametrize(
    ["files", "output_file_name"],
    [
        ([], "file.txt"),
        (["file.txt"], "file.txt"),
        (["file.314.txt"], "file.txt"),  # don't match 3.14
        (["file.42.txt"], "file.txt"),  # don't match 4.2
        (["file.32.txt", "file.txt"], "file.32.txt"),
        (["file.312.txt", "file.txt"], "file.312.txt"),
        (["file.313.txt", "file.txt"], "file.313.txt"),
        (["file.310.txt", "file.313.txt", "file.312.txt", "file.txt"], "file.313.txt"),
        # don't match other test file names accidentally
        ([".file.313.txt"], "file.txt"),
        (["file_other.313.txt"], "file.txt"),
        (["other_file.313.txt"], "file.txt"),
    ],
)
def test_expected_output_file_matching(files: list[str], output_file_name: str) -> None:
    """Test output file matching. Pin current Python version to 3.13."""
    with tempdir():
        for file in files:
            with open(file, "w", encoding="utf-8"):
                ...
        test_file = FunctionalTestFile(".", "file.py")
        with patch(
            "pylint.testutils.functional.test_file._CURRENT_VERSION",
            new=(3, 13),
        ):
            assert test_file.expected_output == f".{os.path.sep}{output_file_name}"


def test_minimal_messages_config_enabled(pytest_config: MagicMock) -> None:
    """Test that all messages not targeted in the functional test are disabled
    when running with --minimal-messages-config.
    """
    test_file = FunctionalTestFile(
        str(DATA_DIRECTORY / "m"), "minimal_messages_config.py"
    )
    mod_test = testutils.LintModuleTest(test_file, pytest_config)
    assert all(
        mod_test._linter.is_message_enabled(msgid)
        for msgid in (
            "consider-using-with",
            "unspecified-encoding",
            "consider-using-f-string",
            # Always enable fatal errors: important not to have false negatives
            "astroid-error",
            "fatal",
            "syntax-error",
        )
    )
    assert not mod_test._linter.is_message_enabled("unused-import")


def test_minimal_messages_config_excluded_file(pytest_config: MagicMock) -> None:
    """Test that functional test files can be excluded from the run with
    --minimal-messages-config if they set the exclude_from_minimal_messages_config
    option in their rcfile.
    """
    test_file = FunctionalTestFile(
        str(DATA_DIRECTORY / "m"), "minimal_messages_excluded.py"
    )
    mod_test = testutils.LintModuleTest(test_file, pytest_config)
    with pytest.raises(Skipped):
        mod_test.setUp()
