# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Unit test for the extensions.diadefslib modules."""

# pylint: disable=redefined-outer-name

from __future__ import annotations

import re
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path
from textwrap import indent
from unittest.mock import Mock

import pytest
from astroid import InferenceError, extract_node, nodes, parse
from astroid.bases import Instance
from astroid.context import InferenceContext
from astroid.inference_tip import inference_tip
from astroid.manager import AstroidManager

from pylint.exceptions import InvalidArgsError
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
        example = extract_node('''
            import collections

            class CustomDict(collections.OrderedDict):
                """docstring"""
            ''')

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
        example = extract_node('''
            class CustomError(Exception):
                """docstring"""
            ''')

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
        ("composition", "DoNothing", "Ancestor"),
        ("composition", "DoNothing", "Specialization"),
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


def test_class_diagram_warns_for_uninferable_target(HANDLER: DiadefsHandler) -> None:
    module = parse("from unresolved import Target", module_name="sample")
    project = Project("sample")
    project.add_module(module)

    with pytest.warns(
        UserWarning,
        match=re.escape(
            "Unable to infer requested class 'Target'; generated diagram will be empty."
        ),
    ):
        diagram = ClassDiadefGenerator(Linker(project), HANDLER).class_diagram(
            project, "Target"
        )

    assert diagram.objects == []


@pytest.mark.parametrize(
    ("first", "second", "result"),
    [
        ("class", "const", "class"),
        ("const", "class", "class"),
        ("class", "unknown", "class"),
        ("unknown", "class", "class"),
        ("unknown", "const", "warning"),
        ("const", "unknown", "warning"),
        ("const", "function", "error"),
        ("class", "class", "class"),
    ],
)
def test_class_diagram_handles_multiple_inferred_types(
    HANDLER: DiadefsHandler, first: str, second: str, result: str
) -> None:
    statements = {
        "class": "class Maybe: pass",
        "const": "Maybe = 1",
        "unknown": "Maybe = unresolved()",
        "function": "def Maybe(): pass",
    }
    module = parse(
        f"if condition:\n{indent(statements[first], '    ')}\n"
        f"else:\n{indent(statements[second], '    ')}\n",
        module_name="sample",
    )
    project = Project("sample")
    project.add_module(module)
    generator = ClassDiadefGenerator(Linker(project), HANDLER)

    if result == "error":
        with pytest.raises(InvalidArgsError, match="is not a class"):
            generator.class_diagram(project, "Maybe")
        return
    if result == "warning":
        with pytest.warns(UserWarning, match="Unable to infer requested class 'Maybe'"):
            diagram = generator.class_diagram(project, "Maybe")
        assert diagram.objects == []
        return

    diagram = generator.class_diagram(project, "Maybe")
    assert len(diagram.objects) == 1
    assert diagram.objects[0].node is next(module.nodes_of_class(nodes.ClassDef))


