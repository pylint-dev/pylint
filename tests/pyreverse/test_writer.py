# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Unit test for ``DiagramWriter``."""

from __future__ import annotations

import codecs
import os
from collections.abc import Iterator
from difflib import unified_diff
from pathlib import Path
from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch

from pylint.pyreverse.diadefslib import DefaultDiadefGenerator, DiadefsHandler
from pylint.pyreverse.inspector import Linker, Project
from pylint.pyreverse.writer import DiagramWriter
from pylint.testutils.pyreverse import PyreverseConfig
from pylint.typing import GetProjectCallable

_DEFAULTS = {
    "all_ancestors": None,
    "show_associated": None,
    "module_names": None,
    "output_format": "dot",
    "diadefs_file": None,
    "quiet": 0,
    "show_ancestors": None,
    "classes": (),
    "all_associated": None,
    "mode": "PUB_ONLY",
    "show_builtin": False,
    "show_stdlib": False,
    "only_classnames": False,
    "output_directory": "",
    "no_standalone": False,
}

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

DOT_FILES = ["packages_No_Name.dot", "classes_No_Name.dot"]
COLORIZED_DOT_FILES = ["packages_colorized.dot", "classes_colorized.dot"]
PUML_FILES = ["packages_No_Name.puml", "classes_No_Name.puml"]
COLORIZED_PUML_FILES = ["packages_colorized.puml", "classes_colorized.puml"]
MMD_FILES = ["packages_No_Name.mmd", "classes_No_Name.mmd"]
HTML_FILES = ["packages_No_Name.html", "classes_No_Name.html"]
NO_STANDALONE_FILES = ["classes_no_standalone.dot", "packages_no_standalone.dot"]
TYPE_CHECK_IMPORTS_FILES = [
    "packages_type_check_imports.dot",
    "classes_type_check_imports.dot",
]


class Config:
    """Config object for tests."""

    def __init__(self) -> None:
        for attr, value in _DEFAULTS.items():
            setattr(self, attr, value)


def _file_lines(path: str) -> list[str]:
    # we don't care about the actual encoding, but python3 forces us to pick one
    with codecs.open(path, encoding="latin1") as stream:
        lines = [
            line.strip()
            for line in stream.readlines()
            if (
                line.find("squeleton generated by ") == -1
                and not line.startswith('__revision__ = "$Id:')
            )
        ]
    return [line for line in lines if line]


@pytest.fixture(autouse=True)
def change_to_temp_dir(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)


@pytest.fixture()
def setup_dot(
    default_config: PyreverseConfig, get_project: GetProjectCallable
) -> Iterator[None]:
    writer = DiagramWriter(default_config)
    project = get_project(TEST_DATA_DIR)
    yield from _setup(project, default_config, writer)


@pytest.fixture()
def setup_colorized_dot(
    colorized_dot_config: PyreverseConfig, get_project: GetProjectCallable
) -> Iterator[None]:
    writer = DiagramWriter(colorized_dot_config)
    project = get_project(TEST_DATA_DIR, name="colorized")
    yield from _setup(project, colorized_dot_config, writer)


@pytest.fixture()
def setup_no_standalone_dot(
    no_standalone_dot_config: PyreverseConfig, get_project: GetProjectCallable
) -> Iterator[None]:
    writer = DiagramWriter(no_standalone_dot_config)
    project = get_project(TEST_DATA_DIR, name="no_standalone")
    yield from _setup(project, no_standalone_dot_config, writer)


@pytest.fixture()
def setup_type_check_imports_dot(
    default_config: PyreverseConfig, get_project: GetProjectCallable
) -> Iterator[None]:
    writer = DiagramWriter(default_config)
    project = get_project(
        os.path.join(os.path.dirname(__file__), "functional", "package_diagrams"),
        name="type_check_imports",
    )

    yield from _setup(project, default_config, writer)


