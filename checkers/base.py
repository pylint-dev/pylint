# Copyright (c) 2003-2013 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# Copyright (c) 2009-2010 Arista Networks, Inc.
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
"""basic checker for Python code"""

import sys
import astroid
from logilab.common.ureports import Table
from astroid import are_exclusive, InferenceError
import astroid.bases

from pylint.interfaces import IAstroidChecker
from pylint.utils import EmptyReport
from pylint.reporters import diff_string
from pylint.checkers import BaseChecker
from pylint.checkers.utils import (
    check_messages,
    clobber_in_except,
    is_builtin_object,
    is_inside_except,
    overrides_a_method,
    safe_infer,
    get_argument_from_call,
    NoSuchArgumentError,
    )


import re

# regex for class/function/variable/constant name
CLASS_NAME_RGX = re.compile('[A-Z_][a-zA-Z0-9]+$')
MOD_NAME_RGX = re.compile('(([a-z_][a-z0-9_]*)|([A-Z][a-zA-Z0-9]+))$')
CONST_NAME_RGX = re.compile('(([A-Z_][A-Z0-9_]*)|(__.*__))$')
COMP_VAR_RGX = re.compile('[A-Za-z_][A-Za-z0-9_]*$')
DEFAULT_NAME_RGX = re.compile('[a-z_][a-z0-9_]{2,30}$')
CLASS_ATTRIBUTE_RGX = re.compile(r'([A-Za-z_][A-Za-z0-9_]{2,30}|(__.*__))$')
# do not require a doc string on system methods
NO_REQUIRED_DOC_RGX = re.compile('__.*__')
REVERSED_METHODS = (('__getitem__', '__len__'),
                    ('__reversed__', ))

PY33 = sys.version_info >= (3, 3)
BAD_FUNCTIONS = ['map', 'filter', 'apply']
if sys.version_info < (3, 0):
    BAD_FUNCTIONS.append('input')
    BAD_FUNCTIONS.append('file')

# Name categories that are always consistent with all naming conventions.
EXEMPT_NAME_CATEGORIES = set(('exempt', 'ignore'))

del re

def in_loop(node):
    """return True if the node is inside a kind of for loop"""
    parent = node.parent
    while parent is not None:
        if isinstance(parent, (astroid.For, astroid.ListComp, astroid.SetComp,
                               astroid.DictComp, astroid.GenExpr)):
            return True
        parent = parent.parent
    return False

def in_nested_list(nested_list, obj):
    """return true if the object is an element of <nested_list> or of a nested
    list
    """
    for elmt in nested_list:
        if isinstance(elmt, (list, tuple)):
            if in_nested_list(elmt, obj):
                return True
        elif elmt == obj:
            return True
    return False

def _loop_exits_early(loop):
    """Returns true if a loop has a break statement in its body."""
    loop_nodes = (astroid.For, astroid.While)
    # Loop over body explicitly to avoid matching break statements
    # in orelse.
    for child in loop.body:
        if isinstance(child, loop_nodes):
            # break statement may be in orelse of child loop.
            for orelse in (child.orelse or ()):
                for _ in orelse.nodes_of_class(astroid.Break, skip_klass=loop_nodes):
                    return True
            continue
        for _ in child.nodes_of_class(astroid.Break, skip_klass=loop_nodes):
            return True
    return False

if sys.version_info < (3, 0):
    PROPERTY_CLASSES = set(('__builtin__.property', 'abc.abstractproperty'))
else:
    PROPERTY_CLASSES = set(('builtins.property', 'abc.abstractproperty'))
ABC_METHODS = set(('abc.abstractproperty', 'abc.abstractmethod',
                   'abc.abstractclassmethod', 'abc.abstractstaticmethod'))

def _determine_function_name_type(node):
    """Determine the name type whose regex the a function's name should match.

    :param node: A function node.
    :returns: One of ('function', 'method', 'attr')
    """
    if not node.is_method():
        return 'function'
    if node.decorators:
        decorators = node.decorators.nodes
    else:
        decorators = []
    for decorator in decorators:
        # If the function is a property (decorated with @property
        # or @abc.abstractproperty), the name type is 'attr'.
        if (isinstance(decorator, astroid.Name) or
            (isinstance(decorator, astroid.Getattr) and
             decorator.attrname == 'abstractproperty')):
            infered = safe_infer(decorator)
            if infered and infered.qname() in PROPERTY_CLASSES:
                return 'attr'
        # If the function is decorated using the prop_method.{setter,getter}
        # form, treat it like an attribute as well.
        elif (isinstance(decorator, astroid.Getattr) and
              decorator.attrname in ('setter', 'deleter')):
            return 'attr'
    return 'method'

def decorated_with_abc(func):
    """ Determine if the `func` node is decorated
    with `abc` decorators (abstractmethod et co.)
    """
    if func.decorators:
        for node in func.decorators.nodes:
            try:
                infered = node.infer().next()
            except InferenceError:
                continue
            if infered and infered.qname() in ABC_METHODS:
                return True

def has_abstract_methods(node):
    """ Determine if the given `node` has
    abstract methods, defined with `abc` module.
    """
    return any(decorated_with_abc(meth)
               for meth in node.mymethods())

