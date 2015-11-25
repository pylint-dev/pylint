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
import re
from copy import copy

import six

import astroid
from astroid import modutils
from pylint.interfaces import IAstroidChecker, INFERENCE, INFERENCE_FAILURE, HIGH
from pylint.utils import get_global_option
from pylint.checkers import BaseChecker
from pylint.checkers.utils import (
    PYMETHODS, is_ancestor_name, is_builtin,
    is_defined_before, is_error, is_func_default, is_func_decorator,
    assign_parent, check_messages, is_inside_except, clobber_in_except,
    get_all_elements, has_known_bases, node_ignores_exception,
    is_inside_abstract_class, is_comprehension, is_iterable,
    safe_infer)

SPECIAL_OBJ = re.compile("^_{2}[a-z]+_{2}$")
FUTURE = '__future__'
PY3K = sys.version_info >= (3, 0)


def _is_from_future_import(stmt, name):
    """Check if the name is a future import from another module."""
    try:
        module = stmt.do_import_module(stmt.modname)
    except astroid.InferenceError:
        return

    for local_node in module.locals.get(name, []):
        if (isinstance(local_node, astroid.ImportFrom)
                and local_node.modname == FUTURE):
            return True


def in_for_else_branch(parent, stmt):
    """Returns True if stmt in inside the else branch for a parent For stmt."""
    return (isinstance(parent, astroid.For) and
            any(else_stmt.parent_of(stmt) for else_stmt in parent.orelse))

def overridden_method(klass, name):
    """get overridden method if any"""
    try:
        parent = next(klass.local_attr_ancestors(name))
    except (StopIteration, KeyError):
        return None
    try:
        meth_node = parent[name]
    except KeyError:
        # We have found an ancestor defining <name> but it's not in the local
        # dictionary. This may happen with astroid built from living objects.
        return None
    if isinstance(meth_node, astroid.FunctionDef):
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

def _detect_global_scope(node, frame, defframe):
    """ Detect that the given frames shares a global
    scope.

    Two frames shares a global scope when neither
    of them are hidden under a function scope, as well
    as any of parent scope of them, until the root scope.
    In this case, depending from something defined later on
    will not work, because it is still undefined.

    Example:
        class A:
            # B has the same global scope as `C`, leading to a NameError.
            class B(C): ...
        class C: ...

    """
    def_scope = scope = None
    if frame and frame.parent:
        scope = frame.parent.scope()
    if defframe and defframe.parent:
        def_scope = defframe.parent.scope()
    if isinstance(frame, astroid.FunctionDef):
        # If the parent of the current node is a
        # function, then it can be under its scope
        # (defined in, which doesn't concern us) or
        # the `->` part of annotations. The same goes
        # for annotations of function arguments, they'll have
        # their parent the Arguments node.
        if not isinstance(node.parent,
                          (astroid.FunctionDef, astroid.Arguments)):
            return False
    elif any(not isinstance(f, (astroid.ClassDef, astroid.Module))
             for f in (frame, defframe)):
        # Not interested in other frames, since they are already
        # not in a global scope.
        return False

    break_scopes = []
    for s in (scope, def_scope):
        # Look for parent scopes. If there is anything different
        # than a module or a class scope, then they frames don't
        # share a global scope.
        parent_scope = s
        while parent_scope:
            if not isinstance(parent_scope, (astroid.ClassDef, astroid.Module)):
                break_scopes.append(parent_scope)
                break
            if parent_scope.parent:
                parent_scope = parent_scope.parent.scope()
            else:
                break
    if break_scopes and len(set(break_scopes)) != 1:
        # Store different scopes than expected.
        # If the stored scopes are, in fact, the very same, then it means
        # that the two frames (frame and defframe) shares the same scope,
        # and we could apply our lineno analysis over them.
        # For instance, this works when they are inside a function, the node
        # that uses a definition and the definition itself.
        return False
    # At this point, we are certain that frame and defframe shares a scope
    # and the definition of the first depends on the second.
    return frame.lineno < defframe.lineno

