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
from logilab.astng import MANAGER
from logilab.astng.inspector import Linker

from pylint.pyreverse.diadefslib import *

from utils import Config

def astng_wrapper(func, modname):
    return func(modname)

PROJECT = MANAGER.project_from_files(['data'], astng_wrapper)

CONFIG = Config()
HANDLER = DiadefsHandler(CONFIG)

def _process_classes(classes):
    """extract class names of a list"""
    return sorted([(isinstance(c.node, astng.Class), c.title) for c in classes])

def _process_relations(relations):
    """extract relation indices from a relation list"""
    result = []
    for rel_type, rels  in relations.iteritems():
        for rel in rels:
            result.append( (rel_type, rel.from_object.title,
                            rel.to_object.title) )
    result.sort()
    return result


class DiaDefGeneratorTC(unittest.TestCase):
    def test_option_values(self):
        """test for ancestor, associated and module options"""
        handler = DiadefsHandler( Config())
        df_h = DiaDefGenerator(Linker(PROJECT), handler)
        cl_config = Config()
        cl_config.classes = ['Specialization']
        cl_h = DiaDefGenerator(Linker(PROJECT), DiadefsHandler(cl_config) )
        self.assertEqual( (0, 0), df_h._get_levels())
        self.assertEqual( False, df_h.module_names)
        self.assertEqual( (-1, -1), cl_h._get_levels())
        self.assertEqual( True, cl_h.module_names)
        for hndl in [df_h, cl_h]:
            hndl.config.all_ancestors = True
            hndl.config.all_associated = True
            hndl.config.module_names = True
            hndl._set_default_options()
            self.assertEqual( (-1, -1), hndl._get_levels())
            self.assertEqual( True, hndl.module_names)
        handler = DiadefsHandler( Config())
        df_h = DiaDefGenerator(Linker(PROJECT), handler)
        cl_config = Config()
        cl_config.classes = ['Specialization']
        cl_h = DiaDefGenerator(Linker(PROJECT), DiadefsHandler(cl_config) )
        for hndl in [df_h, cl_h]:
            hndl.config.show_ancestors = 2
            hndl.config.show_associated = 1
            hndl.config.module_names = False
            hndl._set_default_options()
            self.assertEqual( (2, 1), hndl._get_levels())
            self.assertEqual( False, hndl.module_names)
    #def test_default_values(self):
        """test efault values for package or class diagrams"""
        # TODO : should test difference between default values for package
        # or class diagrams

class DefaultDiadefGeneratorTC(unittest.TestCase):
    def test_known_values1(self):
        dd = DefaultDiadefGenerator(Linker(PROJECT), HANDLER).visit(PROJECT)
        self.assertEqual(len(dd), 2)
        keys = [d.TYPE for d in dd]
        self.assertEqual(keys, ['package', 'class'])
        pd = dd[0]
        self.assertEqual(pd.title, 'packages No Name')
        modules = sorted([(isinstance(m.node, astng.Module), m.title)
                         for m in pd.objects])
        self.assertEqual(modules, [(True, 'data'),
                                   (True, 'data.clientmodule_test'),
                                   (True, 'data.suppliermodule_test')])
        cd = dd[1]
        self.assertEqual(cd.title, 'classes No Name')
        classes = _process_classes(cd.objects)
        self.assertEqual(classes, [(True, 'Ancestor'),
                                   (True, 'DoNothing'),
                                   (True, 'Interface'),
                                   (True, 'Specialization')]
                          )

    _should_rels = [('association', 'DoNothing', 'Ancestor'),
                    ('association', 'DoNothing', 'Specialization'),
                    ('implements', 'Ancestor', 'Interface'),
                    ('specialization', 'Specialization', 'Ancestor')]
    def test_exctract_relations(self):
        """test extract_relations between classes"""
        cd = DefaultDiadefGenerator(Linker(PROJECT), HANDLER).visit(PROJECT)[1]
        cd.extract_relationships()
        relations = _process_relations(cd.relationships)
        self.assertEqual(relations, self._should_rels)

    def test_functional_relation_extraction(self):
        """functional test of relations extraction;
        different classes possibly in different modules"""
        # XXX should be catching pyreverse environnement problem but doesn't
        # pyreverse doesn't extracts the relations but this test ok
        project = MANAGER.project_from_files(['data'], astng_wrapper)
        handler = DiadefsHandler( Config() )
        diadefs = handler.get_diadefs(project, Linker(project, tag=True) )
        cd = diadefs[1]
        relations = _process_relations(cd.relationships)
        self.assertEqual(relations, self._should_rels)

    def test_known_values2(self):
        project = MANAGER.project_from_files(['data.clientmodule_test'], astng_wrapper)
        dd = DefaultDiadefGenerator(Linker(project), HANDLER).visit(project)
        self.assertEqual(len(dd), 1)
        keys = [d.TYPE for d in dd]
        self.assertEqual(keys, ['class'])
        cd = dd[0]
        self.assertEqual(cd.title, 'classes No Name')
        classes = _process_classes(cd.objects)
        self.assertEqual(classes, [(True, 'Ancestor'),
                                   (True, 'DoNothing'),
                                   (True, 'Specialization')]
                          )

class ClassDiadefGeneratorTC(unittest.TestCase):
    def test_known_values1(self):
        HANDLER.config.classes = ['Specialization']
        cdg = ClassDiadefGenerator(Linker(PROJECT), HANDLER)
        special = 'data.clientmodule_test.Specialization'
        cd = cdg.class_diagram(PROJECT, special)
        self.assertEqual(cd.title, special)
        classes = _process_classes(cd.objects)
        self.assertEqual(classes, [(True, 'data.clientmodule_test.Ancestor'),
                                   (True, special),
                                   (True, 'data.suppliermodule_test.DoNothing'),
                                  ])
        
    def test_known_values2(self):
        HANDLER.config.module_names = False
        cd = ClassDiadefGenerator(Linker(PROJECT), HANDLER).class_diagram(PROJECT, 'data.clientmodule_test.Specialization')
        self.assertEqual(cd.title, 'data.clientmodule_test.Specialization')
        classes = _process_classes(cd.objects)
        self.assertEqual(classes, [(True, 'Ancestor'),
                                   (True, 'DoNothing'),
                                   (True, 'Specialization')
                                  ])


if __name__ == '__main__':
    unittest.main()
