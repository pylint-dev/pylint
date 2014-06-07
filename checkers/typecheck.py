# Copyright (c) 2006-2013 LOGILAB S.A. (Paris, FRANCE).
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
"""try to find more bugs in the code using astroid inference capabilities
"""

import re
import shlex

import astroid
from astroid import InferenceError, NotFoundError, YES, Instance

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer, is_super, check_messages

MSGS = {
    'E1101': ('%s %r has no %r member',
              'no-member',
              'Used when a variable is accessed for an unexistent member.'),
    'E1102': ('%s is not callable',
              'not-callable',
              'Used when an object being called has been inferred to a non \
              callable object'),
    'E1103': ('%s %r has no %r member (but some types could not be inferred)',
              'maybe-no-member',
              'Used when a variable is accessed for an unexistent member, but \
              astroid was not able to interpret all possible types of this \
              variable.'),
    'E1111': ('Assigning to function call which doesn\'t return',
              'assignment-from-no-return',
              'Used when an assignment is done on a function call but the \
              inferred function doesn\'t return anything.'),
    'W1111': ('Assigning to function call which only returns None',
              'assignment-from-none',
              'Used when an assignment is done on a function call but the \
              inferred function returns nothing but None.'),

    'E1120': ('No value for argument %s in %s call',
              'no-value-for-parameter',
              'Used when a function call passes too few arguments.'),
    'E1121': ('Too many positional arguments for %s call',
              'too-many-function-args',
              'Used when a function call passes too many positional \
              arguments.'),
    'E1122': ('Duplicate keyword argument %r in %s call',
              'duplicate-keyword-arg',
              'Used when a function call passes the same keyword argument \
              multiple times.',
              {'maxversion': (2, 6)}),
    'E1123': ('Unexpected keyword argument %r in %s call',
              'unexpected-keyword-arg',
              'Used when a function call passes a keyword argument that \
              doesn\'t correspond to one of the function\'s parameter names.'),
    'E1124': ('Argument %r passed by position and keyword in %s call',
              'redundant-keyword-arg',
              'Used when a function call would result in assigning multiple \
              values to a function parameter, one value from a positional \
              argument and one from a keyword argument.'),
    'E1125': ('Missing mandatory keyword argument %r in %s call',
              'missing-kwoa',
              ('Used when a function call does not pass a mandatory'
              ' keyword-only argument.'),
              {'minversion': (3, 0)}),
    }

def _determine_callable(callable_obj):
    # Ordering is important, since BoundMethod is a subclass of UnboundMethod,
    # and Function inherits Lambda.
    if isinstance(callable_obj, astroid.BoundMethod):
        # Bound methods have an extra implicit 'self' argument.
        return callable_obj, 1, callable_obj.type
    elif isinstance(callable_obj, astroid.UnboundMethod):
        return callable_obj, 0, 'unbound method'
    elif isinstance(callable_obj, astroid.Function):
        return callable_obj, 0, callable_obj.type
    elif isinstance(callable_obj, astroid.Lambda):
        return callable_obj, 0, 'lambda'
    elif isinstance(callable_obj, astroid.Class):
        # Class instantiation, lookup __new__ instead.
        # If we only find object.__new__, we can safely check __init__
        # instead.
        try:
            # Use the last definition of __new__.
            new = callable_obj.local_attr('__new__')[-1]
        except astroid.NotFoundError:
            new = None

        if not new or new.parent.scope().name == 'object':
            try:
                # Use the last definition of __init__.
                callable_obj = callable_obj.local_attr('__init__')[-1]
            except astroid.NotFoundError:
                # do nothing, covered by no-init.
                raise ValueError
        else:
            callable_obj = new

        if not isinstance(callable_obj, astroid.Function):
            raise ValueError
        # both have an extra implicit 'cls'/'self' argument.
        return callable_obj, 1, 'constructor'
    else:
        raise ValueError

