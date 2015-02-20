# pylint: disable=W0611
#
# Copyright (c) 2003-2013 LOGILAB S.A. (Paris, FRANCE).
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
"""some functions that may be useful for various checkers
"""

import re
import sys
import string

import astroid
from astroid import scoped_nodes
from logilab.common.compat import builtins

BUILTINS_NAME = builtins.__name__
COMP_NODE_TYPES = astroid.ListComp, astroid.SetComp, astroid.DictComp, astroid.GenExpr
PY3K = sys.version_info[0] == 3

if not PY3K:
    EXCEPTIONS_MODULE = "exceptions"
else:
    EXCEPTIONS_MODULE = "builtins"
ABC_METHODS = set(('abc.abstractproperty', 'abc.abstractmethod',
                   'abc.abstractclassmethod', 'abc.abstractstaticmethod'))


class NoSuchArgumentError(Exception):
    pass

def is_inside_except(node):
    """Returns true if node is inside the name of an except handler."""
    current = node
    while current and not isinstance(current.parent, astroid.ExceptHandler):
        current = current.parent

    return current and current is current.parent.name


def get_all_elements(node):
    """Recursively returns all atoms in nested lists and tuples."""
    if isinstance(node, (astroid.Tuple, astroid.List)):
        for child in node.elts:
            for e in get_all_elements(child):
                yield e
    else:
        yield node


def clobber_in_except(node):
    """Checks if an assignment node in an except handler clobbers an existing
    variable.

    Returns (True, args for W0623) if assignment clobbers an existing variable,
    (False, None) otherwise.
    """
    if isinstance(node, astroid.AssAttr):
        return (True, (node.attrname, 'object %r' % (node.expr.as_string(),)))
    elif isinstance(node, astroid.AssName):
        name = node.name
        if is_builtin(name):
            return (True, (name, 'builtins'))
        else:
            stmts = node.lookup(name)[1]
            if (stmts and not isinstance(stmts[0].ass_type(),
                                         (astroid.Assign, astroid.AugAssign,
                                          astroid.ExceptHandler))):
                return (True, (name, 'outer scope (line %s)' % stmts[0].fromlineno))
    return (False, None)


def safe_infer(node):
    """return the inferred value for the given node.
    Return None if inference failed or if there is some ambiguity (more than
    one node has been inferred)
    """
    try:
        inferit = node.infer()
        value = next(inferit)
    except astroid.InferenceError:
        return
    try:
        next(inferit)
        return # None if there is ambiguity on the inferred node
    except astroid.InferenceError:
        return # there is some kind of ambiguity
    except StopIteration:
        return value

def is_super(node):
    """return True if the node is referencing the "super" builtin function
    """
    if getattr(node, 'name', None) == 'super' and \
           node.root().name == BUILTINS_NAME:
        return True
    return False

def is_error(node):
    """return true if the function does nothing but raising an exception"""
    for child_node in node.get_children():
        if isinstance(child_node, astroid.Raise):
            return True
        return False

def is_raising(body):
    """return true if the given statement node raise an exception"""
    for node in body:
        if isinstance(node, astroid.Raise):
            return True
    return False

def is_empty(body):
    """return true if the given node does nothing but 'pass'"""
    return len(body) == 1 and isinstance(body[0], astroid.Pass)

builtins = builtins.__dict__.copy()
SPECIAL_BUILTINS = ('__builtins__',) # '__path__', '__file__')

def is_builtin_object(node):
    """Returns True if the given node is an object from the __builtin__ module."""
    return node and node.root().name == BUILTINS_NAME

def is_builtin(name): # was is_native_builtin
    """return true if <name> could be considered as a builtin defined by python
    """
    if name in builtins:
        return True
    if name in SPECIAL_BUILTINS:
        return True
    return False