def report_by_type_stats(sect, stats, old_stats):
    """make a report of

    * percentage of different types documented
    * percentage of different types with a bad name
    """
    # percentage of different types documented and/or with a bad name
    nice_stats = {}
    for node_type in ('module', 'class', 'method', 'function'):
        try:
            total = stats[node_type]
        except KeyError:
            raise EmptyReport()
        nice_stats[node_type] = {}
        if total != 0:
            try:
                documented = total - stats['undocumented_'+node_type]
                percent = (documented * 100.) / total
                nice_stats[node_type]['percent_documented'] = '%.2f' % percent
            except KeyError:
                nice_stats[node_type]['percent_documented'] = 'NC'
            try:
                percent = (stats['badname_'+node_type] * 100.) / total
                nice_stats[node_type]['percent_badname'] = '%.2f' % percent
            except KeyError:
                nice_stats[node_type]['percent_badname'] = 'NC'
    lines = ('type', 'number', 'old number', 'difference',
             '%documented', '%badname')
    for node_type in ('module', 'class', 'method', 'function'):
        new = stats[node_type]
        old = old_stats.get(node_type, None)
        if old is not None:
            diff_str = diff_string(old, new)
        else:
            old, diff_str = 'NC', 'NC'
        lines += (node_type, str(new), str(old), diff_str,
                  nice_stats[node_type].get('percent_documented', '0'),
                  nice_stats[node_type].get('percent_badname', '0'))
    sect.append(Table(children=lines, cols=6, rheaders=1))

def redefined_by_decorator(node):
    """return True if the object is a method redefined via decorator.

    For example:
        @property
        def x(self): return self._x
        @x.setter
        def x(self, value): self._x = value
    """
    if node.decorators:
        for decorator in node.decorators.nodes:
            if (isinstance(decorator, astroid.Getattr) and
                getattr(decorator.expr, 'name', None) == node.name):
                return True
    return False

class _BasicChecker(BaseChecker):
    __implements__ = IAstroidChecker
    name = 'basic'

