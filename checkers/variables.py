# Copyright (c) 2003-2014 LOGILAB S.A. (Paris, FRANCE).
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
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""variables checkers for Python code
"""
import os
import sys
from copy import copy

import astroid
from astroid import are_exclusive, builtin_lookup, AstroidBuildingException

from logilab.common.modutils import file_from_modpath

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import (PYMETHODS, is_ancestor_name, is_builtin,
     is_defined_before, is_error, is_func_default, is_func_decorator,
     assign_parent, check_messages, is_inside_except, clobber_in_except,
     get_all_elements)


def in_for_else_branch(parent, stmt):
    """Returns True if stmt in inside the else branch for a parent For stmt."""
    return (isinstance(parent, astroid.For) and
            any(else_stmt.parent_of(stmt) for else_stmt in parent.orelse))

def overridden_method(klass, name):
    """get overridden method if any"""
    try:
        parent = klass.local_attr_ancestors(name).next()
    except (StopIteration, KeyError):
        return None
    try:
        meth_node = parent[name]
    except KeyError:
        # We have found an ancestor defining <name> but it's not in the local
        # dictionary. This may happen with astroid built from living objects.
        return None
    if isinstance(meth_node, astroid.Function):
        return meth_node
    return None

def _get_unpacking_extra_info(node, infered):
    """return extra information to add to the message for unpacking-non-sequence
    and unbalanced-tuple-unpacking errors
    """
    more = ''
    infered_module = infered.root().name
    if node.root().name == infered_module:
        if node.lineno == infered.lineno:
            more = ' %s' % infered.as_string()
        elif infered.lineno:
            more = ' defined at line %s' % infered.lineno
    elif infered.lineno:
        more = ' defined at line %s of %s' % (infered.lineno, infered_module)
    return more

MSGS = {
    'E0601': ('Using variable %r before assignment',
              'used-before-assignment',
              'Used when a local variable is accessed before it\'s \
              assignment.'),
    'E0602': ('Undefined variable %r',
              'undefined-variable',
              'Used when an undefined variable is accessed.'),
    'E0603': ('Undefined variable name %r in __all__',
              'undefined-all-variable',
              'Used when an undefined variable name is referenced in __all__.'),
    'E0604': ('Invalid object %r in __all__, must contain only strings',
              'invalid-all-object',
              'Used when an invalid (non-string) object occurs in __all__.'),
    'E0611': ('No name %r in module %r',
              'no-name-in-module',
              'Used when a name cannot be found in a module.'),

    'W0601': ('Global variable %r undefined at the module level',
              'global-variable-undefined',
              'Used when a variable is defined through the "global" statement \
              but the variable is not defined in the module scope.'),
    'W0602': ('Using global for %r but no assignment is done',
              'global-variable-not-assigned',
              'Used when a variable is defined through the "global" statement \
              but no assignment to this variable is done.'),
    'W0603': ('Using the global statement', # W0121
              'global-statement',
              'Used when you use the "global" statement to update a global \
              variable. PyLint just try to discourage this \
              usage. That doesn\'t mean you can not use it !'),
    'W0604': ('Using the global statement at the module level', # W0103
              'global-at-module-level',
              'Used when you use the "global" statement at the module level \
              since it has no effect'),
    'W0611': ('Unused import %s',
              'unused-import',
              'Used when an imported module or variable is not used.'),
    'W0612': ('Unused variable %r',
              'unused-variable',
              'Used when a variable is defined but not used.'),
    'W0613': ('Unused argument %r',
              'unused-argument',
              'Used when a function or method argument is not used.'),
    'W0614': ('Unused import %s from wildcard import',
              'unused-wildcard-import',
              'Used when an imported module or variable is not used from a \
              \'from X import *\' style import.'),

    'W0621': ('Redefining name %r from outer scope (line %s)',
              'redefined-outer-name',
              'Used when a variable\'s name hide a name defined in the outer \
              scope.'),
    'W0622': ('Redefining built-in %r',
              'redefined-builtin',
              'Used when a variable or function override a built-in.'),
    'W0623': ('Redefining name %r from %s in exception handler',
              'redefine-in-handler',
              'Used when an exception handler assigns the exception \
               to an existing name'),

    'W0631': ('Using possibly undefined loop variable %r',
              'undefined-loop-variable',
              'Used when an loop variable (i.e. defined by a for loop or \
              a list comprehension or a generator expression) is used outside \
              the loop.'),

    'W0632': ('Possible unbalanced tuple unpacking with '
              'sequence%s: '
              'left side has %d label(s), right side has %d value(s)',
              'unbalanced-tuple-unpacking',
              'Used when there is an unbalanced tuple unpacking in assignment'),

    'W0633': ('Attempting to unpack a non-sequence%s',
              'unpacking-non-sequence',
              'Used when something which is not '
              'a sequence is used in an unpack assignment'),

    'W0640': ('Cell variable %s defined in loop',
              'cell-var-from-loop', 
              'A variable used in a closure is defined in a loop. '
              'This will result in all closures using the same value for '
              'the closed-over variable.'),

    }

class VariablesChecker(BaseChecker):
    """checks for
    * unused variables / imports
    * undefined variables
    * redefinition of variable from builtins or from an outer scope
    * use of variable before assignment
    * __all__ consistency
    """

    __implements__ = IAstroidChecker

    name = 'variables'
    msgs = MSGS
    priority = -1
    options = (
               ("init-import",
                {'default': 0, 'type' : 'yn', 'metavar' : '<y_or_n>',
                 'help' : 'Tells whether we should check for unused import in \
__init__ files.'}),
               ("dummy-variables-rgx",
                {'default': ('_$|dummy'),
                 'type' :'regexp', 'metavar' : '<regexp>',
                 'help' : 'A regular expression matching the name of dummy \
variables (i.e. expectedly not used).'}),
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

    def visit_module(self, node):
        """visit module : update consumption analysis variable
        checks globals doesn't overrides builtins
        """
        self._to_consume = [(copy(node.locals), {}, 'module')]
        for name, stmts in node.locals.iteritems():
            if is_builtin(name) and not is_inside_except(stmts[0]):
                # do not print Redefining builtin for additional builtins
                self.add_message('redefined-builtin', args=name, node=stmts[0])

    @check_messages('unused-import', 'unused-wildcard-import', 'redefined-builtin', 'undefined-all-variable', 'invalid-all-object')
    def leave_module(self, node):
        """leave module: check globals
        """
        assert len(self._to_consume) == 1
        not_consumed = self._to_consume.pop()[0]
        # attempt to check for __all__ if defined
        if '__all__' in node.locals:
            assigned = node.igetattr('__all__').next()
            if assigned is not astroid.YES:
                for elt in getattr(assigned, 'elts', ()):
                    try:
                        elt_name = elt.infer().next()
                    except astroid.InferenceError:
                        continue

                    if not isinstance(elt_name, astroid.Const) \
                             or not isinstance(elt_name.value, basestring):
                        self.add_message('invalid-all-object', args=elt.as_string(), node=elt)
                        continue
                    elt_name = elt_name.value
                    # If elt is in not_consumed, remove it from not_consumed
                    if elt_name in not_consumed:
                        del not_consumed[elt_name]
                        continue
                    if elt_name not in node.locals:
                        if not node.package:
                            self.add_message('undefined-all-variable',
                                             args=elt_name,
                                             node=elt)
                        else:
                            basename = os.path.splitext(node.file)[0]
                            if os.path.basename(basename) == '__init__':
                                name = node.name + "." + elt_name
                                try:
                                    file_from_modpath(name.split("."))
                                except ImportError:
                                    self.add_message('undefined-all-variable',
                                                     args=elt_name,
                                                     node=elt)
                                except SyntaxError, exc:
                                    # don't yield an syntax-error warning,
                                    # because it will be later yielded
                                    # when the file will be checked
                                    pass
        # don't check unused imports in __init__ files
        if not self.config.init_import and node.package:
            return
        for name, stmts in not_consumed.iteritems():
            if any(isinstance(stmt, astroid.AssName)
                   and isinstance(stmt.ass_type(), astroid.AugAssign)
                   for stmt in stmts):
                continue
            stmt = stmts[0]
            if isinstance(stmt, astroid.Import):
                self.add_message('unused-import', args=name, node=stmt)
            elif isinstance(stmt, astroid.From) and stmt.modname != '__future__':
                if stmt.names[0][0] == '*':
                    self.add_message('unused-wildcard-import', args=name, node=stmt)
                else:
                    self.add_message('unused-import', args=name, node=stmt)
        del self._to_consume

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
        self._to_consume.append((copy(node.locals), {}, 'comprehension'))

    def leave_genexpr(self, _):
        """leave genexpr: update consumption analysis variable
        """
        # do not check for not used locals here
        self._to_consume.pop()

    def visit_dictcomp(self, node):
        """visit dictcomp: update consumption analysis variable
        """
        self._to_consume.append((copy(node.locals), {}, 'comprehension'))

    def leave_dictcomp(self, _):
        """leave dictcomp: update consumption analysis variable
        """
        # do not check for not used locals here
        self._to_consume.pop()

    def visit_setcomp(self, node):
        """visit setcomp: update consumption analysis variable
        """
        self._to_consume.append((copy(node.locals), {}, 'comprehension'))

    def leave_setcomp(self, _):
        """leave setcomp: update consumption analysis variable
        """
        # do not check for not used locals here
        self._to_consume.pop()

    def visit_function(self, node):
        """visit function: update consumption analysis variable and check locals
        """
        self._to_consume.append((copy(node.locals), {}, 'function'))
        if not (self.linter.is_message_enabled('redefined-outer-name') or
                self.linter.is_message_enabled('redefined-builtin')):
            return
        globs = node.root().globals
        for name, stmt in node.items():
            if is_inside_except(stmt):
                continue
            if name in globs and not isinstance(stmt, astroid.Global):
                line = globs[name][0].fromlineno
                dummy_rgx = self.config.dummy_variables_rgx
                if not dummy_rgx.match(name):
                    self.add_message('redefined-outer-name', args=(name, line), node=stmt)
            elif is_builtin(name):
                # do not print Redefining builtin for additional builtins
                self.add_message('redefined-builtin', args=name, node=stmt)

    def leave_function(self, node):
        """leave function: check function's locals are consumed"""
        not_consumed = self._to_consume.pop()[0]
        if not (self.linter.is_message_enabled('unused-variable') or
                self.linter.is_message_enabled('unused-argument')):
            return
        # don't check arguments of function which are only raising an exception
        if is_error(node):
            return
        # don't check arguments of abstract methods or within an interface
        is_method = node.is_method()
        klass = node.parent.frame()
        if is_method and (klass.type == 'interface' or node.is_abstract()):
            return
        authorized_rgx = self.config.dummy_variables_rgx
        called_overridden = False
        argnames = node.argnames()
        for name, stmts in not_consumed.iteritems():
            # ignore some special names specified by user configuration
            if authorized_rgx.match(name):
                continue
            # ignore names imported by the global statement
            # FIXME: should only ignore them if it's assigned latter
            stmt = stmts[0]
            if isinstance(stmt, astroid.Global):
                continue
            # care about functions with unknown argument (builtins)
            if name in argnames:
                if is_method:
                    # don't warn for the first argument of a (non static) method
                    if node.type != 'staticmethod' and name == argnames[0]:
                        continue
                    # don't warn for argument of an overridden method
                    if not called_overridden:
                        overridden = overridden_method(klass, node.name)
                        called_overridden = True
                    if overridden is not None and name in overridden.argnames():
                        continue
                    if node.name in PYMETHODS and node.name not in ('__init__', '__new__'):
                        continue
                # don't check callback arguments XXX should be configurable
                if node.name.startswith('cb_') or node.name.endswith('_cb'):
                    continue
                self.add_message('unused-argument', args=name, node=stmt)
            else:
                self.add_message('unused-variable', args=name, node=stmt)

    @check_messages('global-variable-undefined', 'global-variable-not-assigned', 'global-statement',
                    'global-at-module-level', 'redefined-builtin')
    def visit_global(self, node):
        """check names imported exists in the global scope"""
        frame = node.frame()
        if isinstance(frame, astroid.Module):
            self.add_message('global-at-module-level', node=node)
            return
        module = frame.root()
        default_message = True
        for name in node.names:
            try:
                assign_nodes = module.getattr(name)
            except astroid.NotFoundError:
                # unassigned global, skip
                assign_nodes = []
            for anode in assign_nodes:
                if anode.parent is None:
                    # node returned for builtin attribute such as __file__,
                    # __doc__, etc...
                    continue
                if anode.frame() is frame:
                    # same scope level assignment
                    break
            else:
                # global but no assignment
                self.add_message('global-variable-not-assigned', args=name, node=node)
                default_message = False
            if not assign_nodes:
                continue
            for anode in assign_nodes:
                if anode.parent is None:
                    self.add_message('redefined-builtin', args=name, node=node)
                    break
                if anode.frame() is module:
                    # module level assignment
                    break
            else:
                # global undefined at the module scope
                self.add_message('global-variable-undefined', args=name, node=node)
                default_message = False
        if default_message:
            self.add_message('global-statement', node=node)

    def _check_late_binding_closure(self, node, assignment_node, scope_type):
        node_scope = node.scope()
        if not isinstance(node_scope, (astroid.Lambda, astroid.Function)):
            return

        if isinstance(assignment_node, astroid.Comprehension):
            if assignment_node.parent.parent_of(node.scope()):
                self.add_message('cell-var-from-loop', node=node, args=node.name)
        else:
            assign_scope = assignment_node.scope()
            maybe_for = assignment_node
            while not isinstance(maybe_for, astroid.For):
                if maybe_for is assign_scope:
                    break
                maybe_for = maybe_for.parent
            else:
                if maybe_for.parent_of(node_scope) and not isinstance(node_scope.statement(), astroid.Return):
                    self.add_message('cell-var-from-loop', node=node, args=node.name)
        
    def _loopvar_name(self, node, name):
        # filter variables according to node's scope
        # XXX used to filter parents but don't remember why, and removing this
        # fixes a W0631 false positive reported by Paul Hachmann on 2008/12 on
        # python-projects (added to func_use_for_or_listcomp_var test)
        #astmts = [stmt for stmt in node.lookup(name)[1]
        #          if hasattr(stmt, 'ass_type')] and
        #          not stmt.statement().parent_of(node)]
        if not self.linter.is_message_enabled('undefined-loop-variable'):
            return
        astmts = [stmt for stmt in node.lookup(name)[1]
                  if hasattr(stmt, 'ass_type')]
        # filter variables according their respective scope test is_statement
        # and parent to avoid #74747. This is not a total fix, which would
        # introduce a mechanism similar to special attribute lookup in
        # modules. Also, in order to get correct inference in this case, the
        # scope lookup rules would need to be changed to return the initial
        # assignment (which does not exist in code per se) as well as any later
        # modifications.
        if not astmts or (astmts[0].is_statement or astmts[0].parent) \
             and astmts[0].statement().parent_of(node):
            _astmts = []
        else:
            _astmts = astmts[:1]
        for i, stmt in enumerate(astmts[1:]):
            if (astmts[i].statement().parent_of(stmt)
                and not in_for_else_branch(astmts[i].statement(), stmt)):
                continue
            _astmts.append(stmt)
        astmts = _astmts
        if len(astmts) == 1:
            ass = astmts[0].ass_type()
            if isinstance(ass, (astroid.For, astroid.Comprehension, astroid.GenExpr)) \
                   and not ass.statement() is node.statement():
                self.add_message('undefined-loop-variable', args=name, node=node)

    @check_messages('redefine-in-handler')
    def visit_excepthandler(self, node):
        for name in get_all_elements(node.name):
            clobbering, args = clobber_in_except(name)
            if clobbering:
                self.add_message('redefine-in-handler', args=args, node=name)

    def visit_assname(self, node):
        if isinstance(node.ass_type(), astroid.AugAssign):
            self.visit_name(node)

    def visit_delname(self, node):
        self.visit_name(node)

    @check_messages(*(MSGS.keys()))
    def visit_name(self, node):
        """check that a name is defined if the current scope and doesn't
        redefine a built-in
        """
        stmt = node.statement()
        if stmt.fromlineno is None:
            # name node from a astroid built from live code, skip
            assert not stmt.root().file.endswith('.py')
            return
        name = node.name
        frame = stmt.scope()
        # if the name node is used as a function default argument's value or as
        # a decorator, then start from the parent frame of the function instead
        # of the function frame - and thus open an inner class scope
        if (is_func_default(node) or is_func_decorator(node)
            or is_ancestor_name(frame, node)):
            start_index = len(self._to_consume) - 2
        else:
            start_index = len(self._to_consume) - 1
        # iterates through parent scopes, from the inner to the outer
        base_scope_type = self._to_consume[start_index][-1]
        for i in range(start_index, -1, -1):
            to_consume, consumed, scope_type = self._to_consume[i]
            # if the current scope is a class scope but it's not the inner
            # scope, ignore it. This prevents to access this scope instead of
            # the globals one in function members when there are some common
            # names. The only exception is when the starting scope is a
            # comprehension and its direct outer scope is a class
            if scope_type == 'class' and i != start_index and not (
                base_scope_type == 'comprehension' and i == start_index-1):
                # XXX find a way to handle class scope in a smoother way
                continue
            # the name has already been consumed, only check it's not a loop
            # variable used outside the loop
            if name in consumed:
                defnode = assign_parent(consumed[name][0])
                self._check_late_binding_closure(node, defnode, scope_type)
                self._loopvar_name(node, name)
                break
            # mark the name as consumed if it's defined in this scope
            # (i.e. no KeyError is raised by "to_consume[name]")
            try:
                consumed[name] = to_consume[name]
            except KeyError:
                continue
            # checks for use before assignment
            defnode = assign_parent(to_consume[name][0])
            if defnode is not None:
                self._check_late_binding_closure(node, defnode, scope_type)
                defstmt = defnode.statement()
                defframe = defstmt.frame()
                maybee0601 = True
                if not frame is defframe:
                    maybee0601 = False
                elif defframe.parent is None:
                    # we are at the module level, check the name is not
                    # defined in builtins
                    if name in defframe.scope_attrs or builtin_lookup(name)[1]:
                        maybee0601 = False
                else:
                    # we are in a local scope, check the name is not
                    # defined in global or builtin scope
                    if defframe.root().lookup(name)[1]:
                        maybee0601 = False
                    else:
                        # check if we have a nonlocal
                        if name in defframe.locals:
                            maybee0601 = not any(isinstance(child, astroid.Nonlocal)
                                                 and name in child.names
                                                 for child in defframe.get_children())
                if (maybee0601
                    and stmt.fromlineno <= defstmt.fromlineno
                    and not is_defined_before(node)
                    and not are_exclusive(stmt, defstmt, ('NameError', 'Exception', 'BaseException'))):
                    if defstmt is stmt and isinstance(node, (astroid.DelName,
                                                             astroid.AssName)):
                        self.add_message('undefined-variable', args=name, node=node)
                    elif self._to_consume[-1][-1] != 'lambda':
                        # E0601 may *not* occurs in lambda scope
                        self.add_message('used-before-assignment', args=name, node=node)
            if isinstance(node, astroid.AssName): # Aug AssName
                del consumed[name]
            else:
                del to_consume[name]
            # check it's not a loop variable used outside the loop
            self._loopvar_name(node, name)
            break
        else:
            # we have not found the name, if it isn't a builtin, that's an
            # undefined name !
            if not (name in astroid.Module.scope_attrs or is_builtin(name)
                    or name in self.config.additional_builtins):
                self.add_message('undefined-variable', args=name, node=node)

    @check_messages('no-name-in-module')
    def visit_import(self, node):
        """check modules attribute accesses"""
        for name, _ in node.names:
            parts = name.split('.')
            try:
                module = node.infer_name_module(parts[0]).next()
            except astroid.ResolveError:
                continue
            self._check_module_attrs(node, module, parts[1:])

    @check_messages('no-name-in-module')
    def visit_from(self, node):
        """check modules attribute accesses"""
        name_parts = node.modname.split('.')
        level = getattr(node, 'level', None)
        try:
            module = node.root().import_module(name_parts[0], level=level)
        except AstroidBuildingException:
            return
        except Exception, exc:
            print 'Unhandled exception in VariablesChecker:', exc
            return
        module = self._check_module_attrs(node, module, name_parts[1:])
        if not module:
            return
        for name, _ in node.names:
            if name == '*':
                continue
            self._check_module_attrs(node, module, name.split('.'))

    @check_messages('unbalanced-tuple-unpacking', 'unpacking-non-sequence')
    def visit_assign(self, node):
        """Check unbalanced tuple unpacking for assignments
        and unpacking non-sequences.
        """
        if not isinstance(node.targets[0], (astroid.Tuple, astroid.List)):
            return

        targets = node.targets[0].itered()
        try:
            for infered in node.value.infer():
                self._check_unpacking(infered, node, targets)
        except astroid.InferenceError:
            return

    def _check_unpacking(self, infered, node, targets):
        """ Check for unbalanced tuple unpacking
        and unpacking non sequences.
        """
        if infered is astroid.YES:
            return
        if isinstance(infered, (astroid.Tuple, astroid.List)):
            # attempt to check unpacking is properly balanced
            values = infered.itered()
            if len(targets) != len(values):
                self.add_message('unbalanced-tuple-unpacking', node=node,
                                 args=(_get_unpacking_extra_info(node, infered),
                                       len(targets),
                                       len(values)))
        # attempt to check unpacking may be possible (ie RHS is iterable)
        elif isinstance(infered, astroid.Instance):
            for meth in ('__iter__', '__getitem__'):
                try:
                    infered.getattr(meth)
                    break
                except astroid.NotFoundError:
                    continue
            else:
                self.add_message('unpacking-non-sequence', node=node,
                                 args=(_get_unpacking_extra_info(node, infered),))
        else:
            self.add_message('unpacking-non-sequence', node=node,
                             args=(_get_unpacking_extra_info(node, infered),))


    def _check_module_attrs(self, node, module, module_names):
        """check that module_names (list of string) are accessible through the
        given module
        if the latest access name corresponds to a module, return it
        """
        assert isinstance(module, astroid.Module), module
        while module_names:
            name = module_names.pop(0)
            if name == '__dict__':
                module = None
                break
            try:
                module = module.getattr(name)[0].infer().next()
                if module is astroid.YES:
                    return None
            except astroid.NotFoundError:
                self.add_message('no-name-in-module', args=(name, module.name), node=node)
                return None
            except astroid.InferenceError:
                return None
        if module_names:
            # FIXME: other message if name is not the latest part of
            # module_names ?
            modname = module and module.name or '__dict__'
            self.add_message('no-name-in-module', node=node,
                             args=('.'.join(module_names), modname))
            return None
        if isinstance(module, astroid.Module):
            return module
        return None


class VariablesChecker3k(VariablesChecker):
    '''Modified variables checker for 3k'''
    # listcomp have now also their scope

    def visit_listcomp(self, node):
        """visit dictcomp: update consumption analysis variable
        """
        self._to_consume.append((copy(node.locals), {}, 'comprehension'))

    def leave_listcomp(self, _):
        """leave dictcomp: update consumption analysis variable
        """
        # do not check for not used locals here
        self._to_consume.pop()

    def leave_module(self, node):
        """ Update consumption analysis variable
        for metaclasses.
        """
        for klass in node.nodes_of_class(astroid.Class):
            if klass._metaclass:
                metaclass = klass.metaclass()
                module_locals = self._to_consume[0][0]

                if isinstance(klass._metaclass, astroid.Name):
                    module_locals.pop(klass._metaclass.name, None)
                if metaclass:                
                    # if it uses a `metaclass=module.Class`                            
                    module_locals.pop(metaclass.root().name, None)
        super(VariablesChecker3k, self).leave_module(node)

if sys.version_info >= (3, 0):
    VariablesChecker = VariablesChecker3k


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(VariablesChecker(linter))