@pytest.fixture()
def setup_puml(
    puml_config: PyreverseConfig, get_project: GetProjectCallable
) -> Iterator[None]:
    writer = DiagramWriter(puml_config)
    project = get_project(TEST_DATA_DIR)
    yield from _setup(project, puml_config, writer)


@pytest.fixture()
def setup_colorized_puml(
    colorized_puml_config: PyreverseConfig, get_project: GetProjectCallable
) -> Iterator[None]:
    writer = DiagramWriter(colorized_puml_config)
    project = get_project(TEST_DATA_DIR, name="colorized")
    yield from _setup(project, colorized_puml_config, writer)


@pytest.fixture()
def setup_mmd(
    mmd_config: PyreverseConfig, get_project: GetProjectCallable
) -> Iterator[None]:
    writer = DiagramWriter(mmd_config)

    project = get_project(TEST_DATA_DIR)
    yield from _setup(project, mmd_config, writer)


@pytest.fixture()
def setup_html(
    html_config: PyreverseConfig, get_project: GetProjectCallable
) -> Iterator[None]:
    writer = DiagramWriter(html_config)

    project = get_project(TEST_DATA_DIR)
    yield from _setup(project, html_config, writer)


def _setup(
    project: Project, config: PyreverseConfig, writer: DiagramWriter
) -> Iterator[None]:
    linker = Linker(project)
    handler = DiadefsHandler(config)
    dd = DefaultDiadefGenerator(linker, handler).visit(project)
    for diagram in dd:
        diagram.extract_relationships()
    writer.write(dd)
    yield


@pytest.mark.usefixtures("setup_dot")
@pytest.mark.parametrize("generated_file", DOT_FILES)
def test_dot_files(generated_file: str) -> None:
    _assert_files_are_equal(generated_file)


@pytest.mark.usefixtures("setup_colorized_dot")
@pytest.mark.parametrize("generated_file", COLORIZED_DOT_FILES)
def test_colorized_dot_files(generated_file: str) -> None:
    _assert_files_are_equal(generated_file)


@pytest.mark.usefixtures("setup_no_standalone_dot")
@pytest.mark.parametrize("generated_file", NO_STANDALONE_FILES)
def test_no_standalone_dot_files(generated_file: str) -> None:
    _assert_files_are_equal(generated_file)


@pytest.mark.usefixtures("setup_type_check_imports_dot")
@pytest.mark.parametrize("generated_file", TYPE_CHECK_IMPORTS_FILES)
def test_type_check_imports_dot_files(generated_file: str) -> None:
    _assert_files_are_equal(generated_file)


@pytest.mark.usefixtures("setup_puml")
@pytest.mark.parametrize("generated_file", PUML_FILES)
def test_puml_files(generated_file: str) -> None:
    _assert_files_are_equal(generated_file)


@pytest.mark.usefixtures("setup_mmd")
@pytest.mark.parametrize("generated_file", MMD_FILES)
def test_mmd_files(generated_file: str) -> None:
    _assert_files_are_equal(generated_file)


@pytest.mark.usefixtures("setup_html")
@pytest.mark.parametrize("generated_file", HTML_FILES)
def test_html_files(generated_file: str) -> None:
    _assert_files_are_equal(generated_file)


@pytest.mark.usefixtures("setup_colorized_puml")
@pytest.mark.parametrize("generated_file", COLORIZED_PUML_FILES)
def test_colorized_puml_files(generated_file: str) -> None:
    _assert_files_are_equal(generated_file)


def _assert_files_are_equal(generated_file: str) -> None:
    expected_file = os.path.join(os.path.dirname(__file__), "data", generated_file)
    generated = _file_lines(generated_file)
    expected = _file_lines(expected_file)
    joined_generated = "\n".join(generated)
    joined_expected = "\n".join(expected)
    files = f"\n *** expected : {expected_file}, generated : {generated_file} \n"
    diff = "\n".join(
        line
        for line in unified_diff(
            joined_expected.splitlines(), joined_generated.splitlines()
        )
    )
    assert joined_expected == joined_generated, f"{files}{diff}"


