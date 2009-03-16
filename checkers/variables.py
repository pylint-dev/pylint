# Copyright (c) 2003-2008 LOGILAB S.A. (Paris, FRANCE).
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
"""variables checkers for Python code
"""

from copy import copy

from logilab.common.compat import enumerate
from logilab import astng
from logilab.astng.lookup import builtin_lookup

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import is_error, is_builtin, is_func_default, is_func_decorator, \
     is_ancestor_name, assign_parent, are_exclusive, \
     is_defined_before #, is_parent, FOR_NODE_TYPES


def overridden_method(klass, name):
    """get overriden method if any"""
    try:
        parent = klass.local_attr_ancestors(name).next()
    except (StopIteration, KeyError):
        return None
    try:
        meth_node = parent[name]
    except KeyError:
        # We have found an ancestor defining <name> but it's not in the local
        # dictionary. This may happen with astng built from living objects.
        return None
    # check its a method
    if getattr(meth_node.args, 'args', None) is not None:
        return meth_node
    return None

    
MSGS = {
    'E0601': ('Using variable %r before assignment',
              'Used when a local variable is accessed before it\'s \
              assignment.'),
    'E0602': ('Undefined variable %r',
              'Used when an undefined variable is accessed.'),

    'E0611': ('No name %r in module %r',
              'Used when a name cannot be found in a module.'),
    
    'W0601': ('Global variable %r undefined at the module level',
              'Used when a variable is defined through the "global" statement \
              but the variable is not defined in the module scope.'),
    'W0602': ('Using global for %r but no assigment is done',
              'Used when a variable is defined through the "global" statement \
              but no assigment to this variable is done.'),
    'W0603': ('Using the global statement', # W0121
              'Used when you use the "global" statement to update a global \
              variable. PyLint just try to discourage this \
              usage. That doesn\'t mean you can not use it !'),
    'W0604': ('Using the global statement at the module level', # W0103
              'Used when you use the "global" statement at the module level \
              since it has no effect'),
    'W0611': ('Unused import %s',
              'Used when an imported module or variable is not used.'),
    'W0612': ('Unused variable %r',
              'Used when a variable is defined but not used.'),
    'W0613': ('Unused argument %r',
              'Used when a function or method argument is not used.'),
    'W0614': ('Unused import %s from wildcard import',
              'Used when an imported module or variable is not used from a \
              \'from X import *\' style import.'),
    
    'W0621': ('Redefining name %r from outer scope (line %s)',
              'Used when a variable\'s name hide a name defined in the outer \
              scope.'),
    'W0622': ('Redefining built-in %r',
              'Used when a variable or function override a built-in.'),

    'W0631': ('Using possibly undefined loop variable %r',
              'Used when an loop variable (i.e. defined by a for loop or \
              a list comprehension or a generator expression) is used outside \
              the loop.'),
    }

