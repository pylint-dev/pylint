# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

"""Tests for the functional test framework."""

from pathlib import Path

import pytest

from pylint import testutils
from pylint.testutils.functional import (
    FunctionalTestFile,
    get_functional_test_files_from_directory,
)

HERE = Path(__file__).parent
DATA_DIRECTORY = HERE / "data"


def test_parsing_of_pylintrc_init_hook() -> None:
    """Test that we correctly parse an init-hook in a settings file."""
    with pytest.raises(RuntimeError):
        test_file = FunctionalTestFile(str(DATA_DIRECTORY), "init_hook.py")
        testutils.LintModuleTest(test_file)


def test_get_functional_test_files_from_directory() -> None:
    """Test that we correctly check the functional test directory structures."""
    with pytest.raises(AssertionError, match="using_dir.py should not go in"):
        get_functional_test_files_from_directory(DATA_DIRECTORY)
