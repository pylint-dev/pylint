# Copyright (c) 2005-2006 LOGILAB S.A. (Paris, FRANCE).
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
"""check for new / old style related problems
"""

__revision__ = "$Id: newstyle.py,v 1.8 2006-03-05 14:39:38 syt Exp $"

from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker

MSGS = {
    'E1001': ('Use __slots__ on an old style class',
              'Used when an old style class use the __slots__ attribute.'),
    'E1002': ('Use super on an old style class',
              'Used when an old style class use the super builtin.'),
    'E1003': ('Bad first argument %r given to super class',
              'Used when another argument than the current class is given as \
              first argument of the super builtin.'),
    'E1010': ('Raising a new style class',
              'Used when a new style class is raised since it\'s not yet \
              possible.'),
    
    'W1001': ('Use of "property" on an old style class',
              'Used when PyLint detect the use of the builtin "property" \
              on an old style class while this is relying on new style \
              classes features'),
    'W1010': ('Exception doesn\'t inherit from standard "Exception" class',
              'Used when a custom exception class is raised but doesn\'t \
              inherit from the builtin "Exception" class.'),
    }


class NewStyleConflictChecker(BaseChecker):
    """checks for usage of new style capabilities on old style classes and
    other new/old styles conflicts problems                                    
    * use of property, __slots__, super                                        
    * "super" usage                                                            
    * raising a new style class as exception                                   
    """
    
    __implements__ = (IASTNGChecker,)

    # configuration section name
    name = 'newstyle'
    # messages
    msgs = MSGS
    priority = -2
    # configuration options
    options = ()

#    def __init__(self, linter=None):
#        BaseChecker.__init__(self, linter)
        
    def visit_class(self, node):
        """check __slots__ usage
        """        
        if '__slots__' in node and not node.newstyle:
            self.add_message('E1001', node=node)
        
    def visit_callfunc(self, node):
        """check property usage"""
        parent = node.parent.frame()
        if (isinstance(parent, astng.Class) and
            not parent.newstyle and
            isinstance(node.node, astng.Name)):
            name = node.node.name
            if name == 'property':
                self.add_message('W1001', node=node)
        
    def visit_raise(self, node):
        """check for raising new style class
        """
        # ignore empty raise
        if node.expr1 is None:
            return
        if not isinstance(node.expr1, (astng.Const, astng.Mod)):
            try:
                name = node.expr1.nodes_of_class(astng.Name).next()
                value = name.infer().next()
            except (StopIteration, astng.ResolveError):
                pass
            else:
                if isinstance(value, astng.Class):
                    if value.newstyle:
                        self.add_message('E1010', node=node)
                    elif not inherit_from_std_ex(value):
                        self.add_message('W1010', node=node)
                        
    def visit_function(self, node):
        """check use of super"""
        # ignore actual functions or method within a new style class
        if not node.is_method():
            return
        klass = node.parent.frame()
        for stmt in node.nodes_of_class(astng.CallFunc):
            expr = stmt.node
            if not isinstance(expr, astng.Getattr):
                continue
            call = expr.expr
            # skip the test if using super
            if isinstance(call, astng.CallFunc) and \
               isinstance(call.node, astng.Name) and \
               call.node.name == 'super':
                if not klass.newstyle:
                    # super should not be used on an old style class
                    self.add_message('E1002', node=node)
                else:
                    # super first arg should be the class
                    try:
                        supcls = (call.args and call.args[0].infer().next()
                                  or None)
                    except astng.InferenceError:
                        continue
                    if klass is not supcls:
                        supcls = getattr(supcls, 'name', supcls)
                        self.add_message('E1003', node=node, args=supcls)
                            
                    
                        
def inherit_from_std_ex(node):
    """return true if the given class node is subclass of
    exceptions.Exception
    """
    if node.name == 'Exception' and node.root().name == 'exceptions':
        return True
    for parent in node.ancestors(recurs=False):
        if inherit_from_std_ex(parent):
            return True
    return False
        
def register(linter):
    """required method to auto register this checker """
    linter.register_checker(NewStyleConflictChecker(linter))
