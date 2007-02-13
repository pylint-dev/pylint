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
    'E1204': ('Non homogeneous values in %s %r',
              'Used when a tuple or list is not containing homogeneous values.'),
    
    'E1205': ('Identifier %r is not properly initialized',
              'Used when an identifier is used in some conditional block \
without being properly initialized before that block.'),
    
    'E1206': ('Modifying global %r from module %s',
              'Used when a module variable is modified, which is not allowed in \
rpython since globals are considered as constants.'),

    'E1207': ('Using negative slice index %s',
              'Used when a negative integer is used as lower, upper or step of a slice.'),
    }

# XXX: nested functions/classes
# XXX: generator expression ? list comprehension ?
# XXX: import rules
# XXX: slice indexes
# XXX: dict homegeneity
# XXX: os.path.join('a', 'b') OK but os.path.join('a', 'b', 'c') KO

UNAVAILABLE_KEYWORDS = set(('yield', 'global')) # print, lambda ?

UNAVAILABLE_BUILTINS = set(('dict', 'file', 'open', # super ?  set ?
                            'enumerate', 'zip')) # range, xrange ?
# "abs" "apply" "basestring"
# "bool" "buffer" "callable" "chr" "classmethod"
# "cmp" "coerce" "compile" "complex" "copyright"
# "delattr" "dict" "dir" "divmod"
# "filter" "float" "getattr" "globals" "hasattr"
# "hash" "hex" "id" "input" "int" "intern"
# "isinstance" "issubclass" "iter" "len" "license"
# "list" "locals" "long" "map" "max" "min" "object"
# "oct" "open" "ord" "pow" "property" "range"
# "raw_input" "reduce" "reload" "repr" "round"
# "setattr" "slice" "staticmethod" "str" "sum"
# "super" "tuple" "type" "unichr" "unicode"
# "xrange"

class RPythonChecker(BaseChecker):
    """check a python program is `Restricted Python`_ compliant. Restricted python
    is used in the PyPy_ project to make a python program compilable.

    .. _`Restricted Python`: http://codespeak.net/pypy
    .. _`PyPy`: http://codespeak.net/pypy/doc/XXX
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

        
    def visit_name(self, node):
        """check unavailable builtins are not used"""
        try:
            infered = node.infer().next()
        except astng.InferenceError:
            return # XXX
        if infered is astng.YES:
            return # XXX 
        if infered.root().name == '__builtin__' and node.name in UNAVAILABLE_BUILTINS:
            self.add_message('E1202', node=node, args=name)
        # E1205 check, example:
        #
        # ...
        # if bla:
        #     a = 4
        # else:
        #     a = 5
        # print a
        #
        # in such a case a should be defined before the if/else block.
        # So here if name is a local name we have to ckeck it's defined in the
        # same block or in a parent block
        frame, stmts = self.lookup(name)
        if frame is self.frame():
            # XXX only consider the first assignment ?
            for assign in stmts[0]:
                assstmt = assign.statement()
                _node = node.statement()
                while _node:
                    if _node is assstmt:
                        return
                    _node = _node.parent
            self.add_message('E1205', node=node, args=name)

    def visit_class(self, node):
        """check class attributes have homogeneous types"""
        for name in node.instance_attrs.keys():
            types = set()
            for infered in node.igetattr(name):
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
            
    def visit_list(self, node):
        """check list or tuple contains homogeneous types"""
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
            self.add_message('E1204', node=node, args=('identifier', name))

    visit_tuple = visit_list
    
    def visit_assattr(self, node):
        """check we are not modifying a module attribute"""
        try:
            infered = node.expr.infer().next()
        except astng.InferenceError:
            return # XXX
        if isinstance(infered, astng.Module):
            self.add_message('E1206', node=node, args=(node.attrname, infered.name))
        
    def visit_slice(self, node):
        """no negative index"""
        for bound in (node.lower, node.upper):
            self.check_slice_arg(bound)
        
    def visit_sliceobj(self, node):
        """no negative index"""
        for bound in node.nodes:
            self.check_slice_arg(bound)
            
    def check_slice_arg(self, node):
        try:
            for infered in node.infer():
                if infered is YES:
                    continue
                assert isinstance(infered, astng.Const)
                if not isinstance(const.value, int):
                    continue # XXX specific message
                if const.value < 0:
                    self.add_message('E1207', node=node, args=node)
        except InferenceError:
            pass
        
# XXX: checking rpython should do an "entry point search", not a "project search" (eg from a modules/packages list)
# more over we should differentiate between initial import vs runtime imports, no ?

for name in UNAVAILABLE_KEYWORDS:
    def visit_unavailable_keyword(self, node, name=name):
        self.add_message('E1201', node=node, args=name)
    setattr(RPythonChecker, 'visit_%s' % name, visit_unavailable_keyword)
    
    
def register(linter):
    """required method to auto register this checker """
    linter.register_checker(RPythonChecker(linter))
