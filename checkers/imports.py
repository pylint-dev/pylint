# Copyright (c) 2003-2006 LOGILAB S.A. (Paris, FRANCE).
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
"""imports checkers for Python code
"""

from logilab.common.graph import get_cycles
from logilab.common.modutils import is_standard_module, is_relative, \
     get_module_part
from logilab.common.ureports import VerbatimText, Paragraph

from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker, EmptyReport
from pylint.checkers.utils import are_exclusive

def get_first_import(context, name, base, level=0):
    """return the node where [base.]<name> is imported or None if not found
    """
    for node in context.values():
        if isinstance(node, astng.Import):
            if name in [iname[0] for iname in node.names]:
                return node
        if isinstance(node, astng.From):
            if base == node.modname and level == node.level and \
                   name in [iname[0] for iname in node.names]:
                return node
            
        
# utilities to represents import dependencies as tree and dot graph ###########

def filter_dependencies_info(dep_info, package_dir, mode='external'):
    """filter external or internal dependencies from dep_info (return a
    new dictionary containing the filtered modules only)
    """
    if mode == 'external':
        filter_func = lambda x: not is_standard_module(x, (package_dir,))
    else:
        assert mode == 'internal'
        filter_func = lambda x: is_standard_module(x, (package_dir,))
    result = {}
    for importee, importers in dep_info.items():
        if filter_func(importee):
            result[importee] = importers
    return result

def make_tree_defs(mod_files_list):
    """get a list of 2-uple (module, list_of_files_which_import_this_module),
    it will return a dictionnary to represent this as a tree
    """
    tree_defs = {}
    for mod, files in mod_files_list:
        node = (tree_defs, ())
        for prefix in mod.split('.'):
            node = node[0].setdefault(prefix, [{}, []])
        node[1] += files
    return tree_defs

def repr_tree_defs(data, indent_str=None):
    """return a string which represents imports as a tree"""
    lines = []
    nodes = data.items()
    for i in range(len(nodes)):
        mod, (sub, files) = nodes[i]
        if not files:
            files = ''
        else:
            files = '(%s)' % ','.join(files)
        if indent_str is None:
            lines.append('%s %s' % (mod, files))
            sub_indent_str = '  '
        else:
            lines.append('%s\-%s %s' % (indent_str, mod, files))
            if i == len(nodes)-1:
                sub_indent_str = '%s  ' % indent_str
            else:
                sub_indent_str = '%s| ' % indent_str
        if sub:
            lines.append(repr_tree_defs(sub, sub_indent_str))
    return '\n'.join(lines)

def dot_node(modname):
    """return the string representation for a dot node"""
    return '"%s" [ label="%s" ];' % (modname, modname)

def dot_edge(from_, to_):
    """return the string representation for a dot edge between two nodes"""
    return'"%s" -> "%s" [ ] ;' % (from_, to_)

DOT_HEADERS = '''rankdir="LR" URL="." concentrate=false
edge[fontsize="10" ]
node[width="0" height="0" fontsize="12" fontcolor="black"]'''

def dependencies_graph(filename, dep_info):
    """write dependencies as defined in the dep_info dictionary as a dot
    (graphviz) file
    """
    done = {}
    stream = open(filename, 'w')
    print >> stream, "digraph g {"
    print >> stream, DOT_HEADERS
    for modname, dependencies in dep_info.items():
        done[modname] = 1
        print >> stream, dot_node(modname)
        for modname in dependencies:
            if not done.has_key(modname):
                done[modname] = 1
                print >> stream, dot_node(modname)
    for depmodname, dependencies in dep_info.items():
        for modname in dependencies:
            print >> stream, dot_edge(modname, depmodname)
    print >> stream,'}'
    stream.close()

def make_graph(filename, dep_info, sect, gtype):
    """generate a dependencies graph and add some information about it in the
    report's section
    """
    dependencies_graph(filename, dep_info)
    sect.append(Paragraph('%simports graph has been written to %s'
                          % (gtype, filename)))


# the import checker itself ###################################################

