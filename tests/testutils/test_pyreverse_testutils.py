# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from pathlib import Path

from pylint.testutils import pyreverse

HERE = Path(__file__).parent
DATA_DIRECTORY = HERE / "pyreverse_data"
TEST_FILES = {
    testfile.source.stem: testfile
    for testfile in pyreverse.get_functional_test_files(DATA_DIRECTORY)
}


def test_files_with_leading_underscore_are_ignored() -> None:
    assert "_not_a_functest" not in TEST_FILES


def test_file_with_options() -> None:
    test_file = TEST_FILES["functest_with_options"]
    assert test_file.options["output_formats"] == ["dot", "png"]
    assert test_file.options["command_line_args"] == ["-ASmy"]


def test_file_without_options() -> None:
    test_file = TEST_FILES["functest_without_options"]
    assert test_file.options["output_formats"] == ["mmd"]
    assert test_file.options["command_line_args"] == []
