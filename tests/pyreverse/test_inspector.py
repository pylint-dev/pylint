# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""For the visitors.diadefs module."""

# pylint: disable=redefined-outer-name

from __future__ import annotations

import os
import warnings
from collections.abc import Generator
from pathlib import Path

import astroid
import pytest

from pylint.pyreverse.inspector import Linker, Project
from pylint.testutils.utils import _test_cwd
from pylint.typing import GetProjectCallable

HERE = Path(__file__)
TESTS = HERE.parent.parent


@pytest.fixture(params=[True, False], ids=["tag=True", "tag=False"])
def test_context(
    request: pytest.FixtureRequest, get_project: GetProjectCallable
) -> Generator[tuple[Project, Linker]]:
    with _test_cwd(TESTS):
        project = get_project("data", "data")
        linker = Linker(project, tag=request.param)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            linker.visit(project)
        yield project, linker


def test_locals_assignment_resolution(test_context: tuple[Project, Linker]) -> None:
    proj, linker = test_context
    klass = proj.get_module("data.clientmodule_test")["Specialization"]
    info = linker.class_info[klass]
    type_dict = info.locals_type
    assert len(type_dict) == 2
    keys = sorted(type_dict.keys())
    assert keys == ["TYPE", "top"]
    assert len(type_dict["TYPE"]) == 1
    assert type_dict["TYPE"][0].value == "final class"
    assert len(type_dict["top"]) == 1
    assert type_dict["top"][0].value == "class"


def test_instance_attrs_resolution(test_context: tuple[Project, Linker]) -> None:
    proj, linker = test_context
    klass = proj.get_module("data.clientmodule_test")["Specialization"]
    info = linker.class_info[klass]
    type_dict = info.instance_attrs_type
    assert len(type_dict) == 3
    keys = sorted(type_dict.keys())
    assert keys == ["_id", "relation", "relation2"]
    assert isinstance(type_dict["relation"][0], astroid.bases.Instance), type_dict[
        "relation"
    ]
    assert type_dict["relation"][0].name == "DoNothing"
    assert type_dict["_id"][0] is astroid.Uninferable


def test_from_directory(test_context: tuple[Project, Linker]) -> None:
    proj, _ = test_context
    expected = os.path.join("tests", "data", "__init__.py")
    assert proj.name == "data"
    assert proj.path.endswith(expected)


def test_project_node(test_context: tuple[Project, Linker]) -> None:
    proj, _ = test_context
    expected = [
        "data",
        "data.clientmodule_test",
        "data.nullable_pattern",
        "data.property_pattern",
        "data.suppliermodule_test",
    ]
    assert sorted(proj.keys()) == expected