class VariablesChecker(BaseChecker):
    """checks for                                                              
    * unused variables / imports                                               
    * undefined variables                                                      
    * redefinition of variable from builtins or from an outer scope            
    * use of variable before assigment                                         
    """
    
    __implements__ = IASTNGChecker

    name = 'variables'
    msgs = MSGS
    priority = -1
    options = (
               ("init-import",
                {'default': 0, 'type' : 'yn', 'metavar' : '<y_or_n>',
                 'help' : 'Tells wether we should check for unused import in \
__init__ files.'}),
               ("dummy-variables-rgx",
                {'default': ('_|dummy'), 
                 'type' :'regexp', 'metavar' : '<regexp>',
                 'help' : 'A regular expression matching names used \
                 for dummy variables (i.e. not used).'}),
               ("additional-builtins",
                {'default': (), 'type' : 'csv',
                 'metavar' : '<comma separated list>',
                 'help' : 'List of additional names supposed to be defined in \
builtins. Remember that you should avoid to define new builtins when possible.'
                 }),
               )
    def __init__(self, linter=None):
        BaseChecker.__init__(self, linter)
        self._to_consume = None
        self._checking_mod_attr = None
        self._vars = None
        
    def visit_module(self, node):
        """visit module : update consumption analysis variable
        checks globals doesn't overrides builtins
        """
        mlocals = copy(node.locals)
        # __dict__ is added to module's locals but not available in module's
        # namespace (unlike __doc__, __name__, etc...). But take care __dict__
        # may be assigned somewhere in the module, so remove astng inserted
        # nodes (having None lineno)
        # XXX this could probably be handled in astng
        mlocals['__dict__'] = [n for n in mlocals['__dict__']
                               if n.lineno is not None]
        if not mlocals['__dict__']:
            del mlocals['__dict__']
        self._to_consume = [(mlocals, {}, 'module')]
        self._vars = []
        for name, stmts in node.locals.items():
            if name in ('__name__', '__doc__', '__file__', '__path__') \
                   and len(stmts) == 1:
                # only the definition added by the astng builder, continue
                continue
            if self._is_builtin(name):
                self.add_message('W0622', args=name, node=stmts[0])
        
    def leave_module(self, node):
        """leave module: check globals
        """
        assert len(self._to_consume) == 1
        not_consumed = self._to_consume.pop()[0]
        # don't check unused imports in __init__ files
        if not self.config.init_import and node.package:
            return
        for name, stmts in not_consumed.items():
            stmt = stmts[0]
            if isinstance(stmt, astng.Import):
                self.add_message('W0611', args=name, node=stmt)
            elif isinstance(stmt, astng.From) and stmt.modname != '__future__':
                if stmt.names[0][0] == '*':
                    self.add_message('W0614', args=name, node=stmt)
                else:
                    self.add_message('W0611', args=name, node=stmt)
        del self._to_consume
        del self._vars

    def visit_class(self, node):
        """visit class: update consumption analysis variable
        """
        self._to_consume.append((copy(node.locals), {}, 'class'))
            
    def leave_class(self, _):
        """leave class: update consumption analysis variable
        """
        # do not check for not used locals here (no sense)
        self._to_consume.pop()

    def visit_lambda(self, node):
        """visit lambda: update consumption analysis variable
        """
        self._to_consume.append((copy(node.locals), {}, 'lambda'))
            
    def leave_lambda(self, _):
        """leave lambda: update consumption analysis variable
        """
        # do not check for not used locals here
        self._to_consume.pop()

    def visit_genexpr(self, node):
        """visit genexpr: update consumption analysis variable
        """
        self._to_consume.append((copy(node.locals), {}, 'genexpr'))
            
    def leave_genexpr(self, _):
        """leave genexpr: update consumption analysis variable
        """
        # do not check for not used locals here
        self._to_consume.pop()

    def visit_function(self, node):
        """visit function: update consumption analysis variable and check locals
        """
        globs = node.root().globals
        for name, stmt in node.items():
            if globs.has_key(name) and not isinstance(stmt, astng.Global):
                line = globs[name][0].lineno
                self.add_message('W0621', args=(name, line), node=stmt)
            elif self._is_builtin(name):
                self.add_message('W0622', args=name, node=stmt)
        self._to_consume.append((copy(node.locals), {}, 'function'))
        self._vars.append({})
        
    def leave_function(self, node):
        """leave function: check function's locals are consumed"""
        not_consumed = self._to_consume.pop()[0]
        self._vars.pop(0)
        # don't check arguments of function which are only raising an exception
        if is_error(node):
            return
        # don't check arguments of abstract methods or within an interface
        is_method = node.is_method()
        klass = node.parent.frame()
        if is_method and (klass.type == 'interface' or node.is_abstract()):
            return
        authorized_rgx = self.config.dummy_variables_rgx
        overridden = marker = []
        argnames = node.argnames()
        for name, stmts in not_consumed.iteritems():
            # ignore some special names specified by user configuration
            if authorized_rgx.match(name):
                continue
            # ignore names imported by the global statement
            # FIXME: should only ignore them if it's assigned latter
            stmt = stmts[0]
            if isinstance(stmt, astng.Global):
                continue
            # care about functions with unknown argument (builtins)
            if name in argnames:
                if is_method:
                    # don't warn for the first argument of a (non static) method
                    if node.type != 'staticmethod' and name == argnames[0]:
                        continue
                    # don't warn for argument of an overridden method
                    if overridden is marker:
                        overridden = overridden_method(klass, node.name)
                    if overridden is not None and name in overridden.argnames():
                        continue
                # don't check callback arguments
                if node.name.startswith('cb_') or \
                       node.name.endswith('_cb'):
                    continue
                self.add_message('W0613', args=name, node=node)
            else:
                self.add_message('W0612', args=name, node=stmt)

    def visit_global(self, node):
        """check names imported exists in the global scope"""
        frame = node.frame()
        if isinstance(frame, astng.Module):
            self.add_message('W0604', node=node)
            return        
        module = frame.root()
        default_message = True
        for name in node.names:
            try:
                assign_nodes = module.getattr(name)
            except astng.NotFoundError:
                # unassigned global, skip
                assign_nodes = []
            for anode in assign_nodes:
                if anode.frame() is frame:
                    # same scope level assigment
                    break
            else:
                # global but no assigment
                self.add_message('W0602', args=name, node=node)
                default_message = False
            if not assign_nodes:
                continue
            for anode in assign_nodes:
                if anode.frame() is module:
                    # module level assigment
                    break
            else:
                # global undefined at the module scope
                self.add_message('W0601', args=name, node=node)
                default_message = False
        if default_message:
            self.add_message('W0603', node=node) 

    def _loopvar_name(self, node, name):
        # filter variables according to node's scope
        # XXX used to filter parents but don't remember why, and removing this
        # fixes a W0631 false positive reported by Paul Hachmann on 2008/12 on
        # python-projects (added to func_use_for_or_listcomp_var test)
        #astmts = [stmt for stmt in node.lookup(name)[1]
        #          if hasattr(stmt, 'ass_type')] and
        #          not stmt.statement().parent_of(node)]
        astmts = [stmt for stmt in node.lookup(name)[1]
                  if hasattr(stmt, 'ass_type')]
        # filter variables according their respective scope
        if not astmts or astmts[0].statement().parent_of(node):
            _astmts = []
        else:
            _astmts = astmts[:1]
        for i, stmt in enumerate(astmts[1:]):
            if astmts[i].statement().parent_of(stmt):
                continue
            _astmts.append(stmt)
        astmts = _astmts
        if len(astmts) == 1:
            ass = astmts[0].ass_type()
            if isinstance(ass, (astng.For, astng.Comprehension, astng.GenExpr)) \
                   and not ass.statement() is node.statement():
                self.add_message('W0631', args=name, node=node)

    def visit_assname(self, node):
        if isinstance(node.ass_type(), astng.AugAssign):
            self.visit_name(node)
            
    def visit_delname(self, node):
        self.visit_name(node)
        
    def visit_name(self, node):
        """check that a name is defined if the current scope and doesn't
        redefine a built-in
        """
        name = node.name
        stmt = node.statement()
        # probably "is_statement == True" missing somewhere in astng
        assert stmt.fromlineno is not None, stmt # fromlineno = 0 is ok
        frame = stmt.scope()
        # if the name node is used as a function default argument's value or as
        # a decorator, then start from the parent frame of the function instead
        # of the function frame - and thus open an inner class scope
        if (is_func_default(node, node.name) or is_func_decorator(node)
                                        or is_ancestor_name(frame, node)):
            start_index = len(self._to_consume) - 2
        else:
            start_index = len(self._to_consume) - 1
        # iterates through parent scopes, from the inner to the outer
        for i in range(start_index, -1, -1):
            to_consume, consumed, scope_type = self._to_consume[i]
            # if the current scope is a class scope but it's not the inner
            # scope, ignore it. This prevents to access this scope instead of
            # the globals one in function members when there are some common
            # names
            if scope_type == 'class' and i != start_index:
                continue
            # the name has already been consumed, only check it's not a loop
            # variable used outside the loop
            if consumed.has_key(name):
                self._loopvar_name(node, name)
                break
            # mark the name as consumed if it's defined in this scope
            # (i.e. no KeyError is raised by "to_consume[name]"
            try:
                consumed[name] = to_consume[name]
            except KeyError:
                continue
            else:
                # checks for use before assigment
                # FIXME: the last condition should just check attribute access
                # is protected by a try: except NameError: (similar to #9219)
                defnode = assign_parent(to_consume[name][0])
                if defnode is not None:
                    defstmt = defnode.statement()
                    defframe = defstmt.frame()
                    maybee0601 = True
                    if not frame is defframe:
                        maybee0601 = False
                    elif defframe.parent is None:
                        # we are at the module level, check the name is not
                        # defined in builtins
                        if builtin_lookup(name)[1]:
                            maybee0601 = False
                    else:
                        # we are in a local scope, check the name is not
                        # defined in global or builtin scope
                        if defframe.root().lookup(name)[1]:
                            maybee0601 = False
                    if (maybee0601
                        and stmt.fromlineno <= defstmt.fromlineno
                        and not is_defined_before(node)
                        and not are_exclusive(stmt, defstmt)):
                        if (stmt is defstmt
                            and not isinstance(stmt, astng.AugAssign)
                            and not isinstance(node, astng.DelName)):
                            self.add_message('E0601', args=name, node=node)
                        else:
                            self.add_message('E0602', args=name, node=node)
                if not isinstance(node, astng.AssName): # Aug AssName
                    del to_consume[name]
                # check it's not a loop variable used outside the loop
                self._loopvar_name(node, name)
                break
        else:
            # we have not found the name, if it isn't a builtin, that's an
            # undefined name !
            if not self._is_builtin(name):
                self.add_message('E0602', args=name, node=node)
                
    def visit_import(self, node):
        """check modules attribute accesses"""
        for name, _ in node.names:
            parts = name.split('.')
            try:
                module = node.infer_name_module(parts[0]).next()
            except astng.ResolveError:
                continue
            self._check_module_attrs(node, module, parts[1:])
                                    
    def visit_from(self, node):
        """check modules attribute accesses"""
        name_parts = node.modname.split('.')
        try:
            module = node.root().import_module(name_parts[0])
        except KeyboardInterrupt:
            raise
        except:
            return
        module = self._check_module_attrs(node, module, name_parts[1:])
        if not module:
            return
        for name, _ in node.names:
            if name == '*':
                continue
            self._check_module_attrs(node, module, name.split('.'))

