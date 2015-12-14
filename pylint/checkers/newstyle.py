# Copyright (c) 2005-2014 LOGILAB S.A. (Paris, FRANCE).
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
"""check for new / old style related problems
"""
import sys

import astroid

from pylint.interfaces import IAstroidChecker, INFERENCE, INFERENCE_FAILURE, HIGH
from pylint.checkers import BaseChecker
from pylint.checkers.utils import (
    check_messages,
    node_frame_class,
    has_known_bases
)

MSGS = {
    'E1001': ('Use of __slots__ on an old style class',
              'slots-on-old-class',
              'Used when an old style class uses the __slots__ attribute.',
              {'maxversion': (3, 0)}),
    'E1002': ('Use of super on an old style class',
              'super-on-old-class',
              'Used when an old style class uses the super builtin.',
              {'maxversion': (3, 0)}),
    'E1003': ('Bad first argument %r given to super()',
              'bad-super-call',
              'Used when another argument than the current class is given as \
              first argument of the super builtin.'),
    'E1004': ('Missing argument to super()',
              'missing-super-argument',
              'Used when the super builtin didn\'t receive an \
               argument.',
              {'maxversion': (3, 0)}),
    'W1001': ('Use of "property" on an old style class',
              'property-on-old-class',
              'Used when Pylint detect the use of the builtin "property" \
              on an old style class while this is relying on new style \
              classes features.',
              {'maxversion': (3, 0)}),
    'C1001': ('Old-style class defined.',
              'old-style-class',
              'Used when a class is defined that does not inherit from another'
              'class and does not inherit explicitly from "object".',
              {'maxversion': (3, 0)})
    }


class NewStyleConflictChecker(BaseChecker):
    """checks for usage of new style capabilities on old style classes and
    other new/old styles conflicts problems
    * use of property, __slots__, super
    * "super" usage
    """

    __implements__ = (IAstroidChecker,)

    # configuration section name
    name = 'newstyle'
    # messages
    msgs = MSGS
    priority = -2
    # configuration options
    options = ()

    @check_messages('slots-on-old-class', 'old-style-class')
    def visit_classdef(self, node):
        """ Check __slots__ in old style classes and old
        style class definition.
        """
        if '__slots__' in node and not node.newstyle:
            confidence = (INFERENCE if has_known_bases(node)
                          else INFERENCE_FAILURE)
            self.add_message('slots-on-old-class', node=node,
                             confidence=confidence)
        # The node type could be class, exception, metaclass, or
        # interface.  Presumably, the non-class-type nodes would always
        # have an explicit base class anyway.
        if not node.bases and node.type == 'class' and not node.metaclass():
            # We use confidence HIGH here because this message should only ever
            # be emitted for classes at the root of the inheritance hierarchyself.
            self.add_message('old-style-class', node=node, confidence=HIGH)

    @check_messages('property-on-old-class')
    def visit_call(self, node):
        """check property usage"""
        parent = node.parent.frame()
        if (isinstance(parent, astroid.ClassDef) and
                not parent.newstyle and
                isinstance(node.func, astroid.Name)):
            confidence = (INFERENCE if has_known_bases(parent)
                          else INFERENCE_FAILURE)
            name = node.func.name
            if name == 'property':
                self.add_message('property-on-old-class', node=node,
                                 confidence=confidence)

    @check_messages('super-on-old-class', 'bad-super-call', 'missing-super-argument')
    def visit_functiondef(self, node):
        """check use of super"""
        # ignore actual functions or method within a new style class
        if not node.is_method():
            return
        klass = node.parent.frame()
        for stmt in node.nodes_of_class(astroid.Call):
            if node_frame_class(stmt) != node_frame_class(node):
                # Don't look down in other scopes.
                continue
            expr = stmt.func
            if not isinstance(expr, astroid.Attribute):
                continue
            call = expr.expr
            # skip the test if using super
            if not (isinstance(call, astroid.Call) and
                    isinstance(call.func, astroid.Name) and
                    call.func.name == 'super'):
                continue

            if not klass.newstyle and has_known_bases(klass):
                # super should not be used on an old style class
                self.add_message('super-on-old-class', node=node)
            else:
                # super first arg should be the class
                if not call.args and sys.version_info[0] == 3:
                    # unless Python 3
                    continue

                try:
                    supcls = (call.args and next(call.args[0].infer())
                              or None)
                except astroid.InferenceError:
                    continue

                if supcls is None:
                    self.add_message('missing-super-argument', node=call)
                    continue

                if klass is not supcls:
                    name = None
                    # if supcls is not YES, then supcls was infered
                    # and use its name. Otherwise, try to look
                    # for call.args[0].name
                    if supcls is not astroid.YES:
                        name = supcls.name
                    else:
                        if hasattr(call.args[0], 'name'):
                            name = call.args[0].name
                    if name is not None:
                        self.add_message('bad-super-call', node=call, args=(name, ))


def register(linter):
    """required method to auto register this checker """
    linter.register_checker(NewStyleConflictChecker(linter))
