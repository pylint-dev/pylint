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
""" Copyright (c) 2003-2006 LOGILAB S.A. (Paris, FRANCE).
 http://www.logilab.fr/ -- mailto:contact@logilab.fr

 basic checker for Python code
"""

from logilab import astng
from logilab.common.ureports import Table

from pylint.interfaces import IASTNGChecker
from pylint.reporters import diff_string
from pylint.checkers import BaseChecker
from pylint.checkers.utils import are_exclusive

import re

# regex for class/function/variable/constant nane
CLASS_NAME_RGX = re.compile('[A-Z_][a-zA-Z0-9]+$')
MOD_NAME_RGX = re.compile('(([a-z_][a-z0-9_]*)|([A-Z][a-zA-Z0-9]+))$')
CONST_NAME_RGX = re.compile('(([A-Z_][A-Z1-9_]*)|(__.*__))$')
COMP_VAR_RGX = re.compile('[A-Za-z_][A-Za-z0-9_]*$')
DEFAULT_NAME_RGX = re.compile('[a-z_][a-z0-9_]{2,30}$')
# do not require a doc string on system methods
NO_REQUIRED_DOC_RGX = re.compile('__.*__')

del re

def in_loop(node):
    """return True if the node is inside a kind of for loop"""
    parent = node.parent
    while parent is not None:
        if isinstance(parent, (astng.For, astng.ListComp, astng.GenExpr)):
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

def report_by_type_stats(sect, stats, old_stats):
    """make a report of

    * percentage of different types documented
    * percentage of different types with a bad name
    """
    # percentage of different types documented and/or with a bad name
    nice_stats = {} 
    for node_type in ('module', 'class', 'method', 'function'):
        nice_stats[node_type] = {}
        total = stats[node_type]
        if total == 0:
            doc_percent = 0
            badname_percent = 0
        else:
            documented = total - stats['undocumented_'+node_type]
            doc_percent = float((documented)*100) / total
            badname_percent = (float((stats['badname_'+node_type])*100)
                               / total)
        nice_stats[node_type]['percent_documented'] = doc_percent
        nice_stats[node_type]['percent_badname'] = badname_percent
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
                  '%.2f' % nice_stats[node_type]['percent_documented'],
                  '%.2f' % nice_stats[node_type]['percent_badname'])
    sect.append(Table(children=lines, cols=6, rheaders=1))


MSGS = {
    'E0100': ('__init__ method is a generator',
              'Used when the special class method __init__ is turned into a generator \
              by a yield in its body.'),    
    'E0101': ('Explicit return in __init__',
              'Used when the special class method __init__ has an explicit \
              return value.'),    
    'E0102': ('%s already defined line %s',
              'Used when a function / class / method is redefined.'),
    'E0103': ('%r not properly in loop',
              'Used when break or continue keywords are used outside a loop.'),

    'W0101': ('Unreachable code',
              'Used when there is some code behind a "return" or "raise" \
              statement, which will never be accessed.'),
    'W0102': ('Dangerous default value %s as argument',
              'Used when a mutable value as list or dictionary is detected in \
              a default value for an argument.'),
    'W0104': ('Statement seems to have no effect',
              'Used when a statement doesn\'t have (or at least seems to) \
              any effect.'),
    'W0105': ('String statement has no effect',
              'Used when a string is used as a statement (which of course \
              has no effect). This is a particular case of W0104 with its \
              own message so you can easily disable it if you\'re using \
              those strings as documentation, instead of comments.'),
    'W0106': ('Unnecessary semicolon',
              'Used when a statement is endend by a semi-colon (";"), which \
              isn\'t necessary (that\'s python, not C ;)'),

    'W0122': ('Use of the exec statement',
              'Used when you use the "exec" statement, to discourage its \
              usage. That doesn\'t mean you can not use it !'),
    
    'W0141': ('Used builtin function %r',
              'Used when a black listed builtin function is used (see the \
              bad-function option). Usual black listed functions are the ones \
              like map, or filter , where Python offers now some cleaner \
              alternative like list comprehension.'),
    'W0142': ('Used * or ** magic',
              'Used when a function or method is called using `*args` or \
              `**kwargs` to dispatch arguments. This doesn\'t improve readility\
               and should be used with care.'),

    'C0102': ('Black listed name "%s"',
              'Used when the name is listed in the black list (unauthorized \
              names).'),
    'C0103': ('Invalid name "%s" (should match %s)',
              'Used when the name doesn\'t match the regular expression \
              associated to its type (constant, variable, class...).'),
    
    'C0111': ('Missing docstring', # W0131
              'Used when a module, function, class or method has no docstring.\
              Some special methods like __init__ doesn\'t necessary require a \
              docstring.'),
    'C0112': ('Empty docstring', # W0132
              'Used when a module, function, class or method has an empty \
              docstring (it would be to easy ;).'),

    'C0121': ('Missing required attribute "%s"', # W0103
              'Used when an attribute required for modules is missing.'),
    
    }

