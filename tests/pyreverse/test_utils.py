# Copyright (c) 2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Mark Byrne <31762852+mbyrnepr2@users.noreply.github.com>
# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""Tests for pylint.pyreverse.utils"""

from typing import Any
from unittest.mock import patch

import astroid
import pytest
from astroid import nodes

from pylint.pyreverse.utils import get_annotation, get_visibility, infer_node


@pytest.mark.parametrize(
    "names, expected",
    [
        (["__reduce_ex__", "__setattr__"], "special"),
        (["__g_", "____dsf", "__23_9"], "private"),
        (["simple"], "public"),
        (
            ["_", "__", "___", "____", "_____", "___e__", "_nextsimple", "_filter_it_"],
            "protected",
        ),
    ],
)
def test_get_visibility(names, expected):
    for name in names:
        got = get_visibility(name)
        assert got == expected, f"got {got} instead of {expected} for value {name}"


@pytest.mark.parametrize(
    "assign, label",
    [
        ("a: str = None", "Optional[str]"),
        ("a: str = 'mystr'", "str"),
        ("a: Optional[str] = 'str'", "Optional[str]"),
        ("a: Optional[str] = None", "Optional[str]"),
    ],
)
def test_get_annotation_annassign(assign, label):
    """AnnAssign"""
    node = astroid.extract_node(assign)
    got = get_annotation(node.value).name
    assert isinstance(node, nodes.AnnAssign)
    assert got == label, f"got {got} instead of {label} for value {node}"


@pytest.mark.parametrize(
    "init_method, label",
    [
        ("def __init__(self, x: str):                   self.x = x", "str"),
        ("def __init__(self, x: str = 'str'):           self.x = x", "str"),
        ("def __init__(self, x: str = None):            self.x = x", "Optional[str]"),
        ("def __init__(self, x: Optional[str]):         self.x = x", "Optional[str]"),
        ("def __init__(self, x: Optional[str] = None):  self.x = x", "Optional[str]"),
        ("def __init__(self, x: Optional[str] = 'str'): self.x = x", "Optional[str]"),
    ],
)
def test_get_annotation_assignattr(init_method, label):
    """AssignAttr"""
    assign = fr"""
        class A:
            {init_method}
    """
    node = astroid.extract_node(assign)
    instance_attrs = node.instance_attrs
    for _, assign_attrs in instance_attrs.items():
        for assign_attr in assign_attrs:
            got = get_annotation(assign_attr).name
            assert isinstance(assign_attr, nodes.AssignAttr)
            assert got == label, f"got {got} instead of {label} for value {node}"


@patch("pylint.pyreverse.utils.get_annotation")
@patch("astroid.node_classes.NodeNG.infer", side_effect=astroid.InferenceError)
def test_infer_node_1(mock_infer: Any, mock_get_annotation: Any) -> None:
    """Return set() when astroid.InferenceError is raised and an annotation has
    not been returned
    """
    mock_get_annotation.return_value = None
    node = astroid.extract_node("a: str = 'mystr'")
    mock_infer.return_value = "x"
    assert infer_node(node) == set()
    assert mock_infer.called


@patch("pylint.pyreverse.utils.get_annotation")
@patch("astroid.node_classes.NodeNG.infer")
def test_infer_node_2(mock_infer: Any, mock_get_annotation: Any) -> None:
    """Return set(node.infer()) when InferenceError is not raised and an
    annotation has not been returned
    """
    mock_get_annotation.return_value = None
    node = astroid.extract_node("a: str = 'mystr'")
    mock_infer.return_value = "x"
    assert infer_node(node) == set("x")
    assert mock_infer.called


def test_infer_node_3() -> None:
    """Return a set containing a nodes.ClassDef object when the attribute
    has a type annotation"""
    node = astroid.extract_node(
        """
        class Component:
            pass

        class Composite:
            def __init__(self, component: Component):
                self.component = component
    """
    )
    instance_attr = node.instance_attrs.get("component")[0]
    assert isinstance(infer_node(instance_attr), set)
    assert isinstance(infer_node(instance_attr).pop(), nodes.ClassDef)


def test_infer_node_4() -> None:
    """Verify the label for an argument with a typehint of the type
    nodes.Subscript
    """
    node = astroid.extract_node(
        """
        class MyClass:
            def __init__(self, my_int: Optional[int] = None):
                self.my_test_int = my_int
    """
    )

    instance_attr = node.instance_attrs.get("my_test_int")[0]
    assert isinstance(instance_attr, nodes.AssignAttr)

    inferred = infer_node(instance_attr).pop()
    assert isinstance(inferred, nodes.Subscript)
    assert inferred.name == "Optional[int]"