class BasicErrorChecker(_BasicChecker):
    msgs = {
    'E0100': ('__init__ method is a generator',
              'init-is-generator',
              'Used when the special class method __init__ is turned into a '
              'generator by a yield in its body.'),
    'E0101': ('Explicit return in __init__',
              'return-in-init',
              'Used when the special class method __init__ has an explicit \
              return value.'),
    'E0102': ('%s already defined line %s',
              'function-redefined',
              'Used when a function / class / method is redefined.'),
    'E0103': ('%r not properly in loop',
              'not-in-loop',
              'Used when break or continue keywords are used outside a loop.'),

    'E0104': ('Return outside function',
              'return-outside-function',
              'Used when a "return" statement is found outside a function or '
              'method.'),
    'E0105': ('Yield outside function',
              'yield-outside-function',
              'Used when a "yield" statement is found outside a function or '
              'method.'),
    'E0106': ('Return with argument inside generator',
              'return-arg-in-generator',
              'Used when a "return" statement with an argument is found '
              'outside in a generator function or method (e.g. with some '
              '"yield" statements).',
              {'maxversion': (3, 3)}),
    'E0107': ("Use of the non-existent %s operator",
              'nonexistent-operator',
              "Used when you attempt to use the C-style pre-increment or"
              "pre-decrement operator -- and ++, which doesn't exist in Python."),
    'E0108': ('Duplicate argument name %s in function definition',
              'duplicate-argument-name',
              'Duplicate argument names in function definitions are syntax'
              ' errors.'),
    'E0110': ('Abstract class with abstract methods instantiated',
              'abstract-class-instantiated',
              'Used when an abstract class with `abc.ABCMeta` as metaclass '
              'has abstract methods and is instantiated.',
              {'minversion': (3, 0)}),
    'W0120': ('Else clause on loop without a break statement',
              'useless-else-on-loop',
              'Loops should only have an else clause if they can exit early '
              'with a break statement, otherwise the statements under else '
              'should be on the same scope as the loop itself.'),
    }

    def __init__(self, linter):
        _BasicChecker.__init__(self, linter)

    @check_messages('function-redefined')
    def visit_class(self, node):
        self._check_redefinition('class', node)

    @check_messages('init-is-generator', 'return-in-init',
                    'function-redefined', 'return-arg-in-generator',
                    'duplicate-argument-name')
    def visit_function(self, node):
        if not redefined_by_decorator(node):
            self._check_redefinition(node.is_method() and 'method' or 'function', node)
        # checks for max returns, branch, return in __init__
        returns = node.nodes_of_class(astroid.Return,
                                      skip_klass=(astroid.Function, astroid.Class))
        if node.is_method() and node.name == '__init__':
            if node.is_generator():
                self.add_message('init-is-generator', node=node)
            else:
                values = [r.value for r in returns]
                # Are we returning anything but None from constructors
                if  [v for v in values if
                     not (v is None or
                          (isinstance(v, astroid.Const) and v.value is None) or
                          (isinstance(v, astroid.Name)  and v.name == 'None')
                          )]:
                    self.add_message('return-in-init', node=node)
        elif node.is_generator():
            # make sure we don't mix non-None returns and yields
            if not PY33:
                for retnode in returns:
                    if isinstance(retnode.value, astroid.Const) and \
                           retnode.value.value is not None:
                        self.add_message('return-arg-in-generator', node=node,
                                         line=retnode.fromlineno)
        # Check for duplicate names
        args = set()
        for name in node.argnames():
            if name in args:
                self.add_message('duplicate-argument-name', node=node, args=(name,))
            else:
                args.add(name)


    @check_messages('return-outside-function')
    def visit_return(self, node):
        if not isinstance(node.frame(), astroid.Function):
            self.add_message('return-outside-function', node=node)

    @check_messages('yield-outside-function')
    def visit_yield(self, node):
        if not isinstance(node.frame(), (astroid.Function, astroid.Lambda)):
            self.add_message('yield-outside-function', node=node)

    @check_messages('not-in-loop')
    def visit_continue(self, node):
        self._check_in_loop(node, 'continue')

    @check_messages('not-in-loop')
    def visit_break(self, node):
        self._check_in_loop(node, 'break')

    @check_messages('useless-else-on-loop')
    def visit_for(self, node):
        self._check_else_on_loop(node)

    @check_messages('useless-else-on-loop')
    def visit_while(self, node):
        self._check_else_on_loop(node)

    @check_messages('nonexistent-operator')
    def visit_unaryop(self, node):
        """check use of the non-existent ++ and -- operator operator"""
        if ((node.op in '+-') and
            isinstance(node.operand, astroid.UnaryOp) and
            (node.operand.op == node.op)):
            self.add_message('nonexistent-operator', node=node, args=node.op*2)

    @check_messages('abstract-class-instantiated')
    def visit_callfunc(self, node):
        """ Check instantiating abstract class with
        abc.ABCMeta as metaclass. 
        """
        try:
            infered = node.func.infer().next()
        except astroid.InferenceError:
            return
        if not isinstance(infered, astroid.Class):
            return
        # __init__ was called
        metaclass = infered.metaclass()
        if metaclass is None:
            # Python 3.4 has `abc.ABC`, which won't be detected
            # by ClassNode.metaclass()
            for ancestor in infered.ancestors():
                if (ancestor.qname() == 'abc.ABC' and
                    has_abstract_methods(infered)):

                    self.add_message('abstract-class-instantiated', node=node)
                    break
            return
        if (metaclass.qname() == 'abc.ABCMeta' and
            has_abstract_methods(infered)):

            self.add_message('abstract-class-instantiated', node=node)
   
    def _check_else_on_loop(self, node):
        """Check that any loop with an else clause has a break statement."""
        if node.orelse and not _loop_exits_early(node):
            self.add_message('useless-else-on-loop', node=node,
                             # This is not optimal, but the line previous
                             # to the first statement in the else clause
                             # will usually be the one that contains the else:.
                             line=node.orelse[0].lineno - 1)

    def _check_in_loop(self, node, node_name):
        """check that a node is inside a for or while loop"""
        _node = node.parent
        while _node:
            if isinstance(_node, (astroid.For, astroid.While)):
                break
            _node = _node.parent
        else:
            self.add_message('not-in-loop', node=node, args=node_name)

    def _check_redefinition(self, redeftype, node):
        """check for redefinition of a function / method / class name"""
        defined_self = node.parent.frame()[node.name]
        if defined_self is not node and not are_exclusive(node, defined_self):
            self.add_message('function-redefined', node=node,
                             args=(redeftype, defined_self.fromlineno))