def test_class_diagram_stops_inferring_after_class(
    HANDLER: DiadefsHandler, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = parse("class Target: pass", module_name="sample")
    project = Project("sample")
    project.add_module(module)

    def infer_class_then_fail(_name: str) -> Iterator[nodes.ClassDef]:
        yield module["Target"]
        raise InferenceError("Later inference should not be evaluated")

    monkeypatch.setattr(module, "ilookup", infer_class_then_fail)

    diagram = ClassDiadefGenerator(Linker(project), HANDLER).class_diagram(
        project, "Target"
    )

    assert len(diagram.objects) == 1
    assert diagram.objects[0].node is module["Target"]


def test_class_diagram_wraps_later_inference_error(
    HANDLER: DiadefsHandler, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = parse("Target = 1", module_name="sample")
    project = Project("sample")
    project.add_module(module)
    error = InferenceError("Failed to infer another possible value")

    def infer_value_then_fail(_name: str) -> Iterator[nodes.Const]:
        yield nodes.Const(1)
        raise error

    monkeypatch.setattr(module, "ilookup", infer_value_then_fail)

    with pytest.raises(
        InvalidArgsError,
        match=re.escape("Unable to resolve class 'Target' in module 'sample'."),
    ) as exc:
        ClassDiadefGenerator(Linker(project), HANDLER).class_diagram(project, "Target")

    assert exc.value.__cause__ is error


@pytest.mark.parametrize("target", ["func", "some_var", "module_value", "instance"])
@pytest.mark.parametrize("multiple_modules", [False, True])
def test_class_diagram_rejects_nonclass_target(
    HANDLER: DiadefsHandler, target: str, multiple_modules: bool
) -> None:
    project = Project("sample")
    project.add_module(
        parse(
            "import sys\nclass Target: pass\ndef func(): pass\n"
            "some_var = 1\nmodule_value = sys\ninstance = Target()\n",
            module_name="first",
        )
    )
    if multiple_modules:
        project.add_module(parse("class Other: pass", module_name="second"))
        target = f"first.{target}"

    with pytest.raises(
        InvalidArgsError,
        match=re.escape(
            f"Requested target {target!r} in module 'first' is not a class."
        ),
    ):
        ClassDiadefGenerator(Linker(project), HANDLER).class_diagram(project, target)


@pytest.mark.parametrize(
    ("target", "module_names", "message"),
    [
        (
            "Target",
            ["first", "second"],
            "Class name 'Target' must be fully qualified when multiple modules are analyzed.",
        ),
        (
            "missing.Target",
            ["first", "second"],
            "Module 'missing' is not part of the project.",
        ),
        (
            "first.Missing",
            ["first", "second"],
            "Unable to resolve class 'first.Missing' in module 'first'.",
        ),
        (
            "Missing",
            ["first"],
            "Unable to resolve class 'Missing' in module 'first'.",
        ),
    ],
)
def test_class_diagram_rejects_invalid_target(
    HANDLER: DiadefsHandler, target: str, module_names: list[str], message: str
) -> None:
    project = Project("sample")
    for module_name in module_names:
        project.add_module(parse("class Target: pass", module_name=module_name))

    with pytest.raises(InvalidArgsError, match=re.escape(message)):
        ClassDiadefGenerator(Linker(project), HANDLER).class_diagram(project, target)


@pytest.mark.parametrize(
    ("target", "module_names"),
    [
        ("Target", ["first"]),
        ("first.Target", ["first"]),
        ("first.Target", ["first", "second"]),
        ("Alias", ["first"]),
        ("first.Alias", ["first"]),
        ("first.Alias", ["first", "second"]),
    ],
)
def test_class_diagram_resolves_valid_target(
    HANDLER: DiadefsHandler, target: str, module_names: list[str]
) -> None:
    project = Project("sample")
    for module_name in module_names:
        project.add_module(
            parse("class Target: pass\nAlias = Target", module_name=module_name)
        )

    diagram = ClassDiadefGenerator(Linker(project), HANDLER).class_diagram(
        project, target
    )

    assert len(diagram.objects) == 1
    assert diagram.objects[0].node is project.get_module("first")["Target"]


def _infer_fresh_class_instance(
    _node: nodes.Call, _context: InferenceContext | None = None
) -> Iterator[Instance]:
    """Mimic the numpy brain of astroid: build a new class each time we are inferred."""
    klass = extract_node("""
    class Fresh:
        def __init__(self):
            self.child = make_fresh()
    """)
    return iter([klass.instantiate_class()])


def _is_make_fresh_call(node: nodes.Call) -> bool:
    return isinstance(node.func, nodes.Name) and node.func.name == "make_fresh"


@pytest.fixture
def fresh_class_transform() -> Iterator[None]:
    manager = AstroidManager()
    transform = inference_tip(_infer_fresh_class_instance)
    manager.register_transform(nodes.Call, transform, _is_make_fresh_call)
    try:
        yield
    finally:
        manager.unregister_transform(nodes.Call, transform, _is_make_fresh_call)


@pytest.mark.usefixtures("fresh_class_transform")
@pytest.mark.parametrize("classes", [[], ["Holder"]])
def test_all_associated_with_classes_rebuilt_on_each_inference(
    default_args: Sequence[str], classes: list[str]
) -> None:
    """Regression test for https://github.com/pylint-dev/pylint/issues/3602.

    Some astroid brains (e.g. the one for ``numpy.ndarray``) return a new ``ClassDef``
    on every inference, whose attributes infer to yet another copy of it.
    ``--all-associated`` used to follow these copies until hitting the recursion limit.
    All the copies must be drawn as one class that every holder is linked to.
    """
    module = parse(
        """
    class Holder:
        def __init__(self):
            self.fresh = make_fresh()
            self.other = OtherHolder()

    class OtherHolder:
        def __init__(self):
            self.fresh = make_fresh()
    """,
        module_name="sample",
    )
    project = Project("sample")
    project.add_module(module)
    config = PyreverseConfig(all_associated=True, classes=classes, module_names=False)
    handler = DiadefsHandler(config=config, args=default_args)

    diagram = handler.get_diadefs(project, Linker(project))[-1]

    assert sorted(obj.title for obj in diagram.objects) == [
        "Fresh",
        "Holder",
        "OtherHolder",
    ]
    assert _process_relations(diagram.relationships) == [
        ("composition", "Fresh", "Fresh"),
        ("composition", "Fresh", "Holder"),
        ("composition", "Fresh", "OtherHolder"),
        ("composition", "OtherHolder", "Holder"),
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
    corr = {"pkg.subpkg2.module2", "pkg.subpkg1.module1.submodule"}

    generator = generator_factory(args=specified_packeges)
    assert len(corr.difference(generator.get_leaf_nodes())) == 0