def _fix_dot_imports(not_consumed):
    """ Try to fix imports with multiple dots, by returning a dictionary
    with the import names expanded. The function unflattens root imports,
    like 'xml' (when we have both 'xml.etree' and 'xml.sax'), to 'xml.etree'
    and 'xml.sax' respectively.
    """
    # TODO: this should be improved in issue astroid #46
    names = {}
    for name, stmts in six.iteritems(not_consumed):
        if any(isinstance(stmt, astroid.AssignName)
               and isinstance(stmt.assign_type(), astroid.AugAssign)
               for stmt in stmts):
            continue
        for stmt in stmts:
            if not isinstance(stmt, (astroid.ImportFrom, astroid.Import)):
                continue
            for imports in stmt.names:
                second_name = None
                if imports[0] == "*":
                    # In case of wildcard imports,
                    # pick the name from inside the imported module.
                    second_name = name
                else:
                    if imports[0].find(".") > -1 or name in imports:
                        # Most likely something like 'xml.etree',
                        # which will appear in the .locals as 'xml'.
                        # Only pick the name if it wasn't consumed.
                        second_name = imports[0]
                if second_name and second_name not in names:
                    names[second_name] = stmt
    return sorted(names.items(), key=lambda a: a[1].fromlineno)

def _find_frame_imports(name, frame):
    """
    Detect imports in the frame, with the required
    *name*. Such imports can be considered assignments.
    Returns True if an import for the given name was found.
    """
    imports = frame.nodes_of_class((astroid.Import, astroid.ImportFrom))
    for import_node in imports:
        for import_name, import_alias in import_node.names:
            # If the import uses an alias, check only that.
            # Otherwise, check only the import name.
            if import_alias:
                if import_alias == name:
                    return True
            elif import_name and import_name == name:
                return True


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
              variable. Pylint just try to discourage this \
              usage. That doesn\'t mean you can not use it !'),
    'W0604': ('Using the global statement at the module level', # W0103
              'global-at-module-level',
              'Used when you use the "global" statement at the module level \
              since it has no effect'),
    'W0611': ('Unused %s',
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
              `\'from X import *\'` style import.'),

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

    'E0632': ('Possible unbalanced tuple unpacking with '
              'sequence%s: '
              'left side has %d label(s), right side has %d value(s)',
              'unbalanced-tuple-unpacking',
              'Used when there is an unbalanced tuple unpacking in assignment',
              {'old_names': [('W0632', 'unbalanced-tuple-unpacking')]}),

    'E0633': ('Attempting to unpack a non-sequence%s',
              'unpacking-non-sequence',
              'Used when something which is not '
              'a sequence is used in an unpack assignment',
              {'old_names': [('W0633', 'unpacking-non-sequence')]}),

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
    options = (("init-import",
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
               ("callbacks",
                {'default' : ('cb_', '_cb'), 'type' : 'csv',
                 'metavar' : '<callbacks>',
                 'help' : 'List of strings which can identify a callback '
                          'function by name. A callback name must start or '
                          'end with one of those strings.'}
               )
              )
    def __init__(self, linter=None):
        BaseChecker.__init__(self, linter)
        self._to_consume = None  # list of tuples: (to_consume:dict, consumed:dict, scope_type:str)
        self._checking_mod_attr = None

    def visit_module(self, node):
        """visit module : update consumption analysis variable
        checks globals doesn't overrides builtins
        """
        self._to_consume = [(copy(node.locals), {}, 'module')]
        for name, stmts in six.iteritems(node.locals):
            if is_builtin(name) and not is_inside_except(stmts[0]):
                # do not print Redefining builtin for additional builtins
                self.add_message('redefined-builtin', args=name, node=stmts[0])

    @check_messages('unused-import', 'unused-wildcard-import',
                    'redefined-builtin', 'undefined-all-variable',
                    'invalid-all-object')
    def leave_module(self, node):
        """leave module: check globals
        """
        assert len(self._to_consume) == 1
        not_consumed = self._to_consume.pop()[0]
        # attempt to check for __all__ if defined
        if '__all__' in node.locals:
            self._check_all(node, not_consumed)
        # don't check unused imports in __init__ files
        if not self.config.init_import and node.package:
            return

        self._check_imports(not_consumed)

    def _check_all(self, node, not_consumed):
        assigned = next(node.igetattr('__all__'))
        if assigned is astroid.YES:
            return

        for elt in getattr(assigned, 'elts', ()):
            try:
                elt_name = next(elt.infer())
            except astroid.InferenceError:
                continue
            if elt_name is astroid.YES:
                continue

            if (not isinstance(elt_name, astroid.Const)
                    or not isinstance(elt_name.value, six.string_types)):
                self.add_message('invalid-all-object',
                                 args=elt.as_string(), node=elt)
                continue

            elt_name = elt_name.value
            # If elt is in not_consumed, remove it from not_consumed
            if elt_name in not_consumed:
                del not_consumed[elt_name]
                continue

            if elt_name not in node.locals:
                if not node.package:
                    self.add_message('undefined-all-variable',
                                     args=(elt_name, ),
                                     node=elt)
                else:
                    basename = os.path.splitext(node.file)[0]
                    if os.path.basename(basename) == '__init__':
                        name = node.name + "." + elt_name
                        try:
                            modutils.file_from_modpath(name.split("."))
                        except ImportError:
                            self.add_message('undefined-all-variable',
                                             args=(elt_name, ),
                                             node=elt)
                        except SyntaxError:
                            # don't yield an syntax-error warning,
                            # because it will be later yielded
                            # when the file will be checked
                            pass

    def _check_imports(self, not_consumed):
        local_names = _fix_dot_imports(not_consumed)
        checked = set()
        for name, stmt in local_names:
            for imports in stmt.names:
                real_name = imported_name = imports[0]
                if imported_name == "*":
                    real_name = name
                as_name = imports[1]
                if real_name in checked:
                    continue
                if name not in (real_name, as_name):
                    continue
                checked.add(real_name)

                if (isinstance(stmt, astroid.Import) or
                        (isinstance(stmt, astroid.ImportFrom) and
                         not stmt.modname)):
                    if (isinstance(stmt, astroid.ImportFrom) and
                            SPECIAL_OBJ.search(imported_name)):
                        # Filter special objects (__doc__, __all__) etc.,
                        # because they can be imported for exporting.
                        continue
                    if as_name is None:
                        msg = "import %s" % imported_name
                    else:
                        msg = "%s imported as %s" % (imported_name, as_name)
                    self.add_message('unused-import', args=msg, node=stmt)
                elif (isinstance(stmt, astroid.ImportFrom)
                      and stmt.modname != FUTURE):

                    if SPECIAL_OBJ.search(imported_name):
                        # Filter special objects (__doc__, __all__) etc.,
                        # because they can be imported for exporting.
                        continue

                    if _is_from_future_import(stmt, name):
                        # Check if the name is in fact loaded from a
                        # __future__ import in another module.
                        continue

                    if imported_name == '*':
                        self.add_message('unused-wildcard-import',
                                         args=name, node=stmt)
                    else:
                        if as_name is None:
                            msg = "%s imported from %s" % (imported_name, stmt.modname)
                        else:
                            fields = (imported_name, stmt.modname, as_name)
                            msg = "%s imported from %s as %s" % fields
                        self.add_message('unused-import', args=msg, node=stmt)
        del self._to_consume

    def visit_classdef(self, node):
        """visit class: update consumption analysis variable
        """
        self._to_consume.append((copy(node.locals), {}, 'class'))

    def leave_classdef(self, _):
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

    def visit_generatorexp(self, node):
        """visit genexpr: update consumption analysis variable
        """
        self._to_consume.append((copy(node.locals), {}, 'comprehension'))

    def leave_generatorexp(self, _):
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

    def visit_functiondef(self, node):
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
                definition = globs[name][0]
                if (isinstance(definition, astroid.ImportFrom)
                        and definition.modname == FUTURE):
                    # It is a __future__ directive, not a symbol.
                    continue

                line = definition.fromlineno
                dummy_rgx = self.config.dummy_variables_rgx
                if not dummy_rgx.match(name):
                    self.add_message('redefined-outer-name',
                                     args=(name, line), node=stmt)
            elif is_builtin(name):
                # do not print Redefining builtin for additional builtins
                self.add_message('redefined-builtin', args=name, node=stmt)

    def leave_functiondef(self, node):
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
        if is_method and node.is_abstract():
            return
        if is_method and isinstance(klass, astroid.ClassDef):
            confidence = INFERENCE if has_known_bases(klass) else INFERENCE_FAILURE
        else:
            confidence = HIGH
        authorized_rgx = self.config.dummy_variables_rgx
        called_overridden = False
        argnames = node.argnames()
        global_names = set()
        nonlocal_names = set()
        for global_stmt in node.nodes_of_class(astroid.Global):
            global_names.update(set(global_stmt.names))
        for nonlocal_stmt in node.nodes_of_class(astroid.Nonlocal):
            nonlocal_names.update(set(nonlocal_stmt.names))

        for name, stmts in six.iteritems(not_consumed):
            # ignore some special names specified by user configuration
            if authorized_rgx.match(name):
                continue
            # ignore names imported by the global statement
            # FIXME: should only ignore them if it's assigned latter
            stmt = stmts[0]
            if isinstance(stmt, astroid.Global):
                continue
            if isinstance(stmt, (astroid.Import, astroid.ImportFrom)):
                # Detect imports, assigned to global statements.
                if not global_names:
                    continue
                skip = False
                for import_name, import_alias in stmt.names:
                    # If the import uses an alias, check only that.
                    # Otherwise, check only the import name.
                    if import_alias:
                        if import_alias in global_names:
                            skip = True
                            break
                    elif import_name in global_names:
                        skip = True
                        break
                if skip:
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
                # don't check callback arguments
                if any(node.name.startswith(cb) or node.name.endswith(cb)
                       for cb in self.config.callbacks):
                    continue
                self.add_message('unused-argument', args=name, node=stmt,
                                 confidence=confidence)
            else:
                if stmt.parent and isinstance(stmt.parent, astroid.Assign):
                    if name in nonlocal_names:
                        continue
                self.add_message('unused-variable', args=name, node=stmt)

    @check_messages('global-variable-undefined', 'global-variable-not-assigned',
                    'global-statement', 'global-at-module-level',
                    'redefined-builtin')
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
                if not _find_frame_imports(name, frame):
                    self.add_message('global-variable-not-assigned',
                                     args=name, node=node)
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

    def _check_late_binding_closure(self, node, assignment_node):
        def _is_direct_lambda_call():
            return (isinstance(node_scope.parent, astroid.Call)
                    and node_scope.parent.func is node_scope)

        node_scope = node.scope()
        if not isinstance(node_scope, (astroid.Lambda, astroid.FunctionDef)):
            return
        if isinstance(node.parent, astroid.Arguments):
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
                if (maybe_for.parent_of(node_scope)
                        and not _is_direct_lambda_call()
                        and not isinstance(node_scope.statement(), astroid.Return)):
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
            assign = astmts[0].assign_type()
            if (isinstance(assign, (astroid.For, astroid.Comprehension,
                                    astroid.GeneratorExp))
                    and assign.statement() is not node.statement()):
                self.add_message('undefined-loop-variable', args=name, node=node)

    @check_messages('redefine-in-handler')
    def visit_excepthandler(self, node):
        for name in get_all_elements(node.name):
            clobbering, args = clobber_in_except(name)
            if clobbering:
                self.add_message('redefine-in-handler', args=args, node=name)

    def visit_assignname(self, node):
        if isinstance(node.assign_type(), astroid.AugAssign):
            self.visit_name(node)

    def visit_delname(self, node):
        self.visit_name(node)

    @staticmethod
    def _defined_in_function_definition(node, frame):
        in_annotation_or_default = False
        if (isinstance(frame, astroid.FunctionDef) and
                node.statement() is frame):
            in_annotation_or_default = (
                (
                    PY3K and (node in frame.args.annotations
                              or node is frame.args.varargannotation
                              or node is frame.args.kwargannotation)
                )
                or
                frame.args.parent_of(node)
            )
        return in_annotation_or_default

    @staticmethod
    def _next_to_consume(node, name, to_consume):
        # mark the name as consumed if it's defined in this scope
        found_node = to_consume.get(name)
        if (found_node
                and isinstance(node.parent, astroid.Assign)
                and node.parent == found_node[0].parent):
            lhs = found_node[0].parent.targets[0]
            if lhs.name == name: # this name is defined in this very statement
                found_node = None
        return found_node

    @staticmethod
    def _is_variable_violation(node, name, defnode, stmt, defstmt,
                               frame, defframe, base_scope_type,
                               recursive_klass):
        maybee0601 = True
        annotation_return = False
        if frame is not defframe:
            maybee0601 = _detect_global_scope(node, frame, defframe)
        elif defframe.parent is None:
            # we are at the module level, check the name is not
            # defined in builtins
            if name in defframe.scope_attrs or astroid.builtin_lookup(name)[1]:
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

        if (base_scope_type == 'lambda' and
                isinstance(frame, astroid.ClassDef)
                and name in frame.locals):

            # This rule verifies that if the definition node of the
            # checked name is an Arguments node and if the name
            # is used a default value in the arguments defaults
            # and the actual definition of the variable label
            # is happening before the Arguments definition.
            #
            # bar = None
            # foo = lambda bar=bar: bar
            #
            # In this case, maybee0601 should be False, otherwise
            # it should be True.
            maybee0601 = not (isinstance(defnode, astroid.Arguments) and
                              node in defnode.defaults and
                              frame.locals[name][0].fromlineno < defstmt.fromlineno)
        elif (isinstance(defframe, astroid.ClassDef) and
              isinstance(frame, astroid.FunctionDef)):
            # Special rule for function return annotations,
            # which uses the same name as the class where
            # the function lives.
            if (PY3K and node is frame.returns and
                    defframe.parent_of(frame.returns)):
                maybee0601 = annotation_return = True

            if (maybee0601 and defframe.name in defframe.locals and
                    defframe.locals[name][0].lineno < frame.lineno):
                # Detect class assignments with the same
                # name as the class. In this case, no warning
                # should be raised.
                maybee0601 = False
            if isinstance(node.parent, astroid.Arguments):
                maybee0601 = stmt.fromlineno <= defstmt.fromlineno
        elif recursive_klass:
            maybee0601 = True
        else:
            maybee0601 = maybee0601 and stmt.fromlineno <= defstmt.fromlineno
        return maybee0601, annotation_return

    def _ignore_class_scope(self, node, name, frame):
        # Detect if we are in a local class scope, as an assignment.
        # For example, the following is fair game.
        #
        # class A:
        #    b = 1
        #    c = lambda b=b: b * b
        #
        # class B:
        #    tp = 1
        #    def func(self, arg: tp):
        #        ...
        # class C:
        #    tp = 2
        #    def func(self, arg=tp):
        #        ...

        in_annotation_or_default = self._defined_in_function_definition(
            node, frame)
        if in_annotation_or_default:
            frame_locals = frame.parent.scope().locals
        else:
            frame_locals = frame.locals
        return not ((isinstance(frame, astroid.ClassDef) or
                     in_annotation_or_default) and
                    name in frame_locals)

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
        # pylint: disable=too-many-nested-blocks; refactoring this block is a pain.
        for i in range(start_index, -1, -1):
            to_consume, consumed, scope_type = self._to_consume[i]
            # if the current scope is a class scope but it's not the inner
            # scope, ignore it. This prevents to access this scope instead of
            # the globals one in function members when there are some common
            # names. The only exception is when the starting scope is a
            # comprehension and its direct outer scope is a class
            if scope_type == 'class' and i != start_index and not (
                    base_scope_type == 'comprehension' and i == start_index-1):
                if self._ignore_class_scope(node, name, frame):
                    continue

            # the name has already been consumed, only check it's not a loop
            # variable used outside the loop
            if name in consumed:
                defnode = assign_parent(consumed[name][0])
                self._check_late_binding_closure(node, defnode)
                self._loopvar_name(node, name)
                break
            found_node = self._next_to_consume(node, name, to_consume)
            if found_node:
                consumed[name] = found_node
            else:
                continue
            # checks for use before assignment
            defnode = assign_parent(to_consume[name][0])
            if defnode is not None:
                self._check_late_binding_closure(node, defnode)
                defstmt = defnode.statement()
                defframe = defstmt.frame()
                # The class reuses itself in the class scope.
                recursive_klass = (frame is defframe and
                                   defframe.parent_of(node) and
                                   isinstance(defframe, astroid.ClassDef) and
                                   node.name == defframe.name)

                maybee0601, annotation_return = self._is_variable_violation(
                    node, name, defnode, stmt, defstmt,
                    frame, defframe,
                    base_scope_type, recursive_klass)

                if (maybee0601
                        and not is_defined_before(node)
                        and not astroid.are_exclusive(stmt, defstmt, ('NameError',
                                                                      'Exception',
                                                                      'BaseException'))):

                    # Used and defined in the same place, e.g `x += 1` and `del x`
                    defined_by_stmt = (
                        defstmt is stmt
                        and isinstance(node, (astroid.DelName, astroid.AssignName))
                    )

                    if (recursive_klass
                            or defined_by_stmt
                            or annotation_return
                            or isinstance(defstmt, astroid.Delete)):
                        if not node_ignores_exception(node, NameError):
                            self.add_message('undefined-variable', args=name,
                                             node=node)
                    elif base_scope_type != 'lambda':
                        # E0601 may *not* occurs in lambda scope.
                        self.add_message('used-before-assignment', args=name, node=node)
                    elif base_scope_type == 'lambda':
                        # E0601 can occur in class-level scope in lambdas, as in
                        # the following example:
                        #   class A:
                        #      x = lambda attr: f + attr
                        #      f = 42
                        if isinstance(frame, astroid.ClassDef) and name in frame.locals:
                            if isinstance(node.parent, astroid.Arguments):
                                if stmt.fromlineno <= defstmt.fromlineno:
                                    # Doing the following is fine:
                                    #   class A:
                                    #      x = 42
                                    #      y = lambda attr=x: attr
                                    self.add_message('used-before-assignment',
                                                     args=name, node=node)
                            else:
                                self.add_message('undefined-variable',
                                                 args=name, node=node)
                        elif scope_type == 'lambda':
                            self.add_message('undefined-variable',
                                             node=node, args=name)

            del to_consume[name]
            # check it's not a loop variable used outside the loop
            self._loopvar_name(node, name)
            break
        else:
            # we have not found the name, if it isn't a builtin, that's an
            # undefined name !
            if not (name in astroid.Module.scope_attrs or is_builtin(name)
                    or name in self.config.additional_builtins):
                if not node_ignores_exception(node, NameError):
                    self.add_message('undefined-variable', args=name, node=node)

    @check_messages('no-name-in-module')
    def visit_import(self, node):
        """check modules attribute accesses"""
        if node_ignores_exception(node, ImportError):
            # No need to verify this, since ImportError is already
            # handled by the client code.
            return

        for name, _ in node.names:
            parts = name.split('.')
            try:
                module = next(node.infer_name_module(parts[0]))
            except astroid.ResolveError:
                continue
            self._check_module_attrs(node, module, parts[1:])

    @check_messages('no-name-in-module')
    def visit_importfrom(self, node):
        """check modules attribute accesses"""
        if node_ignores_exception(node, ImportError):
            # No need to verify this, since ImportError is already
            # handled by the client code.
            return

        name_parts = node.modname.split('.')
        try:
            module = node.do_import_module(name_parts[0])
        except Exception:
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
            infered = safe_infer(node.value)
            if infered is not None:
                self._check_unpacking(infered, node, targets)
        except astroid.InferenceError:
            return

    def _check_unpacking(self, infered, node, targets):
        """ Check for unbalanced tuple unpacking
        and unpacking non sequences.
        """
        if is_inside_abstract_class(node):
            return
        if is_comprehension(node):
            return
        if infered is astroid.YES:
            return
        if (isinstance(infered.parent, astroid.Arguments) and
                isinstance(node.value, astroid.Name) and
                node.value.name == infered.parent.vararg):
            # Variable-length argument, we can't determine the length.
            return
        if isinstance(infered, (astroid.Tuple, astroid.List)):
            # attempt to check unpacking is properly balanced
            values = infered.itered()
            if len(targets) != len(values):
                # Check if we have starred nodes.
                if any(isinstance(target, astroid.Starred)
                       for target in targets):
                    return
                self.add_message('unbalanced-tuple-unpacking', node=node,
                                 args=(_get_unpacking_extra_info(node, infered),
                                       len(targets),
                                       len(values)))
        # attempt to check unpacking may be possible (ie RHS is iterable)
        else:
            if not is_iterable(infered):
                self.add_message('unpacking-non-sequence', node=node,
                                 args=(_get_unpacking_extra_info(node, infered),))


    def _check_module_attrs(self, node, module, module_names):
        """check that module_names (list of string) are accessible through the
        given module
        if the latest access name corresponds to a module, return it
        """
        assert isinstance(module, astroid.Module), module
        ignored_modules = get_global_option(self, 'ignored-modules',
                                            default=[])
        while module_names:
            name = module_names.pop(0)
            if name == '__dict__':
                module = None
                break
            try:
                module = next(module.getattr(name)[0].infer())
                if module is astroid.YES:
                    return None
            except astroid.NotFoundError:
                if module.name in ignored_modules:
                    return None
                self.add_message('no-name-in-module',
                                 args=(name, module.name), node=node)
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
        module_locals = self._to_consume[0][0]
        module_imports = self._to_consume[0][1]
        consumed = {}

        for klass in node.nodes_of_class(astroid.ClassDef):
            found = metaclass = name = None
            if not klass._metaclass:
                # Skip if this class doesn't use
                # explictly a metaclass, but inherits it from ancestors
                continue

            metaclass = klass.metaclass()

            # Look the name in the already found locals.
            # If it's not found there, look in the module locals
            # and in the imported modules.
            if isinstance(klass._metaclass, astroid.Name):
                name = klass._metaclass.name
            elif metaclass:
                # if it uses a `metaclass=module.Class`
                name = metaclass.root().name

            if name:
                found = consumed.setdefault(
                    name, module_locals.get(name, module_imports.get(name)))

            if found is None and not metaclass:
                name = None
                if isinstance(klass._metaclass, astroid.Name):
                    name = klass._metaclass.name
                elif isinstance(klass._metaclass, astroid.Attribute):
                    name = klass._metaclass.as_string()

                if name is not None:
                    if not (name in astroid.Module.scope_attrs or
                            is_builtin(name) or
                            name in self.config.additional_builtins or
                            name in node.locals):
                        self.add_message('undefined-variable',
                                         node=klass,
                                         args=(name, ))
        # Pop the consumed items, in order to
        # avoid having unused-import false positives
        for name in consumed:
            module_locals.pop(name, None)
        super(VariablesChecker3k, self).leave_module(node)

if sys.version_info >= (3, 0):
    VariablesChecker = VariablesChecker3k


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(VariablesChecker(linter))