class BasicChecker(_BasicChecker):
    """checks for :
    * doc strings
    * number of arguments, local variables, branches, returns and statements in
functions, methods
    * required module attributes
    * dangerous default values as arguments
    * redefinition of function / method / class
    * uses of the global statement
    """

    __implements__ = IAstroidChecker

    name = 'basic'
    msgs = {
    'W0101': ('Unreachable code',
              'unreachable',
              'Used when there is some code behind a "return" or "raise" \
              statement, which will never be accessed.'),
    'W0102': ('Dangerous default value %s as argument',
              'dangerous-default-value',
              'Used when a mutable value as list or dictionary is detected in \
              a default value for an argument.'),
    'W0104': ('Statement seems to have no effect',
              'pointless-statement',
              'Used when a statement doesn\'t have (or at least seems to) \
              any effect.'),
    'W0105': ('String statement has no effect',
              'pointless-string-statement',
              'Used when a string is used as a statement (which of course \
              has no effect). This is a particular case of W0104 with its \
              own message so you can easily disable it if you\'re using \
              those strings as documentation, instead of comments.'),
    'W0106': ('Expression "%s" is assigned to nothing',
              'expression-not-assigned',
              'Used when an expression that is not a function call is assigned\
              to nothing. Probably something else was intended.'),
    'W0108': ('Lambda may not be necessary',
              'unnecessary-lambda',
              'Used when the body of a lambda expression is a function call \
              on the same argument list as the lambda itself; such lambda \
              expressions are in all but a few cases replaceable with the \
              function being called in the body of the lambda.'),
    'W0109': ("Duplicate key %r in dictionary",
              'duplicate-key',
              "Used when a dictionary expression binds the same key multiple \
              times."),
    'W0122': ('Use of exec',
              'exec-used',
              'Used when you use the "exec" statement (function for Python 3), to discourage its \
              usage. That doesn\'t mean you can not use it !'),
    'W0123': ('Use of eval',
              'eval-used',
              'Used when you use the "eval" function, to discourage its '
              'usage. Consider using `ast.literal_eval` for safely evaluating '
              'strings containing Python expressions '
              'from untrusted sources. '),
    'W0141': ('Used builtin function %r',
              'bad-builtin',
              'Used when a black listed builtin function is used (see the '
              'bad-function option). Usual black listed functions are the ones '
              'like map, or filter , where Python offers now some cleaner '
              'alternative like list comprehension.'),
    'W0142': ('Used * or ** magic',
              'star-args',
              'Used when a function or method is called using `*args` or '
              '`**kwargs` to dispatch arguments. This doesn\'t improve '
              'readability and should be used with care.'),
    'W0150': ("%s statement in finally block may swallow exception",
              'lost-exception',
              "Used when a break or a return statement is found inside the \
              finally clause of a try...finally block: the exceptions raised \
              in the try clause will be silently swallowed instead of being \
              re-raised."),
    'W0199': ('Assert called on a 2-uple. Did you mean \'assert x,y\'?',
              'assert-on-tuple',
              'A call of assert on a tuple will always evaluate to true if '
              'the tuple is not empty, and will always evaluate to false if '
              'it is.'),
    'W0121': ('Use raise ErrorClass(args) instead of raise ErrorClass, args.',
              'old-raise-syntax',
              "Used when the alternate raise syntax 'raise foo, bar' is used "
              "instead of 'raise foo(bar)'.",
              {'maxversion': (3, 0)}),

    'C0121': ('Missing required attribute "%s"', # W0103
              'missing-module-attribute',
              'Used when an attribute required for modules is missing.'),

    'E0109': ('Missing argument to reversed()',
              'missing-reversed-argument',
              'Used when reversed() builtin didn\'t receive an argument.'),
    'E0111': ('The first reversed() argument is not a sequence',
              'bad-reversed-sequence',
              'Used when the first argument to reversed() builtin '
              'isn\'t a sequence (does not implement __reversed__, '
              'nor __getitem__ and __len__'),

    }

    options = (('required-attributes',
                {'default' : (), 'type' : 'csv',
                 'metavar' : '<attributes>',
                 'help' : 'Required attributes for module, separated by a '
                          'comma'}
                ),
               ('bad-functions',
                {'default' : BAD_FUNCTIONS,
                 'type' :'csv', 'metavar' : '<builtin function names>',
                 'help' : 'List of builtins function names that should not be '
                          'used, separated by a comma'}
                ),
               )
    reports = (('RP0101', 'Statistics by type', report_by_type_stats),)

    def __init__(self, linter):
        _BasicChecker.__init__(self, linter)
        self.stats = None
        self._tryfinallys = None

    def open(self):
        """initialize visit variables and statistics
        """
        self._tryfinallys = []
        self.stats = self.linter.add_stats(module=0, function=0,
                                           method=0, class_=0)
    @check_messages('missing-module-attribute')
    def visit_module(self, node):
        """check module name, docstring and required arguments
        """
        self.stats['module'] += 1
        for attr in self.config.required_attributes:
            if attr not in node:
                self.add_message('missing-module-attribute', node=node, args=attr)

    def visit_class(self, node):
        """check module name, docstring and redefinition
        increment branch counter
        """
        self.stats['class'] += 1

    @check_messages('pointless-statement', 'pointless-string-statement',
                    'expression-not-assigned')
    def visit_discard(self, node):
        """check for various kind of statements without effect"""
        expr = node.value
        if isinstance(expr, astroid.Const) and isinstance(expr.value,
                                                        basestring):
            # treat string statement in a separated message
            self.add_message('pointless-string-statement', node=node)
            return
        # ignore if this is :
        # * a direct function call
        # * the unique child of a try/except body
        # * a yield (which are wrapped by a discard node in _ast XXX)
        # warn W0106 if we have any underlying function call (we can't predict
        # side effects), else pointless-statement
        if (isinstance(expr, (astroid.Yield, astroid.CallFunc)) or
            (isinstance(node.parent, astroid.TryExcept) and
             node.parent.body == [node])):
            return
        if any(expr.nodes_of_class(astroid.CallFunc)):
            self.add_message('expression-not-assigned', node=node, args=expr.as_string())
        else:
            self.add_message('pointless-statement', node=node)

    @check_messages('unnecessary-lambda')
    def visit_lambda(self, node):
        """check whether or not the lambda is suspicious
        """
        # if the body of the lambda is a call expression with the same
        # argument list as the lambda itself, then the lambda is
        # possibly unnecessary and at least suspicious.
        if node.args.defaults:
            # If the arguments of the lambda include defaults, then a
            # judgment cannot be made because there is no way to check
            # that the defaults defined by the lambda are the same as
            # the defaults defined by the function called in the body
            # of the lambda.
            return
        call = node.body
        if not isinstance(call, astroid.CallFunc):
            # The body of the lambda must be a function call expression
            # for the lambda to be unnecessary.
            return
        # XXX are lambda still different with astroid >= 0.18 ?
        # *args and **kwargs need to be treated specially, since they
        # are structured differently between the lambda and the function
        # call (in the lambda they appear in the args.args list and are
        # indicated as * and ** by two bits in the lambda's flags, but
        # in the function call they are omitted from the args list and
        # are indicated by separate attributes on the function call node).
        ordinary_args = list(node.args.args)
        if node.args.kwarg:
            if (not call.kwargs
                or not isinstance(call.kwargs, astroid.Name)
                or node.args.kwarg != call.kwargs.name):
                return
        elif call.kwargs:
            return
        if node.args.vararg:
            if (not call.starargs
                or not isinstance(call.starargs, astroid.Name)
                or node.args.vararg != call.starargs.name):
                return
        elif call.starargs:
            return
        # The "ordinary" arguments must be in a correspondence such that:
        # ordinary_args[i].name == call.args[i].name.
        if len(ordinary_args) != len(call.args):
            return
        for i in xrange(len(ordinary_args)):
            if not isinstance(call.args[i], astroid.Name):
                return
            if node.args.args[i].name != call.args[i].name:
                return
        self.add_message('unnecessary-lambda', line=node.fromlineno, node=node)

    @check_messages('dangerous-default-value')
    def visit_function(self, node):
        """check function name, docstring, arguments, redefinition,
        variable names, max locals
        """
        self.stats[node.is_method() and 'method' or 'function'] += 1
        # check for dangerous default values as arguments
        for default in node.args.defaults:
            try:
                value = default.infer().next()
            except astroid.InferenceError:
                continue
            builtins = astroid.bases.BUILTINS
            if (isinstance(value, astroid.Instance) and
                value.qname() in ['.'.join([builtins, x]) for x in ('set', 'dict', 'list')]):
                if value is default:
                    msg = default.as_string()
                elif type(value) is astroid.Instance:
                    msg = '%s (%s)' % (default.as_string(), value.qname())
                else:
                    msg = '%s (%s)' % (default.as_string(), value.as_string())
                self.add_message('dangerous-default-value', node=node, args=(msg,))

    @check_messages('unreachable', 'lost-exception')
    def visit_return(self, node):
        """1 - check is the node has a right sibling (if so, that's some
        unreachable code)
        2 - check is the node is inside the finally clause of a try...finally
        block
        """
        self._check_unreachable(node)
        # Is it inside final body of a try...finally bloc ?
        self._check_not_in_finally(node, 'return', (astroid.Function,))

    @check_messages('unreachable')
    def visit_continue(self, node):
        """check is the node has a right sibling (if so, that's some unreachable
        code)
        """
        self._check_unreachable(node)

    @check_messages('unreachable', 'lost-exception')
    def visit_break(self, node):
        """1 - check is the node has a right sibling (if so, that's some
        unreachable code)
        2 - check is the node is inside the finally clause of a try...finally
        block
        """
        # 1 - Is it right sibling ?
        self._check_unreachable(node)
        # 2 - Is it inside final body of a try...finally bloc ?
        self._check_not_in_finally(node, 'break', (astroid.For, astroid.While,))

    @check_messages('unreachable', 'old-raise-syntax')
    def visit_raise(self, node):
        """check if the node has a right sibling (if so, that's some unreachable
        code)
        """
        self._check_unreachable(node)
        if sys.version_info >= (3, 0):
            return
        if node.exc is not None and node.inst is not None and node.tback is None:
            self.add_message('old-raise-syntax', node=node)

    @check_messages('exec-used')
    def visit_exec(self, node):
        """just print a warning on exec statements"""
        self.add_message('exec-used', node=node)

    @check_messages('bad-builtin', 'star-args', 'eval-used', 
                    'exec-used', 'missing-reversed-argument', 
                    'bad-reversed-sequence')
    def visit_callfunc(self, node):
        """visit a CallFunc node -> check if this is not a blacklisted builtin
        call and check for * or ** use
        """
        if isinstance(node.func, astroid.Name):
            name = node.func.name
            # ignore the name if it's not a builtin (i.e. not defined in the
            # locals nor globals scope)
            if not (name in node.frame() or
                    name in node.root()):
                if name == 'exec':
                    self.add_message('exec-used', node=node)
                elif name == 'reversed':
                    self._check_reversed(node)
                elif name == 'eval':
                    self.add_message('eval-used', node=node)
                if name in self.config.bad_functions:
                    self.add_message('bad-builtin', node=node, args=name)
        if node.starargs or node.kwargs:
            scope = node.scope()
            if isinstance(scope, astroid.Function):
                toprocess = [(n, vn) for (n, vn) in ((node.starargs, scope.args.vararg),
                                                     (node.kwargs, scope.args.kwarg)) if n]
                if toprocess:
                    for cfnode, fargname in toprocess[:]:
                        if getattr(cfnode, 'name', None) == fargname:
                            toprocess.remove((cfnode, fargname))
                    if not toprocess:
                        return # star-args can be skipped
            self.add_message('star-args', node=node.func)

    @check_messages('assert-on-tuple')
    def visit_assert(self, node):
        """check the use of an assert statement on a tuple."""
        if node.fail is None and isinstance(node.test, astroid.Tuple) and \
           len(node.test.elts) == 2:
            self.add_message('assert-on-tuple', node=node)

    @check_messages('duplicate-key')
    def visit_dict(self, node):
        """check duplicate key in dictionary"""
        keys = set()
        for k, _ in node.items:
            if isinstance(k, astroid.Const):
                key = k.value
                if key in keys:
                    self.add_message('duplicate-key', node=node, args=key)
                keys.add(key)

    def visit_tryfinally(self, node):
        """update try...finally flag"""
        self._tryfinallys.append(node)

    def leave_tryfinally(self, node):
        """update try...finally flag"""
        self._tryfinallys.pop()

    def _check_unreachable(self, node):
        """check unreachable code"""
        unreach_stmt = node.next_sibling()
        if unreach_stmt is not None:
            self.add_message('unreachable', node=unreach_stmt)

    def _check_not_in_finally(self, node, node_name, breaker_classes=()):
        """check that a node is not inside a finally clause of a
        try...finally statement.
        If we found before a try...finally bloc a parent which its type is
        in breaker_classes, we skip the whole check."""
        # if self._tryfinallys is empty, we're not a in try...finally bloc
        if not self._tryfinallys:
            return
        # the node could be a grand-grand...-children of the try...finally
        _parent = node.parent
        _node = node
        while _parent and not isinstance(_parent, breaker_classes):
            if hasattr(_parent, 'finalbody') and _node in _parent.finalbody:
                self.add_message('lost-exception', node=node, args=node_name)
                return
            _node = _parent
            _parent = _node.parent
    
    def _check_reversed(self, node):
        """ check that the argument to `reversed` is a sequence """
        try:
            argument = safe_infer(get_argument_from_call(node, position=0))
        except NoSuchArgumentError:
            self.add_message('missing-reversed-argument', node=node)
        else:
            if argument is astroid.YES:
                return
            if argument is None:
                # nothing was infered
                # try to see if we have iter()
                if isinstance(node.args[0], astroid.CallFunc):
                    try:
                        func = node.args[0].func.infer().next()
                    except InferenceError:
                        return
                    if (getattr(func, 'name', None) == 'iter' and
                        is_builtin_object(func)):
                        self.add_message('bad-reversed-sequence', node=node)
                return

            if isinstance(argument, astroid.Instance):
                if (argument._proxied.name == 'dict' and 
                    is_builtin_object(argument._proxied)):
                     self.add_message('bad-reversed-sequence', node=node)
                     return
                elif any(ancestor.name == 'dict' and is_builtin_object(ancestor)
                       for ancestor in argument._proxied.ancestors()):
                    # mappings aren't accepted by reversed()
                    self.add_message('bad-reversed-sequence', node=node)
                    return

                for methods in REVERSED_METHODS:
                    for meth in methods:
                        try:
                            argument.getattr(meth)
                        except astroid.NotFoundError:
                            break
                    else:
                        break
                else:             
                    # check if it is a .deque. It doesn't seem that
                    # we can retrieve special methods 
                    # from C implemented constructs    
                    if argument._proxied.qname().endswith(".deque"):
                        return
                    self.add_message('bad-reversed-sequence', node=node)
            elif not isinstance(argument, (astroid.List, astroid.Tuple)):
                # everything else is not a proper sequence for reversed()
                self.add_message('bad-reversed-sequence', node=node)

