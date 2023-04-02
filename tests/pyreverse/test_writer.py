# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Unit test for ``DiagramWriter``."""

from __future__ import annotations

import codecs
import os
from collections.abc import Iterator
from difflib import unified_diff
from unittest.mock import Mock

import pytest

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
}

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

DOT_FILES = ["packages_No_Name.dot", "classes_No_Name.dot"]
COLORIZED_DOT_FILES = ["packages_colorized.dot", "classes_colorized.dot"]
PUML_FILES = ["packages_No_Name.puml", "classes_No_Name.puml"]
COLORIZED_PUML_FILES = ["packages_colorized.puml", "classes_colorized.puml"]
MMD_FILES = ["packages_No_Name.mmd", "classes_No_Name.mmd"]
HTML_FILES = ["packages_No_Name.html", "classes_No_Name.html"]


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
    for fname in (
        DOT_FILES
        + COLORIZED_DOT_FILES
        + PUML_FILES
        + COLORIZED_PUML_FILES
        + MMD_FILES
        + HTML_FILES
    ):
        try:
            os.remove(fname)
        except FileNotFoundError:
            continue


@pytest.mark.usefixtures("setup_dot")
@pytest.mark.parametrize("generated_file", DOT_FILES)
def test_dot_files(generated_file: str) -> None:
    _assert_files_are_equal(generated_file)


@pytest.mark.usefixtures("setup_colorized_dot")
@pytest.mark.parametrize("generated_file", COLORIZED_DOT_FILES)
def test_colorized_dot_files(generated_file: str) -> None:
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


# test to check the names of the generated files are corrected when using an incorrect character like "/" in the package name
def test_package_name_with_slash(default_config: PyreverseConfig) -> None:
    writer = DiagramWriter(default_config)
    obj = Mock()

    obj.objects = []
    obj.get_relationships.return_value = []
    obj.title = "test/package/name/with/slash/"
    writer.write([obj])

    assert os.path.exists("test_package_name_with_slash_.dot")
    # remove the generated file
    os.remove("test_package_name_with_slash_.dot")
