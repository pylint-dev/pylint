# Copyright (c) 2000-2004 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""
unittest for the extensions.diadefslib modules
"""

import unittest
import sys

from logilab import astng
from logilab.astng import ASTNGManager
from pyreverse.extensions.diadefslib import *
from logilab.astng.inspector import Linker
from utils import Config

def astng_wrapper(func, modname):
    return func(modname)

project = ASTNGManager().project_from_files(['data'], astng_wrapper)

config = Config()
handler = DiadefsHandler(config)

def _process_classes(classes):
    result = []
    for classe in classes:
        result.append({'node' : isinstance(classe.node, astng.Class),
                       'name' : classe.title})
    result.sort()
    return result

def _process_modules(modules):
    result = []
    for module in modules:
        result.append({'node' : isinstance(module.node, astng.Module),
                       'name': module.title})
    result.sort()
    return result

class DiaDefGeneratorTC(unittest.TestCase):
    def test_known_values(self):
        handler = DiadefsHandler( Config())
        df_h = DiaDefGenerator(Linker(project), handler)
        cl_config = Config()
        cl_config.classes = ['Specialization']
        cl_h = DiaDefGenerator(Linker(project), DiadefsHandler(cl_config) )
        self.assertEquals( (0, 0), df_h._get_levels())
        self.assertEquals( False, df_h.module_names)
        self.assertEquals( (-1, -1), cl_h._get_levels())
        self.assertEquals( True, cl_h.module_names)
        for hndl in [df_h, cl_h]:
            hndl.config.all_ancestors = True
            hndl.config.all_associated = True
            hndl.config.module_names = True
            hndl._set_default_options()
            self.assertEquals( (-1, -1), hndl._get_levels())
            self.assertEquals( True, hndl.module_names)
        handler = DiadefsHandler( Config())
        df_h = DiaDefGenerator(Linker(project), handler)
        cl_config = Config()
        cl_config.classes = ['Specialization']
        cl_h = DiaDefGenerator(Linker(project), DiadefsHandler(cl_config) )
        for hndl in [df_h, cl_h]:
            hndl.config.show_ancestors = 2
            hndl.config.show_associated = 1
            hndl.config.module_names = False
            hndl._set_default_options()
            self.assertEquals( (2, 1), hndl._get_levels())
            self.assertEquals( False, hndl.module_names)


class DefaultDiadefGeneratorTC(unittest.TestCase):
    def test_known_values1(self):
        dd = DefaultDiadefGenerator(Linker(project), handler).visit(project)
        self.assertEquals(len(dd), 2)
        keys = [d.TYPE for d in dd]
        self.assertEquals(keys, ['package', 'class'])
        pd = dd[0]
        self.assertEquals(pd.title, 'packages No Name')
        modules = _process_modules(pd.objects)
        self.assertEquals(modules, [{'node': True, 'name': 'data'},
                                    {'node': True, 'name': 'data.clientmodule_test'},
                                    {'node': True, 'name': 'data.suppliermodule_test'}])
        cd = dd[1]
        self.assertEquals(cd.title, 'classes No Name')
        classes = _process_classes(cd.objects)
        self.assertEquals(classes, [{'node': True, 'name': 'Ancestor'},
                                    {'node': True, 'name': 'DoNothing'},
                                    {'node': True, 'name': 'Interface'},
                                    {'node': True, 'name': 'Specialization'}]
                          )
        
    def test_known_values2(self):
        project = ASTNGManager().project_from_files(['data.clientmodule_test'], astng_wrapper)
        dd = DefaultDiadefGenerator(Linker(project), handler).visit(project)
        self.assertEquals(len(dd), 1)
        keys = [d.TYPE for d in dd]
        self.assertEquals(keys, ['class'])
        cd = dd[0]
        self.assertEquals(cd.title, 'classes No Name')
        classes = _process_classes(cd.objects)
        self.assertEquals(classes, [{'node': True, 'name': 'Ancestor'},
                                    {'node': True, 'name': 'DoNothing'},
                                    {'node': True, 'name': 'Specialization'}]
                          )

class ClassDiadefGeneratorTC(unittest.TestCase):
    def test_known_values1(self):
        handler.config.classes = ['Specialization']
        cdg = ClassDiadefGenerator(Linker(project), handler)
        cd = cdg.class_diagram(project, 'data.clientmodule_test.Specialization')
        self.assertEquals(cd.title, 'data.clientmodule_test.Specialization')
        classes = _process_classes(cd.objects)
        self.assertEquals(classes, [{'node': True, 'name': 'data.clientmodule_test.Ancestor'},
                                    {'node': True, 'name': 'data.clientmodule_test.Specialization'},
                                    {'node': True, 'name': 'data.suppliermodule_test.DoNothing'},
                                    ])
        
    def test_known_values2(self):
        handler.config.module_names = False
        cd = ClassDiadefGenerator(Linker(project), handler).class_diagram(project, 'data.clientmodule_test.Specialization')
        self.assertEquals(cd.title, 'data.clientmodule_test.Specialization')
        classes = _process_classes(cd.objects)
        self.assertEquals(classes, [{'node': True, 'name': 'Ancestor' },
                                    {'node': True, 'name': 'DoNothing'},
                                    {'node': True, 'name': 'Specialization'}
                                    ])

        
class ReadDiadefsFileTC(unittest.TestCase):
    def test_known_values(self):
        dd = read_diadefs_file('data/diadefs.xml')
        keys = dd.keys()
        keys.sort()
        self.assertEquals(keys, ['class-diagram', 'package-diagram'])
        self.assertEquals(len(dd['package-diagram']), 1)
        pd = dd['package-diagram'][0]
        self.assertEquals(pd['name'], 'package dependencies')
        self.assertEquals(pd['package'], [{'name': 'base'},
                                          {'name': 'pyparser'},
                                          {'name': 'xmi_uml'},
                                          {'name': 'xmlconf'},
                                          {'name': 'pyargo'},
                                          {'name': 'pystats'}])
        self.assertEquals(len(dd['class-diagram']), 2)
        cd = dd['class-diagram'][0]
        self.assertEquals(cd['name'], 'object hierarchy')
        self.assertEquals(cd['class'], [{'name': 'FrameMixIn'}, {'name': 'VisitedMixIn'},
                                        {'name': 'AbstractBase'}, {'name': 'AbstractFinal'},
                                        {'name': 'AbstractAttr'}, {'name': 'Project'},
                                        {'name': 'Module'}, {'name': 'Klass'},
                                        {'name': 'Function'}, {'name': 'Attribute'},
                                        {'name': 'Parameter'}])
        cd = dd['class-diagram'][1]
        self.assertEquals(cd['name'], 'pyargo')
        self.assertEquals(cd['class'], [{'name': 'DiaDefsSaxHandler'}, {'name': 'PyParser'},
                                        {'name': 'ArgoWriter'}, {'name': 'IdGeneratorMixIn'},
                                        {'name': 'DiadefsResolverMixIn'}, {'name': 'Visitor'},
                                        {'name': 'FilteredVisitor'}, {'name': 'XMIUMLVisitor'},
                                        {'name': 'DictSaxHandlerMixin'}, {'name': 'PrefReader'}])
        
class DiadefsResolverHelperTC(unittest.TestCase):
    def setUp(self):
        self.helper = DiadefsResolverHelper(project, Linker(project))

    def _assert_class(self, objects, klass):
        for object in objects:
            self.assert_(isinstance(object, klass))
        
    def test_resolve_packages_include_all(self):
        data = {'package': [{'name': 'data.clientmodule_test', 'include': 'all'}]}
        diagram = self.helper.resolve_packages(data, config.mode)
        self._test_resolve_packages_included(diagram)
           
    def test_resolve_packages_include_yes(self):
        data = {'package': [{'name': 'data.clientmodule_test', 'include': 'yes'}]}
        diagram = self.helper.resolve_packages(data, config.mode )
        self._test_resolve_packages_included(diagram)
        
    def test_resolve_packages_include_no(self):
        data = {'package': [{'name': 'data.clientmodule_test', 'include': 'no'}]}
        diagram = self.helper.resolve_packages(data, config.mode)
        self._test_resolve_packages_not_included(diagram)
           
    def test_resolve_packages(self):
        data = {'package': [{'name': 'data.clientmodule_test'}]}
        diagram = self.helper.resolve_packages(data, config.mode)
        self._test_resolve_packages_not_included(diagram)

    def _test_resolve_packages_included(self, data):
        classes = [o for o in data.objects if isinstance(o.node, astng.Class)]
        modules = [o for o in data.objects if isinstance(o.node, astng.Module)]
        self.assertEqual(len(classes), 2)
        self.assertEqual(len(modules), 1)
        
    def _test_resolve_packages_not_included(self, data):
        modules = data.objects
        self.assertEqual(len(modules), 1)
        self._assert_class([c.node for c in modules], astng.Module)
           
    def test_resolve_classes(self):
        data = {'class': [{'name' : 'Specialization', 'owner': 'data.clientmodule_test'}]}
        self.helper.resolve_classes(data, config.mode)
        # FIXME ???
        
if __name__ == '__main__':
    unittest.main()