MSGS = {
    'F0401': ('Unable to import %r (%s)' ,
              'Used when pylint has been unable to import a module.'),
    'R0401': ('Cyclic import (%s)',
              'Used when a cyclic import between two or more modules is \
              detected.'),
    
    'W0401': ('Wildcard import %s',
              'Used when `from module import *` is detected.'),
    'W0402': ('Uses of a deprecated module %r',
              'Used a module marked as deprecated is imported.'),
    'W0403': ('Relative import %r',
              'Used when an import relative to the package directory is \
              detected.'),
    'W0404': ('Reimport %r (imported line %s)',
              'Used when a module is reimported multiple times.'),
    'W0406': ('Module import itself',
              'Used when a module is importing itself.'),
    
    'W0410': ('__future__ import is not the first non docstring statement',
              'Python 2.5 and greater require __future__ import to be the \
              first non docstring statement in the module.'),
    }

class ImportsChecker(BaseChecker):
    """checks for                                                              
    * external modules dependencies                                            
    * relative / wildcard imports                                                         
    * cyclic imports                                                           
    * uses of deprecated modules
    """
    
    __implements__ = IASTNGChecker

    name = 'imports'
    msgs = MSGS
    priority = -2
    
    options = (('deprecated-modules',
                {'default' : ('regsub','string', 'TERMIOS',
                              'Bastion', 'rexec'),
                 'type' : 'csv',
                 'metavar' : '<modules>',
                 'help' : 'Deprecated modules which should not be used, \
separated by a comma'}
                ),
               ('import-graph',
                {'default' : '',
                 'type' : 'string',
                 'metavar' : '<file.dot>',
                 'help' : 'Create a graph of every (i.e. internal and \
external) dependencies in the given file (report R0402 must not be disabled)'}
                ),
               ('ext-import-graph',
                {'default' : '',
                 'type' : 'string',
                 'metavar' : '<file.dot>',
                 'help' : 'Create a graph of external dependencies in the \
given file (report R0402 must not be disabled)'}
                ),
               ('int-import-graph',
                {'default' : '',
                 'type' : 'string',
                 'metavar' : '<file.dot>',
                 'help' : 'Create a graph of internal dependencies in the \
given file (report R0402 must not be disabled)'}
                ),
               
               )

    def __init__(self, linter=None):
        BaseChecker.__init__(self, linter)
        self.stats = None
        self.import_graph = None
        self.__int_dep_info = self.__ext_dep_info = None
        self.reports = (('R0401', 'External dependencies',
                         self.report_external_dependencies),
                        ('R0402', 'Modules dependencies graph',
                         self.report_dependencies_graph),
                        )
        
    def open(self):
        """called before visiting project (i.e set of modules)"""
        self.linter.add_stats(dependencies={})
        self.linter.add_stats(cycles=[])
        self.stats = self.linter.stats
        self.import_graph = {}
        
    def close(self):
        """called before visiting project (i.e set of modules)"""
        # don't try to compute cycles if the associated message is disabled
        if self.linter.is_message_enabled('R0401'):
            for cycle in get_cycles(self.import_graph):
                self.add_message('R0401', args=' -> '.join(cycle))
         
    def visit_import(self, node):
        """triggered when an import statement is seen"""
        for name, _ in node.names:
            self._check_deprecated(node, name)
            relative = self._check_relative(node, name)
            self._imported_module(node, name, relative)
            # handle reimport
            self._check_reimport(node, name)
        

    def visit_from(self, node):
        """triggered when a from statement is seen"""
        basename = node.modname
        if basename == '__future__':
            # check this is the first non docstring statement in the module
            prev = node.previous_sibling()
            if prev:
                # consecutive future statements are possible
                if not(isinstance(prev, astng.From)
                       and prev.modname == '__future__'):
                    self.add_message('W0410', node=node)
        self._check_deprecated(node, basename)
        level = node.level
        if level > 0: # explicit relative import (leading dots)
            relative = True
        else:
            relative = self._check_relative(node, basename)
        for name, _ in node.names:
            if name == '*':
                self.add_message('W0401', args=basename, node=node)
                continue
            # handle reimport
            self._check_reimport(node, name, basename, level)
            # analyze dependencies
            fullname = '.' * level + '%s.%s' % (basename, name)
            try:
                # XXXFIXME: don't use get_module_part which doesn't take
                # care of package precedence
                fullname = get_module_part(fullname,
                                           context_file=node.root().file)
            except ImportError, ex:
                self.add_message('F0401', args=(fullname, ex), node=node)
                continue
            self._imported_module(node, fullname, relative)
        
    def _imported_module(self, node, mod_path, relative):
        """notify an imported module, used to analyze dependencies
        """
        context_name = node.root().name
        if relative:
            context_parts = context_name.split('.')
            if mod_path.startswith('.'):
                while mod_path.startswith('.'):
                    mod_path = mod_path[1:]
                    del context_parts[-1] # one level upwards
                context_parts.append(mod_path)
            else:
                context_parts[-1] = mod_path
            mod_path = '.'.join(context_parts)
        if context_name == mod_path:
            # module importing itself !
            self.add_message('W0406', node=node)
        elif not is_standard_module(mod_path):
            # handle dependencies
            mod_paths = self.stats['dependencies'].setdefault(mod_path, [])
            if not context_name in mod_paths:
                mod_paths.append(context_name)
            if is_standard_module( mod_path, (self.package_dir(),) ):
                # update import graph
                mgraph = self.import_graph.setdefault(context_name, [])
                if not mod_path in mgraph:
                    mgraph.append(mod_path)

    def _check_relative(self, node, mod_path):
        """check relative import module"""
        # check for relative import
        context_file = node.root().file
        relative = is_relative(mod_path, context_file)
        if relative:
            self.add_message('W0403', args=mod_path, node=node)
        return relative
    
    def _check_deprecated(self, node, mod_path):
        """check if the module is deprecated"""
        for mod_name in self.config.deprecated_modules:
            if mod_path.startswith(mod_name) and \
                   (len(mod_path) == len(mod_name)
                    or mod_path[len(mod_name)] == '.'):
                self.add_message('W0402', node=node, args=mod_path)
    
    def _check_reimport(self, node, name, basename=None, level=0):
        """check if the import is necessary (i.e. not already done)
        """
        frame = node.frame()
        first = get_first_import(frame, name, basename, level)
        if isinstance(first, (astng.Import, astng.From)) and first is not node \
               and not are_exclusive(first, node):
            self.add_message('W0404', node=node, args=(name, first.lineno))
        else:
            root = node.root()
            if root is frame:
                return
            first = get_first_import(root, name, basename)
            if not isinstance(first, (astng.Import, astng.From)):
                return
            if first is not node and not are_exclusive(first, node):
                self.add_message('W0404', node=node,
                                 args=(name, first.lineno))

        
    def report_external_dependencies(self, sect, _, dummy):
        """return a verbatim layout for displaying dependencies
        """
        dep_info = make_tree_defs(self._external_dependencies_info().items())
        if not dep_info:
            raise EmptyReport()
        tree_str = repr_tree_defs(dep_info)
        sect.append(VerbatimText(tree_str))

    def report_dependencies_graph(self, sect, _, dummy):
        """write dependencies as a dot (graphviz) file"""
        dep_info = self.stats['dependencies']        
        if not dep_info or not (self.config.import_graph
                                or self.config.ext_import_graph
                                or self.config.int_import_graph):
            raise EmptyReport()
        filename = self.config.import_graph
        if filename:
            make_graph(filename, dep_info, sect, '')
        filename = self.config.ext_import_graph
        if filename:
            make_graph(filename, self._external_dependencies_info(),
                       sect, 'external ')
        filename = self.config.int_import_graph
        if filename:
            make_graph(filename, self._internal_dependencies_info(),
                       sect, 'internal ')
            
    def _external_dependencies_info(self):
        """return cached external dependencies information or build and
        cache them
        """
        if self.__ext_dep_info is None:
            self.__ext_dep_info = filter_dependencies_info(
                self.stats['dependencies'], self.package_dir(), 'external')
        return self.__ext_dep_info
        
    def _internal_dependencies_info(self):
        """return cached internal dependencies information or build and
        cache them
        """
        if self.__int_dep_info is None:
            self.__int_dep_info = filter_dependencies_info(
                self.stats['dependencies'], self.package_dir(), 'internal')
        return self.__int_dep_info
        
            
def register(linter):
    """required method to auto register this checker """
    linter.register_checker(ImportsChecker(linter))