class BasicChecker(BaseChecker):
    """checks for :                                                            
    * doc strings                                                              
    * modules / classes / functions / methods / arguments / variables name     
    * number of arguments, local variables, branchs, returns and statements in
functions, methods                                                       
    * required module attributes                                             
    * dangerous default values as arguments                                    
    * redefinition of function / method / class                                
    * uses of the global statement                                             
    """
    
    __implements__ = IASTNGChecker

    name = 'basic'
    msgs = MSGS
    priority = -1
    options = (('required-attributes',
                {'default' : (), 'type' : 'csv',
                 'metavar' : '<attributes>',
                 'help' : 'Required attributes for module, separated by a '
                          'comma'}
                ),
               ('no-docstring-rgx',
                {'default' : NO_REQUIRED_DOC_RGX,
                 'type' : 'regexp', 'metavar' : '<regexp>',
                 'help' : 'Regular expression which should only match '
                          'functions or classes name which do not require a '
                          'docstring'}
                ),
##                ('min-name-length',
##                 {'default' : 3, 'type' : 'int', 'metavar' : '<int>',
##                  'help': 'Minimal length for module / class / function / '
##                          'method / argument / variable names'}
##                 ),
               ('module-rgx',
                {'default' : MOD_NAME_RGX,
                 'type' :'regexp', 'metavar' : '<regexp>',
                 'help' : 'Regular expression which should only match correct '
                          'module names'}
                ),
               ('const-rgx',
                {'default' : CONST_NAME_RGX,
                 'type' :'regexp', 'metavar' : '<regexp>',
                 'help' : 'Regular expression which should only match correct '
                          'module level names'}
                ),
               ('class-rgx',
                {'default' : CLASS_NAME_RGX,
                 'type' :'regexp', 'metavar' : '<regexp>',
                 'help' : 'Regular expression which should only match correct '
                          'class names'}
                ),
               ('function-rgx',
                {'default' : DEFAULT_NAME_RGX,
                 'type' :'regexp', 'metavar' : '<regexp>',
                 'help' : 'Regular expression which should only match correct '
                          'function names'}
                ),
               ('method-rgx',
                {'default' : DEFAULT_NAME_RGX,
                 'type' :'regexp', 'metavar' : '<regexp>',
                 'help' : 'Regular expression which should only match correct '
                          'method names'}
                ),
               ('attr-rgx',
                {'default' : DEFAULT_NAME_RGX,
                 'type' :'regexp', 'metavar' : '<regexp>',
                 'help' : 'Regular expression which should only match correct '
                          'instance attribute names'}
                ),
               ('argument-rgx',
                {'default' : DEFAULT_NAME_RGX,
                 'type' :'regexp', 'metavar' : '<regexp>',
                 'help' : 'Regular expression which should only match correct '
                          'argument names'}),
               ('variable-rgx',
                {'default' : DEFAULT_NAME_RGX,
                 'type' :'regexp', 'metavar' : '<regexp>',
                 'help' : 'Regular expression which should only match correct '
                          'variable names'}
                ),
               ('inlinevar-rgx',
                {'default' : COMP_VAR_RGX,
                 'type' :'regexp', 'metavar' : '<regexp>',
                 'help' : 'Regular expression which should only match correct '
                          'list comprehension / generator expression variable \
                          names'}
                ),
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
               
               ('bad-functions',
                {'default' : ('map', 'filter', 'apply', 'input'),
                 'type' :'csv', 'metavar' : '<builtin function names>',
                 'help' : 'List of builtins function names that should not be '
                          'used, separated by a comma'}
                ),
               )
    reports = ( ('R0101', 'Statistics by type', report_by_type_stats), )
    
    def __init__(self, linter):
        BaseChecker.__init__(self, linter)
        self.stats = None
        self._returns = None
        
    def open(self):
        """initialize visit variables and statistics
        """
        self._returns = []
        self.stats = self.linter.add_stats(module=0, function=0,
                                           method=0, class_=0,
                                           badname_module=0,
                                           badname_class=0, badname_function=0,
                                           badname_method=0, badname_attr=0,
                                           badname_const=0,
                                           badname_variable=0,
                                           badname_inlinevar=0,
                                           badname_argument=0,
                                           undocumented_module=0,
                                           undocumented_function=0,
                                           undocumented_method=0,
                                           undocumented_class=0)

    def visit_module(self, node):
        """check module name, docstring and required arguments
        """
        self.stats['module'] += 1
        self._check_name('module', node.name.split('.')[-1], node)
        self._check_docstring('module', node)
        self._check_required_attributes(node, self.config.required_attributes)
            
    def visit_class(self, node):
        """check module name, docstring and redefinition
        increment branch counter
        """
        self.stats['class'] += 1
        self._check_name('class', node.name, node)
        if self.config.no_docstring_rgx.match(node.name) is None:
            self._check_docstring('class', node)
        self._check_redefinition('class', node)
        for attr, anodes in node.instance_attrs.items():
            self._check_name('attr', attr, anodes[0])

    def visit_discard(self, node):
        """check for various kind of statements without effect"""
        expr = node.expr
        if isinstance(node.expr, astng.Const):
            # XXX lineno maybe dynamically set incidently
            if expr.value is None and expr.lineno is None:
                # const None node with lineno to None are inserted
                # on unnecessary semi-column
                # XXX navigate to get a correct lineno
                brothers = list(node.parent.getChildNodes())
                previoussibling = brothers[brothers.index(node)-1]
                self.add_message('W0106', node=previoussibling)
                return
            if isinstance(expr.value, basestring):
                # tread string statement in a separated message
                self.add_message('W0105', node=node)
                return
        # ignore if this is a function call (can't predicate side effects)
        # or a yield (which are wrapped by a discard node in py >= 2.5)
        if not isinstance(node.expr, (astng.CallFunc, astng.Yield)):
            self.add_message('W0104', node=node)

    def visit_function(self, node):
        """check function name, docstring, arguments, redefinition,
        variable names, max locals
        """
        is_method = node.is_method()
        self._returns.append([])
        f_type = is_method and 'method' or 'function'
        self.stats[f_type] += 1
        # function name
        self._check_name(f_type, node.name, node)
        # docstring
        if self.config.no_docstring_rgx.match(node.name) is None:
            self._check_docstring(f_type, node)
        # check default arguments'value
        self._check_defaults(node)
        # check arguments name
        args = node.argnames
        if args is not None:
            self._recursive_check_names(args, node)
        # check for redefinition
        self._check_redefinition(is_method and 'method' or 'function', node)

    def leave_function(self, node):
        """most of the work is done here on close:
        checks for max returns, branch, return in __init__
        """
        returns = self._returns.pop()
        if node.is_method() and node.name == '__init__':
            if  node.is_generator():
                self.add_message('E0100', node=node)
            else:
                values = [r.value for r in returns]
                if  [v for v in values if not (
                    (isinstance(v, astng.Const) and v.value is None)
                    or  (isinstance(v, astng.Name) and v.name == 'None'))]:
                    self.add_message('E0101', node=node)

    def visit_assname(self, node):
        """check module level assigned names"""
        frame = node.frame()
        ass_type = node.ass_type()
        if isinstance(ass_type, (astng.ListCompFor, astng.GenExprFor)):
            self._check_name('inlinevar', node.name, node)
        elif isinstance(frame, astng.Module):
            if isinstance(ass_type, astng.Assign) and not in_loop(ass_type):
                self._check_name('const', node.name, node)
        elif isinstance(frame, astng.Function):
            # global introduced variable aren't in the function locals
            if node.name in frame:
                self._check_name('variable', node.name, node)
    
    def visit_return(self, node):
        """check is the node has a right sibling (if so, that's some unreachable
        code)
        """
        if not self._returns:
            raise SyntaxError("'return' outside function")
        self._returns[-1].append(node)
        self._check_unreachable(node)
        
    def visit_yield(self, node):
        """check is the node has a right sibling (if so, that's some unreachable
        code)
        """
        self._returns[-1].append(node)

    def visit_continue(self, node):
        """check is the node has a right sibling (if so, that's some unreachable
        code)
        """
        self._check_unreachable(node)
        self._check_in_loop(node, 'continue')

    def visit_break(self, node):
        """check is the node has a right sibling (if so, that's some unreachable
        code)
        """
        self._check_unreachable(node)
        self._check_in_loop(node, 'break')

    def visit_raise(self, node):
        """check is the node has a right sibling (if so, that's some unreachable
        code)
        """
        self._check_unreachable(node)

    def visit_exec(self, node):
        """just pring a warning on exec statements"""
        self.add_message('W0122', node=node)

    def visit_callfunc(self, node):
        """visit a CallFunc node -> check if this is not a blacklisted builtin
        call and check for * or ** use
        """
        if isinstance(node.node, astng.Name):
            name = node.node.name
            # ignore the name if it's not a builtin (ie not defined in the
            # locals nor globals scope)
            if not (node.frame().has_key(name) or
                    node.root().has_key(name)):
                if name in self.config.bad_functions:
                    self.add_message('W0141', node=node, args=name)
        if node.star_args or node.dstar_args:
            self.add_message('W0142', node=node.node)
            

    def _check_unreachable(self, node):
        """check unreachable code"""
        unreach_stmt = node.next_sibling()
        if unreach_stmt is not None:
            self.add_message('W0101', node=unreach_stmt)
            
    def _check_in_loop(self, node, node_name):
        """check that a node is inside a for or while loop"""
        _node = node.parent
        while _node:
            if isinstance(_node, (astng.For, astng.While)):
                break
            _node = _node.parent
        else:
            self.add_message('E0103', node=node, args=node_name)
        
    def _check_redefinition(self, redef_type, node):
        """check for redefinition of a function / method / class name"""
        defined_self = node.parent.frame()[node.name]
        if defined_self is not node and not are_exclusive(node, defined_self):
            self.add_message('E0102', node=node,
                             args=(redef_type, defined_self.lineno))
        
    def _check_docstring(self, node_type, node):
        """check the node has a non empty docstring"""
        docstring = node.doc
        if docstring is None:
            self.stats['undocumented_'+node_type] += 1
            self.add_message('C0111', node=node)
        elif not docstring.strip():
            self.stats['undocumented_'+node_type] += 1
            self.add_message('C0112', node=node)
            
    def _recursive_check_names(self, args, node):
        """check names in a possibly recursive list <arg>"""
        for arg in args:
            if type(arg) is type(''):
                self._check_name('argument', arg, node)
            else:
                self._recursive_check_names(arg, node)
    
    def _check_name(self, node_type, name, node):
        """check for a name using the type's regexp"""
        if name in self.config.good_names:
            return
        if name in self.config.bad_names:
            self.stats['badname_' + node_type] += 1
            self.add_message('C0102', node=node, args=name)
            return
        regexp = getattr(self.config, node_type + '_rgx')
        if regexp.match(name) is None:
            self.add_message('C0103', node=node, args=(name, regexp.pattern))
            self.stats['badname_' + node_type] += 1
            

    def _check_defaults(self, node):
        """check for dangerous default values as arguments"""
        for default in node.defaults:
            try:
                value = default.infer().next()
            except astng.InferenceError:
                continue
            if isinstance(value, (astng.Dict, astng.List)):
                if value is default:
                    msg = default.as_string()
                else:
                    msg = '%s (%s)' % (default.as_string(), value.as_string())
                self.add_message('W0102', node=node, args=(msg,))
        
    def _check_required_attributes(self, node, attributes):
        """check for required attributes"""
        for attr in attributes:
            if not node.has_key(attr):
                self.add_message('C0121', node=node, args=attr)

    
def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(BasicChecker(linter))

