# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the functional test framework."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest
from _pytest.outcomes import Skipped

from pylint import testutils
from pylint.testutils.functional import (
    FunctionalTestFile,
    get_functional_test_files_from_directory,
)

HERE = Path(__file__).parent
DATA_DIRECTORY = HERE / "data"


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
    assert exc_info.match("m: 4 when the max is 1")
    assert exc_info.match("max_overflow: 3 when the max is 1")
    with pytest.raises(AssertionError) as exc_info:
        get_functional_test_files_from_directory(
            DATA_DIRECTORY / "m", max_file_per_directory=3
        )
    assert exc_info.match("m: 4 when the max is 3")
    assert "max_overflow" not in str(exc_info.value)


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
