# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Unit test for the extensions.diadefslib modules."""

# pylint: disable=redefined-outer-name

from __future__ import annotations

import re
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path
from unittest.mock import Mock

import pytest
from astroid import extract_node, nodes

from pylint.pyreverse.diadefslib import (
    ClassDiadefGenerator,
    DefaultDiadefGenerator,
    DiaDefGenerator,
    DiadefsHandler,
)
from pylint.pyreverse.diagrams import DiagramEntity, Relationship
from pylint.pyreverse.inspector import Linker, Project
from pylint.testutils.pyreverse import PyreverseConfig
from pylint.testutils.utils import _test_cwd
from pylint.typing import GeneratorFactory, GetProjectCallable

HERE = Path(__file__)
TESTS = HERE.parent.parent


def _process_classes(classes: list[DiagramEntity]) -> list[tuple[bool, str]]:
    """Extract class names of a list."""
    return sorted((isinstance(c.node, nodes.ClassDef), c.title) for c in classes)


def _process_relations(
    relations: dict[str, list[Relationship]],
) -> list[tuple[str, str, str]]:
    """Extract relation indices from a relation list."""
    result = []
    for rel_type, rels in relations.items():
        for rel in rels:
            result.append((rel_type, rel.from_object.title, rel.to_object.title))
    result.sort()
    return result


@pytest.fixture
def HANDLER(
    default_config: PyreverseConfig, default_args: Sequence[str]
) -> DiadefsHandler:
    return DiadefsHandler(config=default_config, args=default_args)


@pytest.fixture(scope="module")
def PROJECT(get_project: GetProjectCallable) -> Iterator[Project]:
    with _test_cwd(TESTS):
        yield get_project("data")


# Fixture with factory function to create DiaDefGenerator instances
@pytest.fixture
def generator_factory(HANDLER: DiadefsHandler, PROJECT: Project) -> GeneratorFactory:
    def _factory(
        config: PyreverseConfig | None = None, args: Sequence[str] | None = None
    ) -> DiaDefGenerator:
        if config:
            HANDLER.config = config
        if args:
            HANDLER.args = args
        return DiaDefGenerator(Linker(PROJECT), HANDLER)

    return _factory


# Fixture for creating mocked nodes
@pytest.fixture
def mock_node() -> Callable[[str], Mock]:
    def _mock_node(module_path: str) -> Mock:
        """Create a mocked node with a given module path."""
        node = Mock()
        node.root.return_value.name = module_path
        return node

    return _mock_node


def test_option_values(
    default_config: PyreverseConfig,
    default_args: Sequence[str],
    HANDLER: DiadefsHandler,
    PROJECT: Project,
) -> None:
    """Test for ancestor, associated and module options."""
    df_h = DiaDefGenerator(Linker(PROJECT), HANDLER)
    cl_config = default_config
    cl_config.classes = ["Specialization"]
    cl_h = DiaDefGenerator(Linker(PROJECT), DiadefsHandler(config=cl_config, args=[]))
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
    handler = DiadefsHandler(config=default_config, args=default_args)
    df_h = DiaDefGenerator(Linker(PROJECT), handler)
    cl_config = default_config
    cl_config.classes = ["Specialization"]
    cl_h = DiaDefGenerator(
        Linker(PROJECT), DiadefsHandler(config=cl_config, args=default_args)
    )
    for hndl in (df_h, cl_h):
        hndl.config.show_ancestors = 2
        hndl.config.show_associated = 1
        hndl.config.module_names = False
        hndl._set_default_options()
        assert hndl._get_levels() == (2, 1)
        assert not hndl.module_names


def test_default_values() -> None:
    """Test default values for package or class diagrams."""
    # TODO : should test difference between default values for package or class diagrams


