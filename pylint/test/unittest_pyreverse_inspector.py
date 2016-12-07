# Copyright (c) 2015-2016 Claudiu Popa <pcmanticore@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""
 for the visitors.diadefs module
"""
import os

import astroid
from astroid import nodes
from astroid import bases
from astroid import manager

from pylint.pyreverse import inspector
from unittest_pyreverse_writer import get_project

MANAGER = manager.AstroidManager()


def astroid_wrapper(func, modname):
    return func(modname)


class TestLinker(object):

    def setup_method(self):
        self.project = get_project('data', 'data')
        self.linker = inspector.Linker(self.project)
        self.linker.visit(self.project)

    def test_class_implements(self):
        klass = self.project.get_module('data.clientmodule_test')['Ancestor']
        assert hasattr(klass, 'implements')
        assert len(klass.implements) == 1
        assert isinstance(klass.implements[0], nodes.ClassDef)
        assert klass.implements[0].name == "Interface"
        klass = self.project.get_module('data.clientmodule_test')['Specialization']
        assert hasattr(klass, 'implements')
        assert len(klass.implements) == 0

    def test_locals_assignment_resolution(self):
        klass = self.project.get_module('data.clientmodule_test')['Specialization']
        assert hasattr(klass, 'locals_type')
        type_dict = klass.locals_type
        assert len(type_dict) == 2
        keys = sorted(type_dict.keys())
        assert keys == ['TYPE', 'top']
        assert len(type_dict['TYPE']) == 1
        assert type_dict['TYPE'][0].value == 'final class'
        assert len(type_dict['top']) == 1
        assert type_dict['top'][0].value == 'class'

    def test_instance_attrs_resolution(self):
        klass = self.project.get_module('data.clientmodule_test')['Specialization']
        assert hasattr(klass, 'instance_attrs_type')
        type_dict = klass.instance_attrs_type
        assert len(type_dict) == 2
        keys = sorted(type_dict.keys())
        assert keys == ['_id', 'relation']
        assert isinstance(type_dict['relation'][0], bases.Instance), \
            type_dict['relation']
        assert type_dict['relation'][0].name == 'DoNothing'
        assert type_dict['_id'][0] is astroid.YES

    def test_concat_interfaces(self):
        cls = astroid.extract_node('''
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
        ''')
        interfaces = inspector.interfaces(cls)
        assert [i.name for i in interfaces] == ['IMachin']

    def test_interfaces(self):
        module = astroid.parse('''
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
        ''')

        for klass, interfaces in (('Concrete0', ['MyIFace']),
                                  ('Concrete1', ['MyIFace', 'AnotherIFace']),
                                  ('Concrete2', ['MyIFace', 'AnotherIFace']),
                                  ('Concrete23', ['MyIFace', 'AnotherIFace'])):
            klass = module[klass]
            assert [i.name for i in inspector.interfaces(klass)] == interfaces

    def test_from_directory(self):
        expected = os.path.join('pylint', 'test', 'data', '__init__.py')
        assert self.project.name == 'data'
        assert self.project.path.endswith(expected), self.project.path

    def test_project_node(self):
        expected = [
            'data', 'data.clientmodule_test',
            'data.suppliermodule_test',
        ]
        assert sorted(self.project.keys()) == expected
