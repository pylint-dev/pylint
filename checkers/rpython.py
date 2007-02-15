# Copyright (c) 2007 LOGILAB S.A. (Paris, FRANCE).
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
"""check a python program is `Restricted Python`_ compliant. It is intended to
find potential pypy translation bugs at once without waiting a long time to get
translation failures one by one.
"""

__docformat__ = "restructuredtext en"

import re

from logilab.common.compat import set
from logilab import astng

from pylint.interfaces import IASTNGChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import safe_infer, is_super, display_type


MSGS = {
    'E1201': ('Using unavailable keyword %r',
              'Used when a keyword which is not available in rpython is used.'),
    'E1202': ('Using unavailable builtin %r',
              'Used when a built-in which is not available in rpython is used.'),
    
    'E1203': ('Multiple types assigned to %s %r',
              'Used when an identifier or attribut is infered as having values \
of different types assigned.'),
    
    'E1204': ('Non homogeneous values in list',
              'Used when a list is not containing homogeneous values.'),
    
##     'E1205': ('Identifier %r is not properly initialized',
##               'Used when an identifier is used in some conditional block \
## without being properly initialized before that block.'),
    
    'E1206': ('Modifying global %r from module %s',
              'Used when a module variable is modified, which is not allowed in \
rpython since globals are considered as constants.'),

    'E1207': ('Using negative slice %s %s (infered to %s)',
              'Used when a negative integer is used as lower, upper or step of a slice.'),
    'E1208': ('Using non constant step',
              'Used when a variable not annotated as a constant is used as step of a slice.'),
    
    'E1208': ('%r format is not supported',
              'Used when the unavailable "%r" formatting instruction is used.'),
    }

# XXX: nested functions/classes
# XXX: properties not supported ?

# 'global' is available even if it doesn't help anything since globals are
# considered immutable
UNAVAILABLE_KEYWORDS = set(('yield', 'exec', 'lambda', 'print'))

import __builtin__
BUILTINLIST = set([x for x in dir(__builtin__) if x[0].islower()]) 
AUTHORIZED = set(('abs', 'apply',
                  'basestring', 'bool',
                  'chr', 'cmp', 'coerce',
                  'float', 'hasattr', 'hash', 'hex',
                  'int', 'isinstance',
                  'len', 'list', 'max', 'min', 'oct', 'ord',
                  'range', 'slice', 'str', 'tuple', 'type',
                  'unichr', 'xrange', 'zip'
                  ))

UNAVAILABLE_BUILTINS = {
    '__builtin__': BUILTINLIST - AUTHORIZED,
    'site': 'help',
    }
#from pprint import pprint
#pprint(sorted(BUILTINLIST - AUTHORIZED))
del BUILTINLIST, AUTHORIZED

BUILTIN_MODIFIERS = {'dict': set(('clear', 'fromkeys', 'pop', 'popitem', 'setdefault', 'update')),
                     'list': set(('append', 'extend', 'insert', 'pop', 'remove', 'reverse', 'sort')),}

REPR_NAMED_FORMAT_INSTR = re.compile('%\([^)]+\)r')

class RPythonChecker(BaseChecker):
    """check a python program is `Restricted Python`_ compliant. Restricted python
    is used in the PyPy_ project to make a python program compilable.

    .. _`Restricted Python`: http://codespeak.net/pypy/dist/pypy/doc/coding-guide.html
    .. _`PyPy`: http://codespeak.net/pypy/
    """
    
    __implements__ = (IASTNGChecker,)

    # configuration section name
    name = 'rpython'
    enabled = False # disabled by default
    # messages
    msgs = MSGS
    priority = -1
    # configuration options
    options = ()
    

    def __init__(self, linter=None):
        BaseChecker.__init__(self, linter)
        self._rpython = True

        
    def visit_name(self, node):
        """check unavailable builtins are not used"""
        if not self._rpython:
            return
        try:
            infered = node.infer().next()
        except astng.InferenceError:
            return # XXX
        if infered is astng.YES:
            return # XXX
        name = node.name
        module = infered.root().name
        if module in UNAVAILABLE_BUILTINS and name in UNAVAILABLE_BUILTINS[module]:
            self.add_message('E1202', node=node, args=name)
