# Copyright (c) 2000-2008 LOGILAB S.A. (Paris, FRANCE).
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
"""handle diagram generation options with diadefs or with default generator
"""

import sys

from logilab import astng
from logilab.astng.utils import LocalsVisitor

from pyreverse.extensions.xmlconf import DictSaxHandlerMixIn, PrefReader
from pyreverse.extensions.diagrams import PackageDiagram, ClassDiagram

# diadefs xml files utilities #################################################

class DiaDefsSaxHandler(DictSaxHandlerMixIn):
    """
    definition of the structure of the diadef file, which will enable the MI
    to fill the DiaDefs dictionary
    """
    _MASTER = {}
    _S_LIST = ('class-diagram', 'package-diagram', 'state-diagram',
               'class', 'package')
    _LIST = ()
    _KEY = ('owner', 'name', 'include')
    _CB = {}


def read_diadefs_file(filename):
    """read a diadef file and return the DiaDef dictionnary"""
    diadefs = {}
    reader = PrefReader(DiaDefsSaxHandler, diadefs)
    try:
        reader.fromFile(filename)
    except:
        import traceback
        traceback.print_exc()
        print >> sys.stderr, 'error while reading file %s' % filename
    return diadefs


class DiadefsResolverHelper:
    """fetch objects in the project according to the diagram definition
    from a XML file
    """
    def __init__(self, project, linker):
        self._p = project
        self.linker = linker

    def resolve_packages(self, diadef, mode, diagram=None):
        """take a package diagram definition dictionnary and return matching
        objects
        """
        if diagram is None:
            diagram = PackageDiagram(diadef.get('name',
                                       'No name packages diagram'), mode)
        for package in diadef['package']:
            name = package['name']
            module = self.get_module(name)
            if module is None:
                continue
            self.linker.visit(module)
            diagram.add_object(name, module)
            if package.get('include', 'no') != 'no':
                for node, title in self.get_classes(module):
                    self.linker.visit(node)
                    diagram.add_object(title, node)
        self.resolve_classes(diadef, mode, diagram)
        return diagram

    def resolve_classes(self, diadef, mode, diagram=None):
        """take a class diagram definition dictionnary and return a Diagram
        instance (given in paramaters or created)
        """
        class_defs = diadef.get('class', [])
        if diagram is None:
            diagram = ClassDiagram(diadef.get('name',
                                    'No name classes diagram'), mode)
        for klass in class_defs:
            name, module = klass['name'], klass.get('owner', '')
            c = self.get_class(module, name)
            if c is None:
                continue
            self.linker.visit(c)
            diagram.add_object(name, c)
        return diagram


    def get_classes(self, module):
        """return all class defined in the given astng module
        """
        classes = []
        for object in module.values():
            if isinstance(object, astng.Class):
                classes.append((object, object.name))
        return classes

    def get_module(self, name):
        """return the astng module corresponding to name if it exists in the
        current project
        """
        try:
            return self._p.get_module(name)
        except KeyError:
            print >> sys.stderr, 'Warning: no module named %s' % name

    def get_class(self, module, name):
        """return the astng class corresponding to module.name if it exists in
        the current project
        """
        try:
            module = self._p.get_module(module)
        except KeyError:
            print >> sys.stderr, 'Warning: no module named %s' % module
        else:
            try:
                return module[name]
            except KeyError:
                print >> sys.stderr, 'Warning: no module class %s in %s' % (
                    name, module)

# diagram generators ##########################################################

class DiaDefGenerator:
    """handle diagram generation options
    """
    def __init__(self, linker, handler):
        """common Diagram Handler initialization"""
        self.config = handler.config
        self._set_default_options()
        self.linker = linker

    def get_title(self, node):
        """get title for objects"""
        title = node.name
        if self.module_names:
            title =  '%s.%s' % (node.root().name, title)
        return title

    def _set_default_options(self):
        """set different default options with _default dictionary"""
        mod = {None:False, True:True, False:False}
        if self.config.classes:
            mod[None] = True
        self.module_names = mod[self.config.module_names]
        self._all_ancestors = mod[self.config.all_ancestors]
        self._all_associated = mod[self.config.all_associated]
        anc_level, ass_level = (0, 0)
        if  self._all_ancestors:
            anc_level = -1
        if self._all_associated:
            ass_level = -1
        if self.config.show_ancestors is not None:
            anc_level = self.config.show_ancestors
        if self.config.show_associated is not None:
            ass_level = self.config.show_associated
        self.anc_level, self.ass_level = anc_level, ass_level

    def _get_levels(self):
        """help function for search levels"""
        return self.anc_level, self.ass_level

    def not_show_builtin(self, node):
        """true if builtins and not show_builtins"""
        builtin = (node.name in ('object', 'type') or 
                    node.root().name == '__builtin__')
        return builtin and not (self.config.show_builtin)

    def add_class(self, node):
        """visit one class and add it to diagram"""
        self.linker.visit(node)
        self.classdiagram.add_object(self.get_title(node), node)

    def get_ancestors(self, node, level):
        """return ancestor nodes of a class node"""
        if level == 0:
            return
        for ancestor in node.ancestors(recurs=False):
            if self.not_show_builtin(ancestor):
                continue
            yield ancestor

    def get_associated(self, klass_node, level):
        """return associated nodes of a class node"""
        if level == 0:
            return
        for name, ass_nodes in klass_node.instance_attrs_type.items():
            for ass_node in ass_nodes:
                if isinstance(ass_node, astng.Instance):
                    ass_node = ass_node._proxied
                if not isinstance(ass_node, astng.Class) \
                       or self.not_show_builtin(ass_node):
                    continue
                yield ass_node

    def extract_classes(self, klass_node, anc_level, ass_level):
        """extract recursively classes related to klass_node
        """
        if self.classdiagram.has_node(klass_node):
            return
        self.add_class(klass_node)

        for ancestor in self.get_ancestors(klass_node, anc_level):
            self.extract_classes(ancestor, anc_level-1, ass_level)

        for ass_node in self.get_associated(klass_node, ass_level):
            self.extract_classes(ass_node, anc_level, ass_level-1)