class TypeChecker(BaseChecker):
    """try to find bugs in the code using type inference
    """

    __implements__ = (IAstroidChecker,)

    # configuration section name
    name = 'typecheck'
    # messages
    msgs = MSGS
    priority = -1
    # configuration options
    options = (('ignore-mixin-members',
                {'default' : True, 'type' : 'yn', 'metavar': '<y_or_n>',
                 'help' : 'Tells whether missing members accessed in mixin \
class should be ignored. A mixin class is detected if its name ends with \
"mixin" (case insensitive).'}
                ),
                ('ignored-modules',
                 {'default': (),
                  'type': 'csv',
                  'metavar': '<module names>',
                  'help': 'List of module names for which member attributes \
should not be checked (useful for modules/projects where namespaces are \
manipulated during runtime and thus existing member attributes cannot be \
deduced by static analysis'},
                 ),
               ('ignored-classes',
                {'default' : ('SQLObject',),
                 'type' : 'csv',
                 'metavar' : '<members names>',
                 'help' : 'List of classes names for which member attributes \
should not be checked (useful for classes with attributes dynamically set).'}
                 ),

               ('zope',
                {'default' : False, 'type' : 'yn', 'metavar': '<y_or_n>',
                 'help' : 'When zope mode is activated, add a predefined set \
of Zope acquired attributes to generated-members.'}
                ),
               ('generated-members',
                {'default' : (
        'REQUEST', 'acl_users', 'aq_parent'),
                 'type' : 'string',
                 'metavar' : '<members names>',
                 'help' : 'List of members which are set dynamically and \
missed by pylint inference system, and so shouldn\'t trigger E0201 when \
accessed. Python regular expressions are accepted.'}
                ),
        )

    def open(self):
        # do this in open since config not fully initialized in __init__
        self.generated_members = list(self.config.generated_members)
        if self.config.zope:
            self.generated_members.extend(('REQUEST', 'acl_users', 'aq_parent'))

    def visit_assattr(self, node):
        if isinstance(node.ass_type(), astroid.AugAssign):
            self.visit_getattr(node)

    def visit_delattr(self, node):
        self.visit_getattr(node)

    @check_messages('no-member', 'maybe-no-member')
    def visit_getattr(self, node):
        """check that the accessed attribute exists

        to avoid to much false positives for now, we'll consider the code as
        correct if a single of the inferred nodes has the accessed attribute.

        function/method, super call and metaclasses are ignored
        """
        # generated_members may containt regular expressions
        # (surrounded by quote `"` and followed by a comma `,`)
        # REQUEST,aq_parent,"[a-zA-Z]+_set{1,2}"' =>
        # ('REQUEST', 'aq_parent', '[a-zA-Z]+_set{1,2}')
        if isinstance(self.config.generated_members, str):
            gen = shlex.shlex(self.config.generated_members)
            gen.whitespace += ','
            gen.wordchars += '[]-+'
            self.config.generated_members = tuple(tok.strip('"') for tok in gen)
        for pattern in self.config.generated_members:
            # attribute is marked as generated, stop here
            if re.match(pattern, node.attrname):
                return
        try:
            infered = list(node.expr.infer())
        except InferenceError:
            return
        # list of (node, nodename) which are missing the attribute
        missingattr = set()
        ignoremim = self.config.ignore_mixin_members
        inference_failure = False
        for owner in infered:
            # skip yes object
            if owner is YES:
                inference_failure = True
                continue
            # skip None anyway
            if isinstance(owner, astroid.Const) and owner.value is None:
                continue
            # XXX "super" / metaclass call
            if is_super(owner) or getattr(owner, 'type', None) == 'metaclass':
                continue
            name = getattr(owner, 'name', 'None')
            if name in self.config.ignored_classes:
                continue
            if ignoremim and name[-5:].lower() == 'mixin':
                continue
            try:
                if not [n for n in owner.getattr(node.attrname)
                        if not isinstance(n.statement(), astroid.AugAssign)]:
                    missingattr.add((owner, name))
                    continue
            except AttributeError:
                # XXX method / function
                continue
            except NotFoundError:
                if isinstance(owner, astroid.Function) and owner.decorators:
                    continue
                if isinstance(owner, Instance) and owner.has_dynamic_getattr():
                    continue
                # explicit skipping of module member access
                if owner.root().name in self.config.ignored_modules:
                    continue
                missingattr.add((owner, name))
                continue
            # stop on the first found
            break
        else:
            # we have not found any node with the attributes, display the
            # message for infered nodes
            done = set()
            for owner, name in missingattr:
                if isinstance(owner, Instance):
                    actual = owner._proxied
                else:
                    actual = owner
                if actual in done:
                    continue
                done.add(actual)
                if inference_failure:
                    msgid = 'maybe-no-member'
                else:
                    msgid = 'no-member'
                self.add_message(msgid, node=node,
                                 args=(owner.display_type(), name,
                                       node.attrname))

    @check_messages('assignment-from-no-return', 'assignment-from-none')
    def visit_assign(self, node):
        """check that if assigning to a function call, the function is
        possibly returning something valuable
        """
        if not isinstance(node.value, astroid.CallFunc):
            return
        function_node = safe_infer(node.value.func)
        # skip class, generator and incomplete function definition
        if not (isinstance(function_node, astroid.Function) and
                function_node.root().fully_defined()):
            return
        if function_node.is_generator() \
               or function_node.is_abstract(pass_is_abstract=False):
            return
        returns = list(function_node.nodes_of_class(astroid.Return,
                                                    skip_klass=astroid.Function))
        if len(returns) == 0:
            self.add_message('assignment-from-no-return', node=node)
        else:
            for rnode in returns:
                if not (isinstance(rnode.value, astroid.Const)
                        and rnode.value.value is None
                        or rnode.value is None):
                    break
            else:
                self.add_message('assignment-from-none', node=node)

    @check_messages(*(MSGS.keys()))
    def visit_callfunc(self, node):
        """check that called functions/methods are inferred to callable objects,
        and that the arguments passed to the function match the parameters in
        the inferred function's definition
        """
        # Build the set of keyword arguments, checking for duplicate keywords,
        # and count the positional arguments.
        keyword_args = set()
        num_positional_args = 0
        for arg in node.args:
            if isinstance(arg, astroid.Keyword):
                keyword = arg.arg
                if keyword in keyword_args:
                    self.add_message('duplicate-keyword-arg', node=node, args=keyword)
                keyword_args.add(keyword)
            else:
                num_positional_args += 1

        called = safe_infer(node.func)
        # only function, generator and object defining __call__ are allowed
        if called is not None and not called.callable():
            self.add_message('not-callable', node=node, args=node.func.as_string())

        try:
            called, implicit_args, callable_name = _determine_callable(called)
        except ValueError:
            # Any error occurred during determining the function type, most of 
            # those errors are handled by different warnings.
            return
        num_positional_args += implicit_args
        if called.args.args is None:
            # Built-in functions have no argument information.
            return

        if len(called.argnames()) != len(set(called.argnames())):
            # Duplicate parameter name (see E9801).  We can't really make sense
            # of the function call in this case, so just return.
            return

        # Analyze the list of formal parameters.
        num_mandatory_parameters = len(called.args.args) - len(called.args.defaults)
        parameters = []
        parameter_name_to_index = {}
        for i, arg in enumerate(called.args.args):
            if isinstance(arg, astroid.Tuple):
                name = None
                # Don't store any parameter names within the tuple, since those
                # are not assignable from keyword arguments.
            else:
                if isinstance(arg, astroid.Keyword):
                    name = arg.arg
                else:
                    assert isinstance(arg, astroid.AssName)
                    # This occurs with:
                    #    def f( (a), (b) ): pass
                    name = arg.name
                parameter_name_to_index[name] = i
            if i >= num_mandatory_parameters:
                defval = called.args.defaults[i - num_mandatory_parameters]
            else:
                defval = None
            parameters.append([(name, defval), False])

        kwparams = {}
        for i, arg in enumerate(called.args.kwonlyargs):
            if isinstance(arg, astroid.Keyword):
                name = arg.arg
            else:
                assert isinstance(arg, astroid.AssName)
                name = arg.name
            kwparams[name] = [called.args.kw_defaults[i], False]

        # Match the supplied arguments against the function parameters.

        # 1. Match the positional arguments.
        for i in range(num_positional_args):
            if i < len(parameters):
                parameters[i][1] = True
            elif called.args.vararg is not None:
                # The remaining positional arguments get assigned to the *args
                # parameter.
                break
            else:
                # Too many positional arguments.
                self.add_message('too-many-function-args', node=node, args=(callable_name,))
                break

        # 2. Match the keyword arguments.
        for keyword in keyword_args:
            if keyword in parameter_name_to_index:
                i = parameter_name_to_index[keyword]
                if parameters[i][1]:
                    # Duplicate definition of function parameter.
                    self.add_message('redundant-keyword-arg', node=node, args=(keyword, callable_name))
                else:
                    parameters[i][1] = True
            elif keyword in kwparams:
                if kwparams[keyword][1]:  # XXX is that even possible?
                    # Duplicate definition of function parameter.
                    self.add_message('redundant-keyword-arg', node=node, args=(keyword, callable_name))
                else:
                    kwparams[keyword][1] = True
            elif called.args.kwarg is not None:
                # The keyword argument gets assigned to the **kwargs parameter.
                pass
            else:
                # Unexpected keyword argument.
                self.add_message('unexpected-keyword-arg', node=node, args=(keyword, callable_name))

        # 3. Match the *args, if any.  Note that Python actually processes
        #    *args _before_ any keyword arguments, but we wait until after
        #    looking at the keyword arguments so as to make a more conservative
        #    guess at how many values are in the *args sequence.
        if node.starargs is not None:
            for i in range(num_positional_args, len(parameters)):
                [(name, defval), assigned] = parameters[i]
                # Assume that *args provides just enough values for all
                # non-default parameters after the last parameter assigned by
                # the positional arguments but before the first parameter
                # assigned by the keyword arguments.  This is the best we can
                # get without generating any false positives.
                if (defval is not None) or assigned:
                    break
                parameters[i][1] = True

        # 4. Match the **kwargs, if any.
        if node.kwargs is not None:
            for i, [(name, defval), assigned] in enumerate(parameters):
                # Assume that *kwargs provides values for all remaining
                # unassigned named parameters.
                if name is not None:
                    parameters[i][1] = True
                else:
                    # **kwargs can't assign to tuples.
                    pass

        # Check that any parameters without a default have been assigned
        # values.
        for [(name, defval), assigned] in parameters:
            if (defval is None) and not assigned:
                if name is None:
                    display_name = '<tuple>'
                else:
                    display_name = repr(name)
                self.add_message('no-value-for-parameter', node=node, args=(display_name, callable_name))

        for name in kwparams:
            defval, assigned = kwparams[name]
            if defval is None and not assigned:
                self.add_message('missing-kwoa', node=node, args=(name, callable_name))


def register(linter):
    """required method to auto register this checker """
    linter.register_checker(TypeChecker(linter))
