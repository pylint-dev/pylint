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
"""check for signs of poor design"""

from astroid import Function, If, InferenceError

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages

import re

# regexp for ignored argument name
IGNORED_ARGUMENT_NAMES = re.compile('_.*')


def class_is_abstract(klass):
    """return true if the given class node should be considered as an abstract
    class
    """
    for attr in klass.values():
        if isinstance(attr, Function):
            if attr.is_abstract(pass_is_abstract=False):
                return True
    return False


MSGS = {
    'R0901': ('Too many ancestors (%s/%s)',
              'too-many-ancestors',
              'Used when class has too many parent classes, try to reduce \
              this to get a simpler (and so easier to use) class.'),
    'R0902': ('Too many instance attributes (%s/%s)',
              'too-many-instance-attributes',
              'Used when class has too many instance attributes, try to reduce \
              this to get a simpler (and so easier to use) class.'),
    'R0903': ('Too few public methods (%s/%s)',
              'too-few-public-methods',
              'Used when class has too few public methods, so be sure it\'s \
              really worth it.'),
    'R0904': ('Too many public methods (%s/%s)',
              'too-many-public-methods',
              'Used when class has too many public methods, try to reduce \
              this to get a simpler (and so easier to use) class.'),

    'R0911': ('Too many return statements (%s/%s)',
              'too-many-return-statements',
              'Used when a function or method has too many return statement, \
              making it hard to follow.'),
    'R0912': ('Too many branches (%s/%s)',
              'too-many-branches',
              'Used when a function or method has too many branches, \
              making it hard to follow.'),
    'R0913': ('Too many arguments (%s/%s)',
              'too-many-arguments',
              'Used when a function or method takes too many arguments.'),
    'R0914': ('Too many local variables (%s/%s)',
              'too-many-locals',
              'Used when a function or method has too many local variables.'),
    'R0915': ('Too many statements (%s/%s)',
              'too-many-statements',
              'Used when a function or method has too many statements. You \
              should then split it in smaller functions / methods.'),

    'R0921': ('Abstract class not referenced',
              'abstract-class-not-used',
              'Used when an abstract class is not used as ancestor anywhere.'),
    'R0922': ('Abstract class is only referenced %s times',
              'abstract-class-little-used',
              'Used when an abstract class is used less than X times as \
              ancestor.'),
    'R0923': ('Interface not implemented',
              'interface-not-implemented',
              'Used when an interface class is not implemented anywhere.'),
    }