_NAME_TYPES = {
    'module': (MOD_NAME_RGX, 'module'),
    'const': (CONST_NAME_RGX, 'constant'),
    'class': (CLASS_NAME_RGX, 'class'),
    'function': (DEFAULT_NAME_RGX, 'function'),
    'method': (DEFAULT_NAME_RGX, 'method'),
    'attr': (DEFAULT_NAME_RGX, 'attribute'),
    'argument': (DEFAULT_NAME_RGX, 'argument'),
    'variable': (DEFAULT_NAME_RGX, 'variable'),
    'class_attribute': (CLASS_ATTRIBUTE_RGX, 'class attribute'),
    'inlinevar': (COMP_VAR_RGX, 'inline iteration'),
}

def _create_naming_options():
    name_options = []
    for name_type, (rgx, human_readable_name) in _NAME_TYPES.iteritems():
        name_type = name_type.replace('_', '-')
        name_options.append((
            '%s-rgx' % (name_type,), 
            {'default': rgx, 'type': 'regexp', 'metavar': '<regexp>',
             'help': 'Regular expression matching correct %s names' % (human_readable_name,)}))
        name_options.append((
            '%s-name-hint' % (name_type,), 
            {'default': rgx.pattern, 'type': 'string', 'metavar': '<string>',
             'help': 'Naming hint for %s names' % (human_readable_name,)}))

    return tuple(name_options) 

