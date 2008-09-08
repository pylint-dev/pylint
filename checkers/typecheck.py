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

from logilab.common.compat import set
from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer, is_super, display_type

MSGS = {
    'E1101': ('%s %r has no %r member',
              'Used when a variable is accessed for an unexistant member.'),
    'E1102': ('%s is not callable',
              'Used when an object being called has been infered to a non \
              callable object'),
    'E1103': ('%s %r has no %r member (but some types could not be inferred)',
              'Used when a variable is accessed for an unexistant member, but \
              astng was not able to interpret all possible types of this \
              variable.'),
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
    options = (('ignore-mixin-members',
                {'default' : True, 'type' : 'yn', 'metavar': '<y_or_n>',
                 'help' : 'Tells wether missing members accessed in mixin \
class should be ignored. A mixin class is detected if its name ends with \
"mixin" (case insensitive).'}
                ),

               ('ignored-classes',
                {'default' : ('SQLObject',),
                 'type' : 'csv',
                 'metavar' : '<members names>',
                 'help' : 'List of classes names for which member attributes \
should not be checked (useful for classes with attributes dynamicaly set).'}
                 ),

               ('zope',
                {'default' : False, 'type' : 'yn', 'metavar': '<y_or_n>',
                 'help' : 'When zope mode is activated, add a predefined set \
of Zope acquired attributes to generated-members.'}
                ),
               ('generated-members',
                {'default' : (
        'REQUEST', 'acl_users', 'aq_parent'),
                 'type' : 'csv',
                 'metavar' : '<members names>',
                 'help' : 'List of members which are set dynamically and \
missed by pylint inference system, and so shouldn\'t trigger E0201 when \
accessed.'}
                ),
        )
    def __init__(self, linter=None):
        BaseChecker.__init__(self, linter)
        self.generated_members = list(self.config.generated_members)
        if self.config.zope:
            self.generated_members.extend(('REQUEST', 'acl_users', 'aq_parent'))
            
    def visit_getattr(self, node):
        """check that the accessed attribute exists

        to avoid to much false positives for now, we'll consider the code as
        correct if a single of the infered nodes has the accessed attribute.

        function/method, super call and metaclasses are ignored
        """
        if node.attrname in self.config.generated_members:
            # attribute is marked as generated, stop here
            return
        try:
            infered = list(node.expr.infer())
        except astng.InferenceError:
            return
        # list of (node, nodename) which are missing the attribute
        missingattr = set()
        ignoremim = self.config.ignore_mixin_members
        inference_failure = False
        for owner in infered:
            # skip yes object
            if owner is astng.YES:
                inference_failure = True
                continue
            # skip None anyway
            if isinstance(owner, astng.Const) and owner.value is None:
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
                owner.getattr(node.attrname)
            except AttributeError:
                # XXX method / function
                continue
            except astng.NotFoundError, ex:
                if isinstance(owner, astng.Instance) \
                       and owner.has_dynamic_getattr():
                    continue
                # explicit skipping of optparse'Values class
                if owner.name == 'Values' and \
                       owner.root().name in ('optik', 'optparse'):
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
                if isinstance(owner, astng.Instance):
                    actual = owner._proxied
                else:
                    actual = owner
                if actual in done:
                    continue
                done.add(actual)
                if inference_failure:
                    msgid = 'E1103'
                else:
                    msgid = 'E1101'
                self.add_message(msgid, node=node,
                                 args=(display_type(owner), name,
                                       node.attrname))


    def visit_assign(self, node):
        """check that if assigning to a function call, the function is
        possibly returning something valuable
        """
        if not isinstance(node.expr, astng.CallFunc):
            return
        function_node = safe_infer(node.expr.node)
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
        called = safe_infer(node.node)
        # only function, generator and object defining __call__ are allowed
        if called is not None and not called.callable():
            self.add_message('E1102', node=node, args=node.node.as_string())
        
    
def register(linter):
    """required method to auto register this checker """
    linter.register_checker(TypeChecker(linter))
