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
    assert test_file.options["marker"] == ""
    assert test_file.options["reason"] == ""


def test_file_without_options() -> None:
    test_file = TEST_FILES["functest_without_options"]
    assert test_file.options["output_formats"] == ["mmd"]
    assert test_file.options["command_line_args"] == []
    assert test_file.options["diagram_type"] == "classes"
    assert test_file.options["marker"] == ""
    assert test_file.options["reason"] == ""


@pytest.mark.parametrize("marker", ["", "xfail", "skip"])
def test_file_marker_options(tmp_path: Path, marker: str) -> None:
    reason = "Known diagram issue" if marker else ""
    source = tmp_path / "example.py"
    source.touch()
    source.with_suffix(".rc").write_text(
        f"[testoptions]\nmarker={marker}\nreason={reason}\n", encoding="utf8"
    )

    (testfile,) = pyreverse.get_functional_test_files(tmp_path)

    assert testfile.options["marker"] == marker
    assert testfile.options["reason"] == reason


@pytest.mark.parametrize(
    "options,message",
    [
        ("marker=unknown\nreason=Known issue", "Unsupported test marker"),
        ("marker=xfail", "requires a non-empty reason"),
        ("marker=skip\nreason=   ", "requires a non-empty reason"),
    ],
)
def test_invalid_marker_options(tmp_path: Path, options: str, message: str) -> None:
    source = tmp_path / "example.py"
    source.touch()
    config_file = source.with_suffix(".rc")
    config_file.write_text(f"[testoptions]\n{options}\n", encoding="utf8")

    with pytest.raises(ValueError, match=message) as exc:
        pyreverse.get_functional_test_files(tmp_path)

    assert str(config_file) in str(exc.value)


def test_directories_with_python_suffix_are_not_test_files(tmp_path: Path) -> None:
    directory = tmp_path / "example.py"
    directory.mkdir()
    source = directory / "nested.py"
    source.touch()

    testfiles = pyreverse.get_functional_test_files(tmp_path)

    assert [testfile.source for testfile in testfiles] == [source]


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
            "diagram_type=packages\n"
            "marker=skip\n"
            "reason=Temporarily disabled package test\n",
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
            "marker": "skip",
            "reason": "Temporarily disabled package test",
        }
        if with_config
        else {
            "source_roots": [],
            "output_formats": ["mmd"],
            "command_line_args": [],
            "diagram_type": "classes",
            "marker": "",
            "reason": "",
        }
    )