##     def leave_getattr(self, node):
##         """check modules attribute accesses
        
##         this function is a "leave_" because when parsing 'a.b.c'
##         we want to check the innermost expression first.
##         """
##         if isinstance(node.expr, astng.Name):
##             try:
##                 module = node.expr.infer().next()
##             except astng.InferenceError:
##                 return
##             if not isinstance(module, astng.Module):
##                 # Not a module, don't check
##                 return
##         elif self._checking_mod_attr is not None:
##             module = self._checking_mod_attr
##         else:
##             return
##         self._checking_mod_attr = self._check_module_attrs(node, module,
##                                                            [node.attrname])

##     def leave_default(self, node):
##         """by default, reset the _checking_mod_attr attribute"""
##         self._checking_mod_attr = None
        
    def _check_module_attrs(self, node, module, module_names):
        """check that module_names (list of string) are accessible through the
        given module
        if the latest access name corresponds to a module, return it
        """
        assert isinstance(module, astng.Module), module
        while module_names:
            name = module_names.pop(0)
            if name == '__dict__':
                module = None
                break
            try:
                module = module.getattr(name)[0].infer().next()
            except astng.NotFoundError:
                self.add_message('E0611', args=(name, module.name), node=node)
                return None
            except astng.InferenceError:
                return None
        if module_names:
            # FIXME: other message if name is not the latest part of
            # module_names ?
            modname = module and module.name or '__dict__'
            self.add_message('E0611', node=node,
                             args=('.'.join(module_names), modname))
            return None
        if isinstance(module, astng.Module):
            return module
        return None
    
    def _is_builtin(self, name):
        """return True if the name is defined in the native builtin or
        in the user specific builtins
        """
        return is_builtin(name) or name in self.config.additional_builtins
    

def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(VariablesChecker(linter))