class TestShowOptions:
    def test_show_stdlib(self) -> None:
        example = extract_node(
            '''
            import collections

            class CustomDict(collections.OrderedDict):
                """docstring"""
            '''
        )

        config = PyreverseConfig()
        args: Sequence[str] = []
        dd_gen = DiaDefGenerator(Linker(PROJECT), DiadefsHandler(config, args))

        # Default behavior
        assert not list(dd_gen.get_ancestors(example, 1))

        # Show standard library enabled
        config.show_stdlib = True
        ancestors = list(dd_gen.get_ancestors(example, 1))
        assert len(ancestors) == 1
        assert ancestors[0].name == "OrderedDict"

    def test_show_builtin(self) -> None:
        example = extract_node(
            '''
            class CustomError(Exception):
                """docstring"""
            '''
        )

        config = PyreverseConfig()
        args: Sequence[str] = []
        dd_gen = DiaDefGenerator(Linker(PROJECT), DiadefsHandler(config, args))

        # Default behavior
        assert not list(dd_gen.get_ancestors(example, 1))

        # Show builtin enabled
        config.show_builtin = True
        ancestors = list(dd_gen.get_ancestors(example, 1))
        assert len(ancestors) == 1
        assert ancestors[0].name == "Exception"


class TestDefaultDiadefGenerator:
    _should_rels = [
        ("aggregation", "DoNothing2", "Specialization"),
        ("association", "DoNothing", "Ancestor"),
        ("association", "DoNothing", "Specialization"),
        ("specialization", "Specialization", "Ancestor"),
    ]

    def test_extract_relations(self, HANDLER: DiadefsHandler, PROJECT: Project) -> None:
        """Test extract_relations between classes."""
        cd = DefaultDiadefGenerator(Linker(PROJECT), HANDLER).visit(PROJECT)[1]
        cd.extract_relationships()
        relations = _process_relations(cd.relationships)
        assert relations == self._should_rels

    def test_functional_relation_extraction(
        self,
        default_config: PyreverseConfig,
        default_args: Sequence[str],
        get_project: GetProjectCallable,
    ) -> None:
        """Functional test of relations extraction;
        different classes possibly in different modules.
        """
        # XXX should be catching pyreverse environment problem but doesn't
        # pyreverse doesn't extract the relations but this test ok
        project = get_project("data")
        handler = DiadefsHandler(default_config, default_args)
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
        (True, "data.nullable_pattern"),
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
        (True, "NullablePatterns"),
        (True, "PropertyPatterns"),
        (True, "Specialization"),
    ]


def test_known_values2(
    HANDLER: DiadefsHandler, get_project: GetProjectCallable
) -> None:
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


def test_regression_dataclasses_inference(
    HANDLER: DiadefsHandler, get_project: GetProjectCallable
) -> None:
    project_path = Path("regrtest_data") / "dataclasses_pyreverse"
    path = get_project(str(project_path))

    cdg = ClassDiadefGenerator(Linker(path), HANDLER)
    special = "regrtest_data.dataclasses_pyreverse.InventoryItem"
    cd = cdg.class_diagram(path, special)
    assert cd.title == special


def test_should_include_by_depth_no_limit(
    generator_factory: GeneratorFactory, mock_node: Mock
) -> None:
    """Test that nodes are included when no depth limit is set."""
    generator = generator_factory()

    # Create mocked nodes with different depths
    node1 = mock_node("pkg")  # Depth 0
    node2 = mock_node("pkg.subpkg")  # Depth 1
    node3 = mock_node("pkg.subpkg.module")  # Depth 2

    # All nodes should be included when max_depth is None
    assert generator._should_include_by_depth(node1)
    assert generator._should_include_by_depth(node2)
    assert generator._should_include_by_depth(node3)


@pytest.mark.parametrize("max_depth", range(5))
def test_should_include_by_depth_absolute(
    generator_factory: GeneratorFactory, mock_node: Mock, max_depth: int
) -> None:
    """Test absolute depth filtering when root package is specified.

    - 'pkg'                  -> depth 0
    - 'pkg.subpkg'           -> depth 1
    - 'pkg.subpkg.module'    -> depth 2
    - 'pkg.subpkg.module.submodule' -> depth 3
    """
    specified_pkg = ["pkg"]
    generator = generator_factory(PyreverseConfig(max_depth=max_depth), specified_pkg)

    test_cases = {
        "pkg": [True, True, True, True, True],
        "pkg.subpkg": [False, True, True, True, True],
        "pkg.subpkg.module": [False, False, True, True, True],
        "pkg.subpkg.module.submodule": [False, False, False, True, True],
    }
    nodes = [mock_node(path) for path, _ in test_cases.items()]

    for node in nodes:
        should_show = test_cases[node.root.return_value.name][max_depth]
        result = generator._should_include_by_depth(node)

        msg = (
            f"Node {node.root.return_value.name} with max_depth={max_depth} and "
            f"specified package {specified_pkg} should"
            f"{'' if should_show else ' not'} show. "
            f"Generator returns: {result}"
        )
        assert result == should_show, msg


