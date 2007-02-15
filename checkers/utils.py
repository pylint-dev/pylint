# pylint: disable-msg=W0611
#
# Copyright (c) 2003-2007 LOGILAB S.A. (Paris, FRANCE).
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
"""some functions that may be usefull for various checkers
"""

from logilab.common import flatten

from logilab import astng
from logilab.astng.utils import are_exclusive
try:
    # python >= 2.4
    COMP_NODE_TYPES = (astng.ListComp, astng.GenExpr)
    FOR_NODE_TYPES = (astng.For, astng.ListCompFor, astng.GenExprFor)
except AttributeError:
    COMP_NODE_TYPES = astng.ListComp
    FOR_NODE_TYPES = (astng.For, astng.ListCompFor)

def safe_infer(node):
    """return the infered value for the given node.
    Return None if inference failed or if there is some ambiguity (more than
    one node has been infered)
    """
    try:
        inferit = node.infer()
        value = inferit.next()
    except astng.InferenceError:
        return
    try:
        inferit.next()
        return # None if there is ambiguity on the infered node
    except StopIteration:
        return value

def is_super(node):
    """return True if the node is referencing the "super" builtin function
    """
    if getattr(node, 'name', None) == 'super' and \
           node.root().name == '__builtin__':
        return True
    return False

def is_error(node):
    """return true if the function does nothing but raising an exception"""
    for child_node in node.code.getChildNodes():
        if isinstance(child_node, astng.Raise):
            return True
        return False

def is_raising(stmt):
    """return true if the given statement node raise an exception
    """
    for node in stmt.nodes:
        if isinstance(node, astng.Raise):
            return True
    return False

def is_empty(node):
    """return true if the given node does nothing but 'pass'"""
    for child_node in node.getChildNodes():
        if isinstance(child_node, astng.Pass):
            return True
        else:
            return False

builtins = __builtins__.copy()
SPECIAL_BUILTINS = ('__builtins__',) # '__path__', '__file__')

def is_builtin(name): # was is_native_builtin
    """return true if <name> could be considered as a builtin defined by python
    """
    if builtins.has_key(name):
        return True
    if name in SPECIAL_BUILTINS:
        return True
    return False

def is_defined_before(var_node, comp_node_types=COMP_NODE_TYPES):
    """return True if the variable node is defined by a parent node (list
    or generator comprehension, lambda) or in a previous sibling node
    one the same line (statement_defining ; statement_using)
    """
    varname = var_node.name
    _node = var_node.parent
    while _node:
        if isinstance(_node, comp_node_types):
            for ass_node in _node.nodes_of_class(astng.AssName):
                if ass_node.name == varname:
                    return True
        elif isinstance(_node, astng.For):
            for ass_node in _node.assign.nodes_of_class(astng.AssName):
                if ass_node.name == varname:
                    return True
        elif isinstance(_node, (astng.Lambda, astng.Function)):
            if varname in flatten(_node.argnames):
                return True
            if getattr(_node, 'name', None) == varname:
                return True
            break
        _node = _node.parent
    # possibly multiple statements on the same line using semi colon separator
    stmt = var_node.statement()
    _node = stmt.previous_sibling()
    lineno = stmt.lineno
    while _node and _node.lineno == lineno:
        for ass_node in _node.nodes_of_class(astng.AssName):
            if ass_node.name == varname:
                return True
        for imp_node in _node.nodes_of_class( (astng.From, astng.Import)):
            if varname in [name[1] or name[0] for name in imp_node.names]:
                return True
        _node = _node.previous_sibling()
    return False

def is_func_default(node):
    """return true if the name is used in function default argument's value
    """
    parent = node.parent
    if parent is None:
        return 0
    if isinstance(parent, astng.Function) and parent.defaults and \
           node in parent.defaults:
        return 1
    return is_func_default(parent)
    
def is_ancestor_name(frame, node):
    """return True if `frame` is a astng.Class node with `node` in the
    subtree of its bases attribute
    """
    try:
        bases = frame.bases
    except AttributeError:
        return False
    for base in bases:
        if node in base.nodes_of_class(astng.Name):
            return True
    return False

def assign_parent(node):
    """return the higher parent which is not an AssName, AssTuple or AssList
    node
    """
    while node and isinstance(node, (astng.AssName,
                                     astng.AssTuple,
                                     astng.AssList)):
        node = node.parent
    return node

def overrides_an_abstract_method(class_node, name):
    """return True if pnode is a parent of node"""
    for ancestor in class_node.ancestors():
        if name in ancestor and isinstance(ancestor[name], astng.Function) and \
               ancestor[name].is_abstract(pass_is_abstract=False):
            return True
    return False

def overrides_a_method(class_node, name):
    """return True if <name> is a method overridden from an ancestor"""
    for ancestor in class_node.ancestors():
        if name in ancestor and isinstance(ancestor[name], astng.Function):
            return True
    return False

def display_type(node):
    """return the type of this node for screen display"""
    if isinstance(node, astng.Instance):
        return 'Instance of'
    elif isinstance(node, astng.Module):
        return 'Module'
    return 'Class'