class NameChecker(_BasicChecker):
    msgs = {
    'C0102': ('Black listed name "%s"',
              'blacklisted-name',
              'Used when the name is listed in the black list (unauthorized \
              names).'),
    'C0103': ('Invalid %s name "%s"%s',
              'invalid-name',
              'Used when the name doesn\'t match the regular expression \
              associated to its type (constant, variable, class...).'),
    }

    options = (# XXX use set
               ('good-names',
                {'default' : ('i', 'j', 'k', 'ex', 'Run', '_'),
                 'type' :'csv', 'metavar' : '<names>',
                 'help' : 'Good variable names which should always be accepted,'
                          ' separated by a comma'}
                ),
               ('bad-names',
                {'default' : ('foo', 'bar', 'baz', 'toto', 'tutu', 'tata'),
                 'type' :'csv', 'metavar' : '<names>',
                 'help' : 'Bad variable names which should always be refused, '
                          'separated by a comma'}
                ),
               ('name-group',
                {'default' : (),
                 'type' :'csv', 'metavar' : '<name1:name2>',
                 'help' : ('Colon-delimited sets of names that determine each'
                           ' other\'s naming style when the name regexes'
                           ' allow several styles.')}
                ),
               ('include-naming-hint',
                {'default': False, 'type' : 'yn', 'metavar' : '<y_or_n>',
                 'help': 'Include a hint for the correct naming format with invalid-name'}
                ),
               ) + _create_naming_options()


    def __init__(self, linter):
        _BasicChecker.__init__(self, linter)
        self._name_category = {}
        self._name_group = {}

    def open(self):
        self.stats = self.linter.add_stats(badname_module=0,
                                           badname_class=0, badname_function=0,
                                           badname_method=0, badname_attr=0,
                                           badname_const=0,
                                           badname_variable=0,
                                           badname_inlinevar=0,
                                           badname_argument=0,
                                           badname_class_attribute=0)
        for group in self.config.name_group:
            for name_type in group.split(':'):
                self._name_group[name_type] = 'group_%s' % (group,)

    @check_messages('blacklisted-name', 'invalid-name')
    def visit_module(self, node):
        self._check_name('module', node.name.split('.')[-1], node)

    @check_messages('blacklisted-name', 'invalid-name')
    def visit_class(self, node):
        self._check_name('class', node.name, node)
        for attr, anodes in node.instance_attrs.iteritems():
            if not list(node.instance_attr_ancestors(attr)):
                self._check_name('attr', attr, anodes[0])

    @check_messages('blacklisted-name', 'invalid-name')
    def visit_function(self, node):
        # Do not emit any warnings if the method is just an implementation
        # of a base class method.
        if node.is_method() and overrides_a_method(node.parent.frame(), node.name):
            return
        self._check_name(_determine_function_name_type(node),
                         node.name, node)
        # Check argument names
        args = node.args.args
        if args is not None:
            self._recursive_check_names(args, node)

    @check_messages('blacklisted-name', 'invalid-name')
    def visit_global(self, node):
        for name in node.names:
            self._check_name('const', name, node)

    @check_messages('blacklisted-name', 'invalid-name')
    def visit_assname(self, node):
        """check module level assigned names"""
        frame = node.frame()
        ass_type = node.ass_type()
        if isinstance(ass_type, astroid.Comprehension):
            self._check_name('inlinevar', node.name, node)
        elif isinstance(frame, astroid.Module):
            if isinstance(ass_type, astroid.Assign) and not in_loop(ass_type):
                if isinstance(safe_infer(ass_type.value), astroid.Class):
                    self._check_name('class', node.name, node)
                else:
                    self._check_name('const', node.name, node)
            elif isinstance(ass_type, astroid.ExceptHandler):
                self._check_name('variable', node.name, node)
        elif isinstance(frame, astroid.Function):
            # global introduced variable aren't in the function locals
            if node.name in frame and node.name not in frame.argnames():
                self._check_name('variable', node.name, node)
        elif isinstance(frame, astroid.Class):
            if not list(frame.local_attr_ancestors(node.name)):
                self._check_name('class_attribute', node.name, node)

    def _recursive_check_names(self, args, node):
        """check names in a possibly recursive list <arg>"""
        for arg in args:
            if isinstance(arg, astroid.AssName):
                self._check_name('argument', arg.name, node)
            else:
                self._recursive_check_names(arg.elts, node)

    def _find_name_group(self, node_type):
        return self._name_group.get(node_type, node_type)

    def _is_multi_naming_match(self, match):
        return (match is not None and
                match.lastgroup is not None and
                match.lastgroup not in EXEMPT_NAME_CATEGORIES)

    def _check_name(self, node_type, name, node):
        """check for a name using the type's regexp"""
        if is_inside_except(node):
            clobbering, _ = clobber_in_except(node)
            if clobbering:
                return
        if name in self.config.good_names:
            return
        if name in self.config.bad_names:
            self.stats['badname_' + node_type] += 1
            self.add_message('blacklisted-name', node=node, args=name)
            return
        regexp = getattr(self.config, node_type + '_rgx')
        match = regexp.match(name)

        if self._is_multi_naming_match(match):
            name_group = self._find_name_group(node_type)
            if name_group not in self._name_category:
                self._name_category[name_group] = match.lastgroup
            elif self._name_category[name_group] != match.lastgroup:
                match = None

        if match is None:
            type_label = _NAME_TYPES[node_type][1]
            hint = ''
            if self.config.include_naming_hint:
                hint = ' (hint: %s)' % (getattr(self.config, node_type + '_name_hint'))
            self.add_message('invalid-name', node=node, args=(type_label, name, hint))
            self.stats['badname_' + node_type] += 1