def is_defined_before(var_node):
    """return True if the variable node is defined by a parent node (list,
    set, dict, or generator comprehension, lambda) or in a previous sibling
    node on the same line (statement_defining ; statement_using)
    """
    varname = var_node.name
    _node = var_node.parent
    while _node:
        if isinstance(_node, COMP_NODE_TYPES):
            for ass_node in _node.nodes_of_class(astroid.AssName):
                if ass_node.name == varname:
                    return True
        elif isinstance(_node, astroid.For):
            for ass_node in _node.target.nodes_of_class(astroid.AssName):
                if ass_node.name == varname:
                    return True
        elif isinstance(_node, astroid.With):
            for expr, ids in _node.items:
                if expr.parent_of(var_node):
                    break
                if (ids and
                        isinstance(ids, astroid.AssName) and
                        ids.name == varname):
                    return True
        elif isinstance(_node, (astroid.Lambda, astroid.Function)):
            if _node.args.is_argument(varname):
                return True
            if getattr(_node, 'name', None) == varname:
                return True
            break
        elif isinstance(_node, astroid.ExceptHandler):
            if isinstance(_node.name, astroid.AssName):
                ass_node = _node.name
                if ass_node.name == varname:
                    return True
        _node = _node.parent
    # possibly multiple statements on the same line using semi colon separator
    stmt = var_node.statement()
    _node = stmt.previous_sibling()
    lineno = stmt.fromlineno
    while _node and _node.fromlineno == lineno:
        for ass_node in _node.nodes_of_class(astroid.AssName):
            if ass_node.name == varname:
                return True
        for imp_node in _node.nodes_of_class((astroid.From, astroid.Import)):
            if varname in [name[1] or name[0] for name in imp_node.names]:
                return True
        _node = _node.previous_sibling()
    return False

def is_func_default(node):
    """return true if the given Name node is used in function default argument's
    value
    """
    parent = node.scope()
    if isinstance(parent, astroid.Function):
        for default_node in parent.args.defaults:
            for default_name_node in default_node.nodes_of_class(astroid.Name):
                if default_name_node is node:
                    return True
    return False

def is_func_decorator(node):
    """return true if the name is used in function decorator"""
    parent = node.parent
    while parent is not None:
        if isinstance(parent, astroid.Decorators):
            return True
        if (parent.is_statement or
                isinstance(parent, astroid.Lambda) or
                isinstance(parent, (scoped_nodes.ComprehensionScope,
                                    scoped_nodes.ListComp))):
            break
        parent = parent.parent
    return False

def is_ancestor_name(frame, node):
    """return True if `frame` is a astroid.Class node with `node` in the
    subtree of its bases attribute
    """
    try:
        bases = frame.bases
    except AttributeError:
        return False
    for base in bases:
        if node in base.nodes_of_class(astroid.Name):
            return True
    return False

def assign_parent(node):
    """return the higher parent which is not an AssName, Tuple or List node
    """
    while node and isinstance(node, (astroid.AssName,
                                     astroid.Tuple,
                                     astroid.List)):
        node = node.parent
    return node

def overrides_an_abstract_method(class_node, name):
    """return True if pnode is a parent of node"""
    for ancestor in class_node.ancestors():
        if name in ancestor and isinstance(ancestor[name], astroid.Function) and \
               ancestor[name].is_abstract(pass_is_abstract=False):
            return True
    return False

def overrides_a_method(class_node, name):
    """return True if <name> is a method overridden from an ancestor"""
    for ancestor in class_node.ancestors():
        if name in ancestor and isinstance(ancestor[name], astroid.Function):
            return True
    return False

PYMETHODS = set(('__new__', '__init__', '__del__', '__hash__',
                 '__str__', '__repr__',
                 '__len__', '__iter__',
                 '__delete__', '__get__', '__set__',
                 '__getitem__', '__setitem__', '__delitem__', '__contains__',
                 '__getattribute__', '__getattr__', '__setattr__', '__delattr__',
                 '__call__',
                 '__enter__', '__exit__',
                 '__cmp__', '__ge__', '__gt__', '__le__', '__lt__', '__eq__',
                 '__nonzero__', '__neg__', '__invert__',
                 '__mul__', '__imul__', '__rmul__',
                 '__div__', '__idiv__', '__rdiv__',
                 '__add__', '__iadd__', '__radd__',
                 '__sub__', '__isub__', '__rsub__',
                 '__pow__', '__ipow__', '__rpow__',
                 '__mod__', '__imod__', '__rmod__',
                 '__and__', '__iand__', '__rand__',
                 '__or__', '__ior__', '__ror__',
                 '__xor__', '__ixor__', '__rxor__',
                 # XXX To be continued
                ))