class DefaultDiadefGenerator(LocalsVisitor, DiaDefGenerator):
    """generate minimum diagram definition for the project :

    * a package diagram including project's modules
    * a class diagram including project's classes
    """

    def __init__(self, linker, handler):
        DiaDefGenerator.__init__(self, linker, handler)
        LocalsVisitor.__init__(self)

    def visit_project(self, node):
        """visit an astng.Project node

        create a diagram definition for packages
        """
        mode = self.config.mode
        if len(node.modules) > 1:
            self.pkgdiagram = PackageDiagram('packages %s' % node.name, mode)
        else:
            self.pkgdiagram = None
        self.classdiagram = ClassDiagram('classes %s' % node.name, mode)

    def leave_project(self, node):
        """leave the astng.Project node

        return the generated diagram definition
        """
        if self.pkgdiagram:
            return self.pkgdiagram, self.classdiagram
        return self.classdiagram,

    def visit_module(self, node):
        """visit an astng.Module node

        add this class to the package diagram definition
        """
        if self.pkgdiagram:
            self.linker.visit(node)
            self.pkgdiagram.add_object(node.name, node)

    def visit_class(self, node):
        """visit an astng.Class node

        add this class to the class diagram definition
        """
        anc_level, ass_level = self._get_levels()
        self.extract_classes(node, anc_level, ass_level)

    def visit_from(self, node):
        """visit astng.From  and catch modules for package diagram
        """
        if self.pkgdiagram:
            self.pkgdiagram.add_depend_relation( node, node.modname )

class ClassDiadefGenerator(DiaDefGenerator):
    """generate a class diagram definition including all classes related to a
    given class
    """

    def __init__(self, linker, handler):
        DiaDefGenerator.__init__(self, linker, handler)

    def class_diagram(self, project, klass):
        """return a class diagram definition for the given klass and its
        related klasses
        """

        self.classdiagram = ClassDiagram(klass, self.config.mode)
        if len(project.modules) > 1:
            module, klass = klass.rsplit('.', 1)
            module = project.get_module(module)
        else:
            module = project.modules[0]
            klass = klass.split('.')[-1]
        klass = module.ilookup(klass).next()

        anc_level, ass_level = self._get_levels()
        self.extract_classes(klass, anc_level, ass_level)
        return self.classdiagram

# diagram handler #############################################################

class DiadefsHandler:
    """handle diagram definitions :

    get it from user (i.e. xml files) or generate them
    """

    def __init__(self, config):
        self.config = config

    def get_diadefs(self, project, linker):
        """get the diagrams configuration data, either from a specified file or
        generated
        :param linker: astng.inspector.Linker(IdGeneratorMixIn, LocalsVisitor)
        :param project: astng.manager.Project        
        """

        #  read and interpret diagram definitions (Diadefs)
        diagrams = []
        if self.config.diadefs_file is not None:
            diadefs = read_diadefs_file(self.config.diadefs_file)
            resolver = DiadefsResolverHelper(project, linker)
            for class_diagram in diadefs.get('class-diagram', ()):
                resolver.resolve_classes(class_diagram)
            for package_diagram in diadefs.get('package-diagram', ()):
                resolver.resolve_packages(package_diagram)
        generator = ClassDiadefGenerator(linker, self)
        for klass in self.config.classes:
            diagrams.append(generator.class_diagram(project, klass))
        if not diagrams:
            diagrams = DefaultDiadefGenerator(linker, self).visit(project)
        for diagram in diagrams:
            diagram.extract_relationships()
        return  diagrams
