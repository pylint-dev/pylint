# Copyright (c) 2008, 2010, 2013 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2021 Mark Byrne <31762852+mbyrnepr2@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""
unit test for visitors.diadefs and extensions.diadefslib modules
"""


import codecs
import os
from difflib import unified_diff
from unittest.mock import patch

import astroid
import pytest

from pylint.pyreverse.diadefslib import DefaultDiadefGenerator, DiadefsHandler
from pylint.pyreverse.inspector import Linker, project_from_files
from pylint.pyreverse.utils import get_annotation, get_visibility, infer_node
from pylint.pyreverse.writer import DotWriter

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
    "only_classnames": False,
    "output_directory": "",
}


class Config:
    """config object for tests"""

    def __init__(self):
        for attr, value in _DEFAULTS.items():
            setattr(self, attr, value)


def _file_lines(path):
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


def get_project(module, name="No Name"):
    """return an astroid project representation"""

    def _astroid_wrapper(func, modname):
        return func(modname)

    return project_from_files([module], _astroid_wrapper, project_name=name)


DOT_FILES = ["packages_No_Name.dot", "classes_No_Name.dot"]


@pytest.fixture(scope="module")
def setup():
    project = get_project(os.path.join(os.path.dirname(__file__), "data"))
    linker = Linker(project)
    CONFIG = Config()
    handler = DiadefsHandler(CONFIG)
    dd = DefaultDiadefGenerator(linker, handler).visit(project)
    for diagram in dd:
        diagram.extract_relationships()
    writer = DotWriter(CONFIG)
    writer.write(dd)
    yield
    for fname in DOT_FILES:
        try:
            os.remove(fname)
        except FileNotFoundError:
            continue


@pytest.mark.usefixtures("setup")
@pytest.mark.parametrize("generated_file", DOT_FILES)
def test_dot_files(generated_file):
    expected_file = os.path.join(os.path.dirname(__file__), "data", generated_file)
    generated = _file_lines(generated_file)
    expected = _file_lines(expected_file)
    generated = "\n".join(generated)
    expected = "\n".join(expected)
    files = f"\n *** expected : {expected_file}, generated : {generated_file} \n"
    diff = "\n".join(
        line for line in unified_diff(expected.splitlines(), generated.splitlines())
    )
    assert expected == generated, f"{files}{diff}"
    os.remove(generated_file)


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
    assert isinstance(node, astroid.AnnAssign)
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
    assign = rf"""
        class A:
            {init_method}
    """
    node = astroid.extract_node(assign)
    instance_attrs = node.instance_attrs
    for _, assign_attrs in instance_attrs.items():
        for assign_attr in assign_attrs:
            got = get_annotation(assign_attr).name
            assert isinstance(assign_attr, astroid.AssignAttr)
            assert got == label, f"got {got} instead of {label} for value {node}"


@patch("pylint.pyreverse.utils.get_annotation")
@patch("astroid.node_classes.NodeNG.infer", side_effect=astroid.InferenceError)
def test_infer_node_1(mock_infer, mock_get_annotation):
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
def test_infer_node_2(mock_infer, mock_get_annotation):
    """Return set(node.infer()) when InferenceError is not raised and an
    annotation has not been returned
    """
    mock_get_annotation.return_value = None
    node = astroid.extract_node("a: str = 'mystr'")
    mock_infer.return_value = "x"
    assert infer_node(node) == set("x")
    assert mock_infer.called