def check_messages(*messages):
    """decorator to store messages that are handled by a checker method"""

    def store_messages(func):
        func.checks_msgs = messages
        return func
    return store_messages

class IncompleteFormatString(Exception):
    """A format string ended in the middle of a format specifier."""
    pass

class UnsupportedFormatCharacter(Exception):
    """A format character in a format string is not one of the supported
    format characters."""
    def __init__(self, index):
        Exception.__init__(self, index)
        self.index = index

def parse_format_string(format_string):
    """Parses a format string, returning a tuple of (keys, num_args), where keys
    is the set of mapping keys in the format string, and num_args is the number
    of arguments required by the format string.  Raises
    IncompleteFormatString or UnsupportedFormatCharacter if a
    parse error occurs."""
    keys = set()
    num_args = 0
    def next_char(i):
        i += 1
        if i == len(format_string):
            raise IncompleteFormatString
        return (i, format_string[i])
    i = 0
    while i < len(format_string):
        char = format_string[i]
        if char == '%':
            i, char = next_char(i)
            # Parse the mapping key (optional).
            key = None
            if char == '(':
                depth = 1
                i, char = next_char(i)
                key_start = i
                while depth != 0:
                    if char == '(':
                        depth += 1
                    elif char == ')':
                        depth -= 1
                    i, char = next_char(i)
                key_end = i - 1
                key = format_string[key_start:key_end]

            # Parse the conversion flags (optional).
            while char in '#0- +':
                i, char = next_char(i)
            # Parse the minimum field width (optional).
            if char == '*':
                num_args += 1
                i, char = next_char(i)
            else:
                while char in string.digits:
                    i, char = next_char(i)
            # Parse the precision (optional).
            if char == '.':
                i, char = next_char(i)
                if char == '*':
                    num_args += 1
                    i, char = next_char(i)
                else:
                    while char in string.digits:
                        i, char = next_char(i)
            # Parse the length modifier (optional).
            if char in 'hlL':
                i, char = next_char(i)
            # Parse the conversion type (mandatory).
            if PY3K:
                flags = 'diouxXeEfFgGcrs%a'
            else:
                flags = 'diouxXeEfFgGcrs%'
            if char not in flags:
                raise UnsupportedFormatCharacter(i)
            if key:
                keys.add(key)
            elif char != '%':
                num_args += 1
        i += 1
    return keys, num_args


def is_attr_protected(attrname):
    """return True if attribute name is protected (start with _ and some other
    details), False otherwise.
    """
    return attrname[0] == '_' and not attrname == '_' and not (
        attrname.startswith('__') and attrname.endswith('__'))

def node_frame_class(node):
    """return klass node for a method node (or a staticmethod or a
    classmethod), return null otherwise
    """
    klass = node.frame()

    while klass is not None and not isinstance(klass, astroid.Class):
        if klass.parent is None:
            klass = None
        else:
            klass = klass.parent.frame()

    return klass

def is_super_call(expr):
    """return True if expression node is a function call and if function name
    is super. Check before that you're in a method.
    """
    return (isinstance(expr, astroid.CallFunc) and
            isinstance(expr.func, astroid.Name) and
            expr.func.name == 'super')

def is_attr_private(attrname):
    """Check that attribute name is private (at least two leading underscores,
    at most one trailing underscore)
    """
    regex = re.compile('^_{2,}.*[^_]+_?$')
    return regex.match(attrname)

def get_argument_from_call(callfunc_node, position=None, keyword=None):
    """Returns the specified argument from a function call.

    :param callfunc_node: Node representing a function call to check.
    :param int position: position of the argument.
    :param str keyword: the keyword of the argument.

    :returns: The node representing the argument, None if the argument is not found.
    :raises ValueError: if both position and keyword are None.
    :raises NoSuchArgumentError: if no argument at the provided position or with
    the provided keyword.
    """
    if position is None and keyword is None:
        raise ValueError('Must specify at least one of: position or keyword.')
    try:
        if position is not None and not isinstance(callfunc_node.args[position], astroid.Keyword):
            return callfunc_node.args[position]
    except IndexError as error:
        raise NoSuchArgumentError(error)
    if keyword:
        for arg in callfunc_node.args:
            if isinstance(arg, astroid.Keyword) and arg.arg == keyword:
                return arg.value
    raise NoSuchArgumentError

