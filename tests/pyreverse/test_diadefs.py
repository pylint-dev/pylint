# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

"""Unit test for the extensions.diadefslib modules."""
# pylint: disable=redefined-outer-name
import sys
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import pytest
from astroid import nodes

from pylint.pyreverse.diadefslib import (
    ClassDiadefGenerator,
    DefaultDiadefGenerator,
    DiaDefGenerator,
    DiadefsHandler,
)
from pylint.pyreverse.diagrams import DiagramEntity, Relationship
from pylint.pyreverse.inspector import Linker, Project
from pylint.testutils.pyreverse import PyreverseConfig


def _process_classes(classes: List[DiagramEntity]) -> List[Tuple[bool, str]]:
    """Extract class names of a list."""
    return sorted((isinstance(c.node, nodes.ClassDef), c.title) for c in classes)


def _process_relations(
    relations: Dict[str, List[Relationship]]
) -> List[Tuple[str, str, str]]:
    """Extract relation indices from a relation list."""
    result = []
    for rel_type, rels in relations.items():
        for rel in rels:
            result.append((rel_type, rel.from_object.title, rel.to_object.title))
    result.sort()
    return result


@pytest.fixture
def HANDLER(default_config: PyreverseConfig) -> DiadefsHandler:
    return DiadefsHandler(default_config)


@pytest.fixture(scope="module")
def PROJECT(get_project):
    return get_project("data")


def test_option_values(
    default_config: PyreverseConfig, HANDLER: DiadefsHandler, PROJECT: Project
) -> None:
    """Test for ancestor, associated and module options."""
    df_h = DiaDefGenerator(Linker(PROJECT), HANDLER)
    cl_config = default_config
    cl_config.classes = ["Specialization"]
    cl_h = DiaDefGenerator(Linker(PROJECT), DiadefsHandler(cl_config))
    assert df_h._get_levels() == (0, 0)
    assert not df_h.module_names
    assert cl_h._get_levels() == (-1, -1)
    assert cl_h.module_names
    for hndl in (df_h, cl_h):
        hndl.config.all_ancestors = True
        hndl.config.all_associated = True
        hndl.config.module_names = True
        hndl._set_default_options()
        assert hndl._get_levels() == (-1, -1)
        assert hndl.module_names
    handler = DiadefsHandler(default_config)
    df_h = DiaDefGenerator(Linker(PROJECT), handler)
    cl_config = default_config
    cl_config.classes = ["Specialization"]
    cl_h = DiaDefGenerator(Linker(PROJECT), DiadefsHandler(cl_config))
    for hndl in (df_h, cl_h):
        hndl.config.show_ancestors = 2
        hndl.config.show_associated = 1
        hndl.config.module_names = False
        hndl._set_default_options()
        assert hndl._get_levels() == (2, 1)
        assert not hndl.module_names


def test_default_values() -> None:
    """Test default values for package or class diagrams."""
    # TODO : should test difference between default values for package or class diagrams pylint: disable=fixme


class TestDefaultDiadefGenerator:
    _should_rels = [
        ("association", "DoNothing", "Ancestor"),
        ("association", "DoNothing", "Specialization"),
        ("association", "DoNothing2", "Specialization"),
        ("implements", "Ancestor", "Interface"),
        ("specialization", "Specialization", "Ancestor"),
    ]

    def test_exctract_relations(
        self, HANDLER: DiadefsHandler, PROJECT: Project
    ) -> None:
        """Test extract_relations between classes."""
        cd = DefaultDiadefGenerator(Linker(PROJECT), HANDLER).visit(PROJECT)[1]
        cd.extract_relationships()
        relations = _process_relations(cd.relationships)
        assert relations == self._should_rels

    def test_functional_relation_extraction(
        self, default_config: PyreverseConfig, get_project: Callable
    ) -> None:
        """Functional test of relations extraction;
        different classes possibly in different modules
        """
        # XXX should be catching pyreverse environment problem but doesn't
        # pyreverse doesn't extract the relations but this test ok
        project = get_project("data")
        handler = DiadefsHandler(default_config)
        diadefs = handler.get_diadefs(project, Linker(project, tag=True))
        cd = diadefs[1]
        relations = _process_relations(cd.relationships)
        assert relations == self._should_rels


def test_known_values1(HANDLER: DiadefsHandler, PROJECT: Project) -> None:
    dd = DefaultDiadefGenerator(Linker(PROJECT), HANDLER).visit(PROJECT)
    assert len(dd) == 2
    keys = [d.TYPE for d in dd]
    assert keys == ["package", "class"]
    pd = dd[0]
    assert pd.title == "packages No Name"
    modules = sorted((isinstance(m.node, nodes.Module), m.title) for m in pd.objects)
    assert modules == [
        (True, "data"),
        (True, "data.clientmodule_test"),
        (True, "data.property_pattern"),
        (True, "data.suppliermodule_test"),
    ]
    cd = dd[1]
    assert cd.title == "classes No Name"
    classes = _process_classes(cd.objects)
    assert classes == [
        (True, "Ancestor"),
        (True, "CustomException"),
        (True, "DoNothing"),
        (True, "DoNothing2"),
        (True, "DoSomething"),
        (True, "Interface"),
        (True, "PropertyPatterns"),
        (True, "Specialization"),
    ]


def test_known_values2(HANDLER: DiadefsHandler, get_project: Callable) -> None:
    project = get_project("data.clientmodule_test")
    dd = DefaultDiadefGenerator(Linker(project), HANDLER).visit(project)
    assert len(dd) == 1
    keys = [d.TYPE for d in dd]
    assert keys == ["class"]
    cd = dd[0]
    assert cd.title == "classes No Name"
    classes = _process_classes(cd.objects)
    assert classes == [(True, "Ancestor"), (True, "Specialization")]


def test_known_values3(HANDLER: DiadefsHandler, PROJECT: Project) -> None:
    HANDLER.config.classes = ["Specialization"]
    cdg = ClassDiadefGenerator(Linker(PROJECT), HANDLER)
    special = "data.clientmodule_test.Specialization"
    cd = cdg.class_diagram(PROJECT, special)
    assert cd.title == special
    classes = _process_classes(cd.objects)
    assert classes == [
        (True, "data.clientmodule_test.Ancestor"),
        (True, special),
        (True, "data.suppliermodule_test.DoNothing"),
        (True, "data.suppliermodule_test.DoNothing2"),
    ]


def test_known_values4(HANDLER: DiadefsHandler, PROJECT: Project) -> None:
    HANDLER.config.classes = ["Specialization"]
    HANDLER.config.module_names = False
    cd = ClassDiadefGenerator(Linker(PROJECT), HANDLER).class_diagram(
        PROJECT, "data.clientmodule_test.Specialization"
    )
    assert cd.title == "data.clientmodule_test.Specialization"
    classes = _process_classes(cd.objects)
    assert classes == [
        (True, "Ancestor"),
        (True, "DoNothing"),
        (True, "DoNothing2"),
        (True, "Specialization"),
    ]


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires dataclasses")
def test_regression_dataclasses_inference(
    HANDLER: DiadefsHandler, get_project: Callable
) -> None:
    project_path = Path("regrtest_data") / "dataclasses_pyreverse"
    path = get_project(str(project_path))

    cdg = ClassDiadefGenerator(Linker(path), HANDLER)
    special = "regrtest_data.dataclasses_pyreverse.InventoryItem"
    cd = cdg.class_diagram(path, special)
    assert cd.title == special