def test_color_for_stdlib_module(default_config: PyreverseConfig) -> None:
    writer = DiagramWriter(default_config)
    obj = Mock()
    obj.node = Mock()
    obj.node.qname.return_value = "collections"
    assert writer.get_shape_color(obj) == "grey"


def test_package_name_with_slash(default_config: PyreverseConfig) -> None:
    """Test to check the names of the generated files are corrected
    when using an incorrect character like "/" in the package name.
    """
    writer = DiagramWriter(default_config)
    obj = Mock()

    obj.objects = []
    obj.get_relationships.return_value = []
    obj.title = "test/package/name/with/slash/"
    writer.write([obj])

    assert os.path.exists("test_package_name_with_slash_.dot")


def test_should_show_node_no_depth_limit(default_config: PyreverseConfig) -> None:
    """Test that nodes are shown when no depth limit is set."""
    writer = DiagramWriter(default_config)
    writer.max_depth = None

    assert writer.should_show_node("pkg")
    assert writer.should_show_node("pkg.subpkg")
    assert writer.should_show_node("pkg.subpkg.module")
    assert writer.should_show_node("pkg.subpkg.module.submodule")


@pytest.mark.parametrize("max_depth", range(5))
def test_should_show_node_with_depth_limit(
    default_config: PyreverseConfig, max_depth: int
) -> None:
    """Test that nodes are filtered correctly when depth limit is set.

    Depth counting is zero-based, determined by number of dots in path:
    - 'pkg'                  -> depth 0 (0 dots)
    - 'pkg.subpkg'           -> depth 1 (1 dot)
    - 'pkg.subpkg.module'    -> depth 2 (2 dots)
    - 'pkg.subpkg.module.submodule' -> depth 3 (3 dots)
    """
    writer = DiagramWriter(default_config)
    print("max_depth:", max_depth)
    writer.max_depth = max_depth

    # Test cases for different depths
    test_cases = [
        "pkg",
        "pkg.subpkg",
        "pkg.subpkg.module",
        "pkg.subpkg.module.submodule",
    ]

    # Test if nodes are shown based on their depth and max_depth setting
    for i, path in enumerate(test_cases):
        should_show = i <= max_depth
        print(
            f"Path {path} (depth {i}) with max_depth={max_depth} "
            f"{'should show' if should_show else 'should not show'}:"
            f"{writer.should_show_node(path, is_class=True)}"
        )
        assert writer.should_show_node(path) == should_show


@pytest.mark.parametrize("max_depth", range(5))
def test_should_show_node_classes(
    default_config: PyreverseConfig, max_depth: int
) -> None:
    """Test class visibility based on their containing module depth.

     Classes are filtered based on their containing module's depth:
    - MyClass -> depth 0 (no module)
    - pkg.MyClass -> depth 0 (module has no dots)
    - pkg.subpkg.MyClass -> depth 1 (module has 1 dot)
    - pkg.subpkg.mod.MyClass -> depth 2 (module has 2 dots)
    """
    writer = DiagramWriter(default_config)
    print("max_depth:", max_depth)
    writer.max_depth = max_depth

    # Test cases for different depths
    test_cases = [
        "MyClass",
        "pkg.MyClass",
        "pkg.subpkg.MyClass",
        "pkg.subpkg.mod.MyClass",
    ]

    # Test if nodes are shown based on their depth and max_depth setting
    for i, path in enumerate(test_cases):
        should_show = i - 1 <= max_depth  # Subtract 1 to account for the class name
        print(
            f"Path {path} (depth {i}) with max_depth={max_depth} "
            f"{'should show' if should_show else 'should not show'}:"
            f"{writer.should_show_node(path, is_class=True)}"
        )
        assert writer.should_show_node(path, is_class=True) == should_show