def inherit_from_std_ex(node):
    """
    Return true if the given class node is subclass of
    exceptions.Exception.
    """
    if node.name in ('Exception', 'BaseException') \
            and node.root().name == EXCEPTIONS_MODULE:
        return True
    return any(inherit_from_std_ex(parent)
               for parent in node.ancestors(recurs=False))

def is_import_error(handler):
    """
    Check if the given exception handler catches
    ImportError.

    :param handler: A node, representing an ExceptHandler node.
    :returns: True if the handler catches ImportError, False otherwise.
    """
    names = None
    if isinstance(handler.type, astroid.Tuple):
        names = [name for name in handler.type.elts
                 if isinstance(name, astroid.Name)]
    elif isinstance(handler.type, astroid.Name):
        names = [handler.type]
    else:
        # Don't try to infer that.
        return
    for name in names:
        try:
            for infered in name.infer():
                if (isinstance(infered, astroid.Class) and
                        inherit_from_std_ex(infered) and
                        infered.name == 'ImportError'):
                    return True
        except astroid.InferenceError:
            continue

def has_known_bases(klass):
    """Returns true if all base classes of a class could be inferred."""
    try:
        return klass._all_bases_known
    except AttributeError:
        pass
    for base in klass.bases:
        result = safe_infer(base)
        # TODO: check for A->B->A->B pattern in class structure too?
        if (not isinstance(result, astroid.Class) or
                result is klass or
                not has_known_bases(result)):
            klass._all_bases_known = False
            return False
    klass._all_bases_known = True
    return True

def decorated_with_property(node):
    """ Detect if the given function node is decorated with a property. """
    if not node.decorators:
        return False
    for decorator in node.decorators.nodes:
        if not isinstance(decorator, astroid.Name):
            continue
        try:
            for infered in decorator.infer():
                if isinstance(infered, astroid.Class):
                    if (infered.root().name == BUILTINS_NAME and
                            infered.name == 'property'):
                        return True
                    for ancestor in infered.ancestors():
                        if (ancestor.name == 'property' and
                                ancestor.root().name == BUILTINS_NAME):
                            return True
        except astroid.InferenceError:
            pass


def decorated_with_abc(func):
    """Determine if the `func` node is decorated with `abc` decorators."""
    if func.decorators:
        for node in func.decorators.nodes:
            try:
                infered = next(node.infer())
            except astroid.InferenceError:
                continue
            if infered and infered.qname() in ABC_METHODS:
                return True


def unimplemented_abstract_methods(node, is_abstract_cb=decorated_with_abc):
    """
    Get the unimplemented abstract methods for the given *node*.

    A method can be considered abstract if the callback *is_abstract_cb*
    returns a ``True`` value. The check defaults to verifying that
    a method is decorated with abstract methods.
    The function will work only for new-style classes. For old-style
    classes, it will simply return an empty dictionary.
    For the rest of them, it will return a dictionary of abstract method
    names and their inferred objects.
    """
    visited = {}
    try:
        mro = reversed(node.mro())
    except NotImplementedError:
        # Old style class, it will not have a mro.
        return {}
    except astroid.ResolveError:
        # Probably inconsistent hierarchy, don'try
        # to figure this out here.
        return {}
    for ancestor in mro:
        for obj in ancestor.values():
            infered = obj
            if isinstance(obj, astroid.AssName):
                infered = safe_infer(obj)
                if not infered:
                    continue
                if not isinstance(infered, astroid.Function):
                    if obj.name in visited:
                        del visited[obj.name]
            if isinstance(infered, astroid.Function):
                # It's critical to use the original name,
                # since after inferring, an object can be something
                # else than expected, as in the case of the
                # following assignment.
                #
                # class A:
                #     def keys(self): pass
                #     __iter__ = keys
                abstract = is_abstract_cb(infered)
                if abstract:
                    visited[obj.name] = infered
                elif not abstract and obj.name in visited:
                    del visited[obj.name]
    return visited
