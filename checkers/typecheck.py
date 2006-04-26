# Copyright (c) 2006 LOGILAB S.A. (Paris, FRANCE).
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
"""try to find more bugs in the code using astng inference capabilities
"""

__revision__ = "$Id: typecheck.py,v 1.12 2006-04-19 16:16:20 syt Exp $"

from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker

MSGS = {
    'E1101': ('%s %r has no %r member',
              'Used when a class is accessed for an unexistant member.'),
    'E1102': ('%s is not callable',
              'Used when an object being called has been infered to a non \
              callable object'),
    'E1111': ('Assigning to function call which doesn\'t return',
              'Used when an assigment is done on a function call but the \
              infered function doesn\'t return anything.'),
    'W1111': ('Assigning to function call which only returns None',
              'Used when an assigment is done on a function call but the \
              infered function returns nothing but None.'),
    }


class TypeChecker(BaseChecker):
    """try to find bugs in the code using type inference
    """
    
    __implements__ = (IASTNGChecker,)

    # configuration section name
    name = 'typecheck'
    # messages
    msgs = MSGS
    priority = -1
    # configuration options
    options = (
               ('ignore-mixin-members',
                {'default' : True, 'type' : 'yn', 'metavar': '<y_or_n>',
                 'help' : 'Tells wether missing members accessed in mixin \
class should be ignored. A mixin class is detected if its name ends with \
"mixin" (case insensitive).'}
                ),
               
               ('zope',
                {'default' : False, 'type' : 'yn', 'metavar': '<y_or_n>',
                 'help' : 'When zope mode is activated, consider the \
acquired-members option to ignore access to some undefined attributes.'}
                ),
               ('acquired-members',
                {'default' : (
        'REQUEST', 'acl_users', 'aq_parent'),
                 'type' : 'csv',
                 'metavar' : '<members names>',
                 'help' : 'List of members which are usually get through \
zope\'s acquisition mecanism and so shouldn\'t trigger E0201 when accessed \
(need zope=yes to be considered.'}
                ),
        )

    def visit_getattr(self, node):
        """check that the accessed attribute exists"""
        # if we are running in zope mode, is it an acquired attribute ?
        if self.config.zope and node.attrname in self.config.acquired_members:
            return
        try:
            infered = list(node.expr.infer())
            for owner in infered:
                # skip yes object
                if owner is astng.YES:
                    continue
                # if there is ambiguity, skip None
                if len(infered) > 1 and isinstance(owner, astng.Const) \
                       and owner.value is None:
                    continue
                # XXX "super" call
                owner_name = getattr(owner, 'name', 'None')
                if owner_name == 'super' and \
                   owner.root().name == '__builtin__':
                    continue
                if getattr(owner, 'type', None) == 'metaclass':
                    continue
                if self.config.ignore_mixin_members \
                       and owner_name[-5:].lower() == 'mixin':
                    continue
                #print owner.name, owner.root().name
                try:
                    owner.getattr(node.attrname)
                except AttributeError:
                    # XXX method / function
                    continue
                except astng.NotFoundError:
                    if isinstance(owner, astng.Instance):
                        if hasattr(owner, 'has_dynamic_getattr') and owner.has_dynamic_getattr():
                            continue
                        # XXX
                        if getattr(owner, 'name', None) == 'Values' and \
                               owner.root().name == 'optparse':
                            continue
                        _type = 'Instance of'
                    elif isinstance(owner, astng.Module):
                        _type = 'Module'
                    else:
                        _type = 'Class'
                    self.add_message('E1101', node=node,
                                     args=(_type, owner_name, node.attrname))
                # XXX: stop on the first found
                # this is a bad solution to fix func_noerror_socket_member.py
                break
        except astng.InferenceError:
            pass

    def visit_assign(self, node):
        """check that if assigning to a function call, the function is
        possibly returning something valuable
        """
        if not isinstance(node.expr, astng.CallFunc):
            return
        function_node = self._safe_infer(node.expr.node)
        # skip class, generator and uncomplete function definition
        if not (isinstance(function_node, astng.Function) and
                function_node.root().fully_defined()):
            return
        if function_node.is_generator() \
               or function_node.is_abstract(pass_is_abstract=False):
            return
        returns = list(function_node.nodes_of_class(astng.Return,
                                                    skip_klass=astng.Function))
        if len(returns) == 0:
            self.add_message('E1111', node=node)
        else:
            for rnode in returns:
                if not (isinstance(rnode.value, astng.Name)
                        and rnode.value.name == 'None'):
                    break
            else:
                self.add_message('W1111', node=node)

    def visit_callfunc(self, node):
        """check that called method are infered to callable objects
        """
        called = self._safe_infer(node.node)
        # only function, generator and object defining __call__ are allowed
        if called is not None and not called.callable():
            self.add_message('E1102', node=node, args=node.node.as_string())
        
    def _safe_infer(self, node):
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
    
def register(linter):
    """required method to auto register this checker """
    linter.register_checker(TypeChecker(linter))
