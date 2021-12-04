# Copyright (c) 2015-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Damien Baty <damien.baty@polyconseil.fr>
# Copyright (c) 2021 Takahide Nojima <nozzy123nozzy@gmail.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>
# Copyright (c) 2021 Mark Byrne <31762852+mbyrnepr2@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""
 for the visitors.diadefs module
"""
# pylint: disable=redefined-outer-name

import os
from typing import Callable

import astroid
import pytest
from astroid import nodes

from pylint.pyreverse import inspector
from pylint.pyreverse.inspector import Project


@pytest.fixture
def project(get_project: Callable) -> Project:
    project = get_project("data", "data")
    linker = inspector.Linker(project)
    linker.visit(project)
    return project


def test_class_implements(project: Project) -> None:
    klass = project.get_module("data.clientmodule_test")["Ancestor"]
    assert hasattr(klass, "implements")
    assert len(klass.implements) == 1
    assert isinstance(klass.implements[0], nodes.ClassDef)
    assert klass.implements[0].name == "Interface"


def test_class_implements_specialization(project: Project) -> None:
    klass = project.get_module("data.clientmodule_test")["Specialization"]
    assert hasattr(klass, "implements")
    assert len(klass.implements) == 0


def test_locals_assignment_resolution(project: Project) -> None:
    klass = project.get_module("data.clientmodule_test")["Specialization"]
    assert hasattr(klass, "locals_type")
    type_dict = klass.locals_type
    assert len(type_dict) == 2
    keys = sorted(type_dict.keys())
    assert keys == ["TYPE", "top"]
    assert len(type_dict["TYPE"]) == 1
    assert type_dict["TYPE"][0].value == "final class"
    assert len(type_dict["top"]) == 1
    assert type_dict["top"][0].value == "class"


def test_instance_attrs_resolution(project: Project) -> None:
    klass = project.get_module("data.clientmodule_test")["Specialization"]
    assert hasattr(klass, "instance_attrs_type")
    type_dict = klass.instance_attrs_type
    assert len(type_dict) == 3
    keys = sorted(type_dict.keys())
    assert keys == ["_id", "relation", "relation2"]
    assert isinstance(type_dict["relation"][0], astroid.bases.Instance), type_dict[
        "relation"
    ]
    assert type_dict["relation"][0].name == "DoNothing"
    assert type_dict["_id"][0] is astroid.Uninferable


def test_concat_interfaces() -> None:
    cls = astroid.extract_node(
        '''
        class IMachin: pass

        class Correct2:
            """docstring"""
            __implements__ = (IMachin,)

        class BadArgument:
            """docstring"""
            __implements__ = (IMachin,)

        class InterfaceCanNowBeFound: #@
            """docstring"""
            __implements__ = BadArgument.__implements__ + Correct2.__implements__
    '''
    )
    interfaces = inspector.interfaces(cls)
    assert [i.name for i in interfaces] == ["IMachin"]


def test_interfaces() -> None:
    module = astroid.parse(
        """
    class Interface(object): pass
    class MyIFace(Interface): pass
    class AnotherIFace(Interface): pass
    class Concrete0(object):
        __implements__ = MyIFace
    class Concrete1:
        __implements__ = (MyIFace, AnotherIFace)
    class Concrete2:
        __implements__ = (MyIFace, AnotherIFace)
    class Concrete23(Concrete1): pass
    """
    )

    for klass, interfaces in (
        ("Concrete0", ["MyIFace"]),
        ("Concrete1", ["MyIFace", "AnotherIFace"]),
        ("Concrete2", ["MyIFace", "AnotherIFace"]),
        ("Concrete23", ["MyIFace", "AnotherIFace"]),
    ):
        klass = module[klass]
        assert [i.name for i in inspector.interfaces(klass)] == interfaces


def test_from_directory(project: Project) -> None:
    expected = os.path.join("tests", "data", "__init__.py")
    assert project.name == "data"
    assert project.path.endswith(expected)


def test_project_node(project: Project) -> None:
    expected = [
        "data",
        "data.clientmodule_test",
        "data.property_pattern",
        "data.suppliermodule_test",
    ]
    assert sorted(project.keys()) == expected
