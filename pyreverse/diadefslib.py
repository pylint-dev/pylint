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

import sys

from logilab.common.configuration import OptionsProviderMixIn
from logilab import astng
from logilab.astng.utils import LocalsVisitor

from pyreverse.extensions.xmlconf import DictSaxHandlerMixIn, PrefReader
from pyreverse.extensions.diagrams import PackageDiagram, ClassDiagram
from pyreverse.utils import FilterMixIn

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

    def resolve_packages(self, diadef, diagram=None):
        """take a package diagram definition dictionnary and return matching
        objects
        """
        if diagram is None:
            diagram = PackageDiagram(diadef.get('name',
                                                'No name packages diagram'))
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
        self.resolve_classes(diadef, diagram)
        return diagram

    def resolve_classes(self, diadef, diagram=None):
        """take a class diagram definition dictionnary and return a Diagram
        instance (given in paramaters or created)
        """
        class_defs = diadef.get('class', [])
        if diagram is None:
            diagram = ClassDiagram(diadef.get('name', 'No name classes diagram'))
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

class OptionHandler:
    """"handle diagram generation options
    """
    def __init__(self, linker, handler):
        if handler:
            self.config = handler.config
            self.show_attr = handler.show_attr
            self.include_module_name = self.config.module_names
        else:
            self.include_module_name = False
        self.linker = linker

    def get_title(self, node ):
        title = node.name
        if self.include_module_name:
            title =  '%s.%s' % (node.root().name , title)
        return title

class DefaultDiadefGenerator(LocalsVisitor, OptionHandler):
    """generate minimum diagram definition for the project :

    * a package diagram including project's modules
    * a class diagram including project's classes
    """
    
    def __init__(self, linker, handler):
        OptionHandler.__init__(self, linker, handler)
        LocalsVisitor.__init__(self)

    def visit_project(self, node):
        """visit an astng.Project node

        create a diagram definition for packages
        """
        if len(node.modules) > 1:
            self.pkgdiagram = PackageDiagram('packages %s' % node.name)
        else:
            self.pkgdiagram = None
        self.classdiagram = ClassDiagram('classes %s' % node.name)

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
        #self._cleanup(node)
        if self.pkgdiagram:
            self.linker.visit(node)
            self.pkgdiagram.add_object(node=node, title=node.name)

    def visit_class(self, node):
        """visit an astng.Class node

        add this class to the class diagram definition
        """
        # XXX display of __builtin__.object in the diagram should be configurable
        if node.name in ('object', 'type') and node.root().name == '__builtin__':
            return
        #self._cleanup(node)
        self.linker.visit(node)     
        title = self.get_title(node)
        self.classdiagram.add_object(node=node, title=title, show_attr=self.show_attr)


    # locals problem seems no more reproduceable
    #def _cleanup( self, node ):
        #"""cleanup locals inserted by the astng builder to mimick python
        #interpretor behaviour
        #"""
        #for loc in ['__dict__','__doc__','__file__','__name__']:
            #try:
                 #del node.locals[ loc ]
            #except:
                #pass

class ClassDiadefGenerator(OptionHandler):
    """generate a class diagram definition including all classes related to a
    given class
    """

    def __init__(self, linker, handler):
        OptionHandler.__init__(self, linker, handler)
        if self.include_module_name == None:
            self.include_module_name = True
    
    def class_diagram(self, project, klass, include_level=-1):
        """return a class diagram definition for the given klass and its related
        klasses. Search deep depends on the include_level parameter (=1 will
        take all classes directly related, while =2 will also take all classes
        related to the one fecthed by=1)
        """

        diagram = ClassDiagram(klass)
        if len(project.modules) > 1:
            module, klass = klass.rsplit('.',1)
            module = project.get_module(module)
        else:
            module = project.modules[0]
            klass = klass.split('.')[-1]
        klass = module.ilookup(klass).next()
        self.extract_classes(diagram, klass, include_level)
        return diagram

    def extract_classes(self, diagram, klass_node, include_level):
        """extract classes related to klass_node until include_level is 0
        """
        if include_level == 0 or diagram.has_node(klass_node):
            return
        self.add_class_def(diagram, klass_node)
        # add all ancestors whatever the include_level ?
        for ancestor in klass_node.ancestors():
            # XXX display of __builtin__.object in the diagram should be configurable
            if ancestor.name == 'object' and ancestor.root().name == '__builtin__':
                continue
            self.extract_classes(diagram, ancestor, include_level)
        include_level -= 1
        # association
        for name, ass_nodes in klass_node.instance_attrs_type.items():
            for ass_node in ass_nodes:
                # XXX could find here class attributes and their type
                if isinstance(ass_node, astng.Instance):
                    ass_node = ass_node._proxied
                if not isinstance(ass_node, astng.Class) \
                       or ass_node.root().name == '__builtin__':
                    continue
                self.extract_classes(diagram, ass_node, include_level)

    def add_class_def(self, diagram, klass_node):
        """add a class definition to the class diagram
        """
        title = self.get_title(klass_node)    
        self.linker.visit(klass_node)
        diagram.add_object(node=klass_node, title=title, show_attr=self.show_attr)

# diagram handler #############################################################

class DiadefsHandler(OptionsProviderMixIn, FilterMixIn):
    """handle diagram definitions :

    get it from user (i.e. xml files) or generate them
    """

    name = 'Diagram definition'
    options = (
        ("diadefs",
         dict(action="store", type='string', metavar="<file>",short='d',
          dest="diadefs_file", default=None,
          help="create diagram according to the diagrams definitions in \
<file>")),
        ("class",
         dict(action="append", type='string', metavar="<class>", short='c',
          dest="classes",  default=(),
          help="create a class diagram with all classes related to <class> ")),
        ("search-level",
        dict(dest="include_level", action="store",type='int',
        metavar='<depth>', default=-1, help='depth of search for associated classes') ),
        ("module-names",
        dict(dest="module_names", action="store",short="m",type='yn', metavar='[yn]',
        default=None, help='include module name in representation of classes') ),
        )

    def __init__(self):

        self.options += FilterMixIn.options
        OptionsProviderMixIn.__init__(self)

    
    def get_diadefs(self, project, linker):
        """get the diagrams configuration data, either from a specified file or
        generated
        :param linker: astng.inspector.Linker(IdGeneratorMixIn, LocalsVisitor)
        :param project: astng.manager.Project        
        """

        #  read and interpret diagram definitions
        diagrams = []
        if self.config.diadefs_file is not None:
            diadefs = read_diadefs_file(self.config.diadefs_file)
            resolver = DiadefsResolverHelper(project, linker)
            for class_diagram in diadefs.get('class-diagram', ()):
                resolver.resolve_classes(class_diagram)
            for package_diagram in diadefs.get('package-diagram', ()):
                resolver.resolve_packages(package_diagram)
        generator = ClassDiadefGenerator(linker, self)
        level = int(self.config.include_level)

        for klass in self.config.classes:
            diagrams.append(generator.class_diagram(project, klass, level))
        # FIXME: generate only if no option provided
        # or generate one
        if not diagrams:
            diagrams += DefaultDiadefGenerator(linker, self).visit(project)
        for diagram in diagrams:
            diagram.extract_relationships()
        return  diagrams