##         # E1205 check, example:
##         #
##         # ...
##         # if bla:
##         #     a = 4
##         # else:
##         #     a = 5
##         # print a
##         #
##         # in such a case a should be defined before the if/else block.
##         # So here if name is a local name we have to ckeck it's defined in the
##         # same block or in a parent block
##         frame, stmts = node.lookup(name)
##         if frame is node.frame() and len(stmts) > 1:
##             # XXX only consider the first assignment ?
##             assstmt = stmts[0].statement().parent
##             _node = node.statement()
##             while _node:
##                 if _node is assstmt:
##                     break
##                 _node = _node.parent
##             else:
##                 self.add_message('E1205', node=node, args=name)
        try:
            for infered in node.infer():
                if infered is astng.YES:
                    continue
                break
            else:
                return
        except astng.InferenceError:
            return
        frame = infered.frame()
        # check for more global alteration
        if not frame is node.frame() and isinstance(frame, astng.Module):
            # accessing to a global
            if isinstance(infered, (astng.List, astng.Dict)):
                # is it a tuple/dict item assignment ?
                ass = node.parent
                last = node
                while ass and not isinstance(ass, astng.Assign):
                    last = last
                    ass = ass.parent
                # "not last is ass.expr" is checking the global isn't in the rhs
                if ass is not None and not last is ass.expr:
                    self.add_message('E1206', node=node, args=(node.name, node.root().name))
                    return
                # is it a call to a tuple/dict method modifying it ?
                if isinstance(node.parent, astng.Getattr) and \
                       isinstance(node.parent.parent, astng.CallFunc):
                    if node.parent.attrname in BUILTIN_MODIFIERS[infered.name]:
                        self.add_message('E1206', node=node, args=(node.name, node.root().name))
                        
        
    def visit_class(self, node):
        """check class attributes have homogeneous types"""
        if not self._rpython:
            return
        for name in node.instance_attrs.keys():
            types = set()
            for infered in astng.Instance(node).igetattr(name):
                if infered is astng.YES:
                    continue
                # skip None
                if isinstance(infered, astng.Const) and infered.value is None:
                    continue
                types.add(str(infered))
            if len(types) > 1:
                self.add_message('E1203', node=node, args=('attribute', name))
        
    def visit_function(self, node):
        """check function locals have homogeneous types"""
        docstring = node.doc
        if docstring is not None and 'NOT RPYTHON' in docstring:
            self._rpython = False
        if not self._rpython:
            return
        for name in node.locals.keys():
            types = set()
            for infered in node.ilookup(name):
                if infered is astng.YES:
                    continue
                # skip None
                if isinstance(infered, astng.Const) and infered.value is None:
                    continue
                types.add(str(infered))
            if len(types) > 1:
                self.add_message('E1203', node=node, args=('identifier', name))

    def leave_function(self, node):
        docstring = node.doc
        if docstring is not None and 'NOT RPYTHON' in docstring:
            self._rpython = True
        
    def visit_list(self, node):
        """check list contains homogeneous types"""
        if not self._rpython:
            return
        types = set()
        for node in node.nodes:
            try:
                # XXX use ifilter + filter to factorize filtering below
                for infered in node.infer():
                    if infered is astng.YES:
                        continue
                    # XXX skip None ?
                    if isinstance(infered, astng.Const) and infered.value is None:
                        continue
                    types.add(str(infered))
            except astng.InferenceError:
                continue
        if len(types) > 1:
            self.add_message('E1204', node=node)

    
    def visit_assattr(self, node):
        """check we are not modifying a module attribute"""
        if not self._rpython:
            return
        try:
            infered = node.expr.infer().next()
        except astng.InferenceError:
            return # XXX
        if isinstance(infered, astng.Module):
            self.add_message('E1206', node=node, args=(node.attrname, infered.name))
        
    def visit_assname(self, node):
        """check we are not modifying a module attribute"""
        if not self._rpython:
            return
        if not node.name in node.frame().locals.keys():
            self.add_message('E1206', node=node, args=(node.name, node.root().name))
            
        
    def visit_slice(self, node):
        """no negative index"""
        if not self._rpython:
            return
        self.check_slice(node.lower, node.upper)
        
    def visit_sliceobj(self, node):
        """no negative index"""
        if not self._rpython:
            return
        sdef = []
        for bound in node.nodes:
            if isinstance(bound, astng.Const) and bound.value is None:
                sdef.append(None)
            else:
                sdef.append(bound)
        self.check_slice(*sdef)
            
    def check_slice(self, start, stop, step=None):
        """
        * step has to be annotated as a constant and >= 0
        * start >= 0
        * stop >= 0
        * [:-1] et [0:-1] OK
        """

        if start is not None:
            value = self.check_positive_integer(start, 'start index')
        if stop is not None:
            self.check_positive_integer(stop, 'stop index', start is None or value == 0)
        if step is not None:
            try:
                for infered in step.infer():
                    if infered is astng.YES:
                        self.add_message('E1208', node=step)
                        return
            except astng.InferenceError:
                self.add_message('E1208', node=node)
                return
            self.check_positive_integer(step, 'step')
        
    def check_positive_integer(self, node, msg, minus_one_allowed=False):
        value = None
        try:
            for infered in node.infer():
                if infered is astng.YES:
                    continue
                if not isinstance(infered, astng.Const) or not isinstance(infered.value, int):
                    continue # XXX specific message
                if infered.value < 0:
                    if minus_one_allowed and infered.value == -1:
                        value = infered.value
                        continue
                    self.add_message('E1207', node=node, args=(msg,
                                                               node.as_string(),
                                                               infered.value))
                else:
                    value = infered.value
        except astng.InferenceError:
            pass
        return value

    def visit_mod(self, node):
        try:
            for infered in node.left.infer():
                if infered is astng.YES:
                    continue
                if not isinstance(infered, astng.Const) or not isinstance(infered.value, basestring):
                    continue # XXX specific message
                value = infered.value.replace('%%', '%%')
                if '%r' in value or REPR_NAMED_FORMAT_INSTR.search(value):
                    self.add_message('E1208', node=infered)
                
        except astng.InferenceError:
            pass
        
# XXX: checking rpython should do an "entry point search", not a "project search" (eg from a modules/packages list)
# more over we should differentiate between initial import vs runtime imports, no ?

for name in UNAVAILABLE_KEYWORDS:
    def visit_unavailable_keyword(self, node, name=name):
        if not self._rpython:
            return
        self.add_message('E1201', node=node, args=name)
    setattr(RPythonChecker, 'visit_%s' % name, visit_unavailable_keyword)
del name
    
def register(linter):
    """required method to auto register this checker """
    linter.register_checker(RPythonChecker(linter))
