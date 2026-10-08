# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from pathlib import Path

import pytest

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
    assert test_file.options["diagram_type"] == "classes"


def test_file_without_options() -> None:
    test_file = TEST_FILES["functest_without_options"]
    assert test_file.options["output_formats"] == ["mmd"]
    assert test_file.options["command_line_args"] == []
    assert test_file.options["diagram_type"] == "classes"


@pytest.mark.parametrize("with_config", [False, True])
def test_package_discovery(tmp_path: Path, with_config: bool) -> None:
    package = tmp_path / "package"
    package.mkdir()
    nested_package = package / "nested"
    nested_package.mkdir()
    (nested_package / "module.py").touch()
    (tmp_path / "README.txt").touch()
    (tmp_path / "_ignored").mkdir()

    if with_config:
        (package / "__init__.py").touch()
        (nested_package / "__init__.py").touch()
        (package / "package.rc").write_text(
            "[testoptions]\n"
            "source_roots=../source,../other\n"
            "output_formats=dot,puml\n"
            'command_line_args=--project "example project"\n'
            "diagram_type=packages\n",
            encoding="utf8",
        )

    testfiles = pyreverse.get_functional_test_packages(tmp_path)

    assert len(testfiles) == 1
    assert testfiles[0].source == package
    assert testfiles[0].options == (
        {
            "source_roots": ["../source", "../other"],
            "output_formats": ["dot", "puml"],
            "command_line_args": ["--project", "example project"],
            "diagram_type": "packages",
        }
        if with_config
        else {
            "source_roots": [],
            "output_formats": ["mmd"],
            "command_line_args": [],
            "diagram_type": "classes",
        }
    )