class MisdesignChecker(BaseChecker):
    """checks for sign of poor/misdesign:
    * number of methods, attributes, local variables...
    * size, complexity of functions, methods
    """

    __implements__ = (IAstroidChecker,)

    # configuration section name
    name = 'design'
    # messages
    msgs = MSGS
    priority = -2
    # configuration options
    options = (('max-args',
                {'default' : 5, 'type' : 'int', 'metavar' : '<int>',
                 'help': 'Maximum number of arguments for function / method'}
                ),
               ('ignored-argument-names',
                {'default' : IGNORED_ARGUMENT_NAMES,
                 'type' :'regexp', 'metavar' : '<regexp>',
                 'help' : 'Argument names that match this expression will be '
                          'ignored. Default to name with leading underscore'}
                ),
               ('max-locals',
                {'default' : 15, 'type' : 'int', 'metavar' : '<int>',
                 'help': 'Maximum number of locals for function / method body'}
                ),
               ('max-returns',
                {'default' : 6, 'type' : 'int', 'metavar' : '<int>',
                 'help': 'Maximum number of return / yield for function / '
                         'method body'}
                ),
               ('max-branches',
                {'default' : 12, 'type' : 'int', 'metavar' : '<int>',
                 'help': 'Maximum number of branch for function / method body'}
                ),
               ('max-statements',
                {'default' : 50, 'type' : 'int', 'metavar' : '<int>',
                 'help': 'Maximum number of statements in function / method '
                         'body'}
                ),
               ('max-parents',
                {'default' : 7,
                 'type' : 'int',
                 'metavar' : '<num>',
                 'help' : 'Maximum number of parents for a class (see R0901).'}
                ),
               ('max-attributes',
                {'default' : 7,
                 'type' : 'int',
                 'metavar' : '<num>',
                 'help' : 'Maximum number of attributes for a class \
(see R0902).'}
                ),
               ('min-public-methods',
                {'default' : 2,
                 'type' : 'int',
                 'metavar' : '<num>',
                 'help' : 'Minimum number of public methods for a class \
(see R0903).'}
                ),
               ('max-public-methods',
                {'default' : 20,
                 'type' : 'int',
                 'metavar' : '<num>',
                 'help' : 'Maximum number of public methods for a class \
(see R0904).'}
                ),
               )

    def __init__(self, linter=None):
        BaseChecker.__init__(self, linter)
        self.stats = None
        self._returns = None
        self._branches = None
        self._used_abstracts = None
        self._used_ifaces = None
        self._abstracts = None
        self._ifaces = None
        self._stmts = 0

    def open(self):
        """initialize visit variables"""
        self.stats = self.linter.add_stats()
        self._returns = []
        self._branches = []
        self._used_abstracts = {}
        self._used_ifaces = {}
        self._abstracts = []
        self._ifaces = []

    # Check 'R0921', 'R0922', 'R0923'
    def close(self):
        """check that abstract/interface classes are used"""
        for abstract in self._abstracts:
            if not abstract in self._used_abstracts:
                self.add_message('abstract-class-not-used', node=abstract)
            elif self._used_abstracts[abstract] < 2:
                self.add_message('abstract-class-little-used', node=abstract,
                                 args=self._used_abstracts[abstract])
        for iface in self._ifaces:
            if not iface in self._used_ifaces:
                self.add_message('interface-not-implemented', node=iface)

    @check_messages('too-many-ancestors', 'too-many-instance-attributes',
                    'too-few-public-methods', 'too-many-public-methods',
                    'abstract-class-not-used', 'abstract-class-little-used',
                    'interface-not-implemented')
    def visit_class(self, node):
        """check size of inheritance hierarchy and number of instance attributes
        """
        self._inc_branch()
        # Is the total inheritance hierarchy is 7 or less?
        nb_parents = len(list(node.ancestors()))
        if nb_parents > self.config.max_parents:
            self.add_message('too-many-ancestors', node=node,
                             args=(nb_parents, self.config.max_parents))
        # Does the class contain less than 20 attributes for
        # non-GUI classes (40 for GUI)?
        # FIXME detect gui classes
        if len(node.instance_attrs) > self.config.max_attributes:
            self.add_message('too-many-instance-attributes', node=node,
                             args=(len(node.instance_attrs),
                                   self.config.max_attributes))
        # update abstract / interface classes structures
        if class_is_abstract(node):
            self._abstracts.append(node)
        elif node.type == 'interface' and node.name != 'Interface':
            self._ifaces.append(node)
            for parent in node.ancestors(False):
                if parent.name == 'Interface':
                    continue
                self._used_ifaces[parent] = 1
        try:
            for iface in node.interfaces():
                self._used_ifaces[iface] = 1
        except InferenceError:
            # XXX log ?
            pass
        for parent in node.ancestors():
            try:
                self._used_abstracts[parent] += 1
            except KeyError:
                self._used_abstracts[parent] = 1

    @check_messages('too-many-ancestors', 'too-many-instance-attributes',
                    'too-few-public-methods', 'too-many-public-methods',
                    'abstract-class-not-used', 'abstract-class-little-used',
                    'interface-not-implemented')
    def leave_class(self, node):
        """check number of public methods"""
        nb_public_methods = 0
        special_methods = set()
        for method in node.methods():
            if not method.name.startswith('_'):
                nb_public_methods += 1
            if method.name.startswith("__"):
                special_methods.add(method.name)
        # Does the class contain less than 20 public methods ?
        if nb_public_methods > self.config.max_public_methods:
            self.add_message('too-many-public-methods', node=node,
                             args=(nb_public_methods,
                                   self.config.max_public_methods))
        # stop here for exception, metaclass and interface classes
        if node.type != 'class':
            return
        # Does the class contain more than 5 public methods ?
        if nb_public_methods < self.config.min_public_methods:
            self.add_message('R0903', node=node,
                             args=(nb_public_methods,
                                   self.config.min_public_methods))

    @check_messages('too-many-return-statements', 'too-many-branches',
                    'too-many-arguments', 'too-many-locals', 'too-many-statements')
    def visit_function(self, node):
        """check function name, docstring, arguments, redefinition,
        variable names, max locals
        """
        self._inc_branch()
        # init branch and returns counters
        self._returns.append(0)
        self._branches.append(0)
        # check number of arguments
        args = node.args.args
        if args is not None:
            ignored_args_num = len(
                [arg for arg in args
                 if self.config.ignored_argument_names.match(arg.name)])
            argnum = len(args) - ignored_args_num
            if  argnum > self.config.max_args:
                self.add_message('too-many-arguments', node=node,
                                 args=(len(args), self.config.max_args))
        else:
            ignored_args_num = 0
        # check number of local variables
        locnum = len(node.locals) - ignored_args_num
        if locnum > self.config.max_locals:
            self.add_message('too-many-locals', node=node,
                             args=(locnum, self.config.max_locals))
        # init statements counter
        self._stmts = 1

    @check_messages('too-many-return-statements', 'too-many-branches', 'too-many-arguments', 'too-many-locals', 'too-many-statements')
    def leave_function(self, node):
        """most of the work is done here on close:
        checks for max returns, branch, return in __init__
        """
        returns = self._returns.pop()
        if returns > self.config.max_returns:
            self.add_message('too-many-return-statements', node=node,
                             args=(returns, self.config.max_returns))
        branches = self._branches.pop()
        if branches > self.config.max_branches:
            self.add_message('too-many-branches', node=node,
                             args=(branches, self.config.max_branches))
        # check number of statements
        if self._stmts > self.config.max_statements:
            self.add_message('too-many-statements', node=node,
                             args=(self._stmts, self.config.max_statements))

    def visit_return(self, _):
        """count number of returns"""
        if not self._returns:
            return # return outside function, reported by the base checker
        self._returns[-1] += 1

    def visit_default(self, node):
        """default visit method -> increments the statements counter if
        necessary
        """
        if node.is_statement:
            self._stmts += 1

    def visit_tryexcept(self, node):
        """increments the branches counter"""
        branches = len(node.handlers)
        if node.orelse:
            branches += 1
        self._inc_branch(branches)
        self._stmts += branches

    def visit_tryfinally(self, _):
        """increments the branches counter"""
        self._inc_branch(2)
        self._stmts += 2

    def visit_if(self, node):
        """increments the branches counter"""
        branches = 1
        # don't double count If nodes coming from some 'elif'
        if node.orelse and (len(node.orelse) > 1 or
                            not isinstance(node.orelse[0], If)):
            branches += 1
        self._inc_branch(branches)
        self._stmts += branches

    def visit_while(self, node):
        """increments the branches counter"""
        branches = 1
        if node.orelse:
            branches += 1
        self._inc_branch(branches)

    visit_for = visit_while

    def _inc_branch(self, branchesnum=1):
        """increments the branches counter"""
        branches = self._branches
        for i in xrange(len(branches)):
            branches[i] += branchesnum

    # FIXME: make a nice report...

def register(linter):
    """required method to auto register this checker """
    linter.register_checker(MisdesignChecker(linter))