class DocStringChecker(_BasicChecker):
    msgs = {
    'C0111': ('Missing %s docstring', # W0131
              'missing-docstring',
              'Used when a module, function, class or method has no docstring.\
              Some special methods like __init__ doesn\'t necessary require a \
              docstring.'),
    'C0112': ('Empty %s docstring', # W0132
              'empty-docstring',
              'Used when a module, function, class or method has an empty \
              docstring (it would be too easy ;).'),
    }
    options = (('no-docstring-rgx',
                {'default' : NO_REQUIRED_DOC_RGX,
                 'type' : 'regexp', 'metavar' : '<regexp>',
                 'help' : 'Regular expression which should only match '
                          'function or class names that do not require a '
                          'docstring.'}
                ),
               ('docstring-min-length',
                {'default' : -1,
                 'type' : 'int', 'metavar' : '<int>',
                 'help': ('Minimum line length for functions/classes that'
                          ' require docstrings, shorter ones are exempt.')}
                ),
               )


    def open(self):
        self.stats = self.linter.add_stats(undocumented_module=0,
                                           undocumented_function=0,
                                           undocumented_method=0,
                                           undocumented_class=0)
    @check_messages('missing-docstring', 'empty-docstring')
    def visit_module(self, node):
        self._check_docstring('module', node)

    @check_messages('missing-docstring', 'empty-docstring')
    def visit_class(self, node):
        if self.config.no_docstring_rgx.match(node.name) is None:
            self._check_docstring('class', node)
    @check_messages('missing-docstring', 'empty-docstring')
    def visit_function(self, node):
        if self.config.no_docstring_rgx.match(node.name) is None:
            ftype = node.is_method() and 'method' or 'function'
            if isinstance(node.parent.frame(), astroid.Class):
                overridden = False
                # check if node is from a method overridden by its ancestor
                for ancestor in node.parent.frame().ancestors():
                    if node.name in ancestor and \
                       isinstance(ancestor[node.name], astroid.Function):
                        overridden = True
                        break
                self._check_docstring(ftype, node,
                                      report_missing=not overridden)
            else:
                self._check_docstring(ftype, node)

    def _check_docstring(self, node_type, node, report_missing=True):
        """check the node has a non empty docstring"""
        docstring = node.doc
        if docstring is None:
            if not report_missing:
                return
            if node.body:
                lines = node.body[-1].lineno - node.body[0].lineno + 1
            else:
                lines = 0
            max_lines = self.config.docstring_min_length

            if node_type != 'module' and max_lines > -1 and lines < max_lines:
                return
            self.stats['undocumented_'+node_type] += 1
            self.add_message('missing-docstring', node=node, args=(node_type,))
        elif not docstring.strip():
            self.stats['undocumented_'+node_type] += 1
            self.add_message('empty-docstring', node=node, args=(node_type,))