@pytest.mark.parametrize("max_depth", range(5))
@pytest.mark.parametrize("args", [["pkg"], ["pkg.subpkg"], ["pkg.subpkg.module"]])
def test_should_include_by_depth_relative_single_package(
    generator_factory: GeneratorFactory,
    mock_node: Mock,
    max_depth: int,
    args: list[str],
) -> None:
    """Test relative depth filtering when only one package is specified.

    Each test case ensures that depth is calculated **relative** to the specified package.
    """
    specified_pkg = args[0]
    generator = generator_factory(PyreverseConfig(max_depth=max_depth), args)

    test_cases = {
        "pkg": {
            "pkg": [True, True, True, True, True],
            "pkg.subpkg": [False, True, True, True, True],
            "pkg.subpkg.module": [False, False, True, True, True],
            "pkg.subpkg.module.submodule": [False, False, False, True, True],
        },
        "pkg.subpkg": {
            "pkg": [False, False, False, False, False],
            "pkg.subpkg": [True, True, True, True, True],
            "pkg.subpkg.module": [False, True, True, True, True],
            "pkg.subpkg.module.submodule": [False, False, True, True, True],
        },
        "pkg.subpkg.module": {
            "pkg": [False, False, False, False, False],
            "pkg.subpkg": [False, False, False, False, False],
            "pkg.subpkg.module": [True, True, True, True, True],
            "pkg.subpkg.module.submodule": [False, True, True, True, True],
        },
    }
    nodes = [mock_node(path) for path, _ in test_cases.items()]

    for node in nodes:
        should_show = test_cases[specified_pkg][node.root.return_value.name][max_depth]
        result = generator._should_include_by_depth(node)

        msg = (
            f"Node {node.root.return_value.name} with max_depth={max_depth} and "
            f"specified package {specified_pkg} should"
            f"{'' if should_show else ' not'} show. "
            f"Generator returns: {result}"
        )
        assert result == should_show, msg


@pytest.mark.parametrize("max_depth", range(5))
def test_should_include_by_depth_relative_multiple_packages(
    generator_factory: GeneratorFactory,
    mock_node: Mock,
    max_depth: int,
) -> None:
    """Test relative depth filtering when multiple packages are specified."""
    specified_pkg = ["pkg", "pkg.subpkg"]

    warning_msg = re.escape(
        "Detected nested names within the specified packages. "
        "The following packages: ['pkg'] will be ignored for "
        "depth calculations, using only: ['pkg.subpkg'] as the base for limiting "
        "package depth."
    )

    with pytest.warns(UserWarning, match=warning_msg):
        generator = generator_factory(
            PyreverseConfig(max_depth=max_depth), specified_pkg
        )

    test_cases = {
        "pkg": [False, False, False, False, False],
        "pkg.subpkg": [True, True, True, True, True],
        "pkg.subpkg.module": [False, True, True, True, True],
        "pkg.subpkg.module.submodule": [False, False, True, True, True],
    }
    nodes = [mock_node(path) for path, _ in test_cases.items()]

    for node in nodes:
        should_show = test_cases[node.root.return_value.name][max_depth]
        result = generator._should_include_by_depth(node)

        msg = (
            f"Node {node.root.return_value.name} with max_depth={max_depth} and "
            f"specified package {specified_pkg} "
            f"{'should show' if should_show else 'should not show'}. "
            f"Generator returns: {result}"
        )
        assert result == should_show, msg


def test_get_leaf_nodes(generator_factory: GeneratorFactory) -> None:
    """Test that leaf nodes are correctly identified."""
    # Create a tree with a single root node and multiple leaf nodes
    specified_packeges = [
        "pkg",
        "pkg.subpkg1",
        "pkg.subpkg2",
        "pkg.subpkg1.module1",
        "pkg.subpkg2.module2",
        "pkg.subpkg1.module1.submodule",
    ]
    corr = set(["pkg.subpkg2.module2", "pkg.subpkg1.module1.submodule"])

    generator = generator_factory(args=specified_packeges)
    assert len(corr.difference(generator.get_leaf_nodes())) == 0