class PassChecker(_BasicChecker):
    """check if the pass statement is really necessary"""
    msgs = {'W0107': ('Unnecessary pass statement',
                      'unnecessary-pass',
                      'Used when a "pass" statement that can be avoided is '
                      'encountered.'),
            }
    @check_messages('unnecessary-pass')
    def visit_pass(self, node):
        if len(node.parent.child_sequence(node)) > 1:
            self.add_message('unnecessary-pass', node=node)


class LambdaForComprehensionChecker(_BasicChecker):
    """check for using a lambda where a comprehension would do.

    See <http://www.artima.com/weblogs/viewpost.jsp?thread=98196>
    where GvR says comprehensions would be clearer.
    """

    msgs = {'W0110': ('map/filter on lambda could be replaced by comprehension',
                      'deprecated-lambda',
                      'Used when a lambda is the first argument to "map" or '
                      '"filter". It could be clearer as a list '
                      'comprehension or generator expression.',
                      {'maxversion': (3, 0)}),
            }

    @check_messages('deprecated-lambda')
    def visit_callfunc(self, node):
        """visit a CallFunc node, check if map or filter are called with a
        lambda
        """
        if not node.args:
            return
        if not isinstance(node.args[0], astroid.Lambda):
            return
        infered = safe_infer(node.func)
        if (is_builtin_object(infered)
            and infered.name in ['map', 'filter']):
            self.add_message('deprecated-lambda', node=node)


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(BasicErrorChecker(linter))
    linter.register_checker(BasicChecker(linter))
    linter.register_checker(NameChecker(linter))
    linter.register_checker(DocStringChecker(linter))
    linter.register_checker(PassChecker(linter))
    linter.register_checker(LambdaForComprehensionChecker(linter))
