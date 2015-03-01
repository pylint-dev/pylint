# Copyright (c) 2003-2014 LOGILAB S.A. (Paris, FRANCE).
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
"""classes checker for Python code
"""
from __future__ import generators

import sys
from collections import defaultdict

import astroid
from astroid import YES, Instance, are_exclusive, AssAttr, Class
from astroid.bases import Generator, BUILTINS
from astroid.inference import InferenceContext

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import (
    PYMETHODS, overrides_a_method, check_messages, is_attr_private,
    is_attr_protected, node_frame_class, safe_infer, is_builtin_object,
    decorated_with_property, unimplemented_abstract_methods)
import six

if sys.version_info >= (3, 0):
    NEXT_METHOD = '__next__'
else:
    NEXT_METHOD = 'next'
ITER_METHODS = ('__iter__', '__getitem__')

def _called_in_methods(func, klass, methods):
    """ Check if the func was called in any of the given methods,
    belonging to the *klass*. Returns True if so, False otherwise.
    """
    if not isinstance(func, astroid.Function):
        return False
    for method in methods:
        try:
            infered = klass.getattr(method)
        except astroid.NotFoundError:
            continue
        for infer_method in infered:
            for callfunc in infer_method.nodes_of_class(astroid.CallFunc):
                try:
                    bound = next(callfunc.func.infer())
                except (astroid.InferenceError, StopIteration):
                    continue
                if not isinstance(bound, astroid.BoundMethod):
                    continue
                func_obj = bound._proxied
                if isinstance(func_obj, astroid.UnboundMethod):
                    func_obj = func_obj._proxied
                if func_obj.name == func.name:
                    return True
    return False

def class_is_abstract(node):
    """return true if the given class node should be considered as an abstract
    class
    """
    for method in node.methods():
        if method.parent.frame() is node:
            if method.is_abstract(pass_is_abstract=False):
                return True
    return False

def _is_attribute_property(name, klass):
    """ Check if the given attribute *name* is a property
    in the given *klass*.

    It will look for `property` calls or for functions
    with the given name, decorated by `property` or `property`
    subclasses.
    Returns ``True`` if the name is a property in the given klass,
    ``False`` otherwise.
    """

    try:
        attributes = klass.getattr(name)
    except astroid.NotFoundError:
        return False
    property_name = "{0}.property".format(BUILTINS)
    for attr in attributes:
        try:
            infered = next(attr.infer())
        except astroid.InferenceError:
            continue
        if (isinstance(infered, astroid.Function) and
                decorated_with_property(infered)):
            return True
        if infered.pytype() == property_name:
            return True
    return False


MSGS = {
    'F0202': ('Unable to check methods signature (%s / %s)',
              'method-check-failed',
              'Used when Pylint has been unable to check methods signature '
              'compatibility for an unexpected reason. Please report this kind '
              'if you don\'t make sense of it.'),

    'E0202': ('An attribute defined in %s line %s hides this method',
              'method-hidden',
              'Used when a class defines a method which is hidden by an '
              'instance attribute from an ancestor class or set by some '
              'client code.'),
    'E0203': ('Access to member %r before its definition line %s',
              'access-member-before-definition',
              'Used when an instance member is accessed before it\'s actually '
              'assigned.'),
    'W0201': ('Attribute %r defined outside __init__',
              'attribute-defined-outside-init',
              'Used when an instance attribute is defined outside the __init__ '
              'method.'),

    'W0212': ('Access to a protected member %s of a client class', # E0214
              'protected-access',
              'Used when a protected member (i.e. class member with a name '
              'beginning with an underscore) is access outside the class or a '
              'descendant of the class where it\'s defined.'),

    'E0211': ('Method has no argument',
              'no-method-argument',
              'Used when a method which should have the bound instance as '
              'first argument has no argument defined.'),
    'E0213': ('Method should have "self" as first argument',
              'no-self-argument',
              'Used when a method has an attribute different the "self" as '
              'first argument. This is considered as an error since this is '
              'a so common convention that you shouldn\'t break it!'),
    'C0202': ('Class method %s should have %s as first argument',
              'bad-classmethod-argument',
              'Used when a class method has a first argument named differently '
              'than the value specified in valid-classmethod-first-arg option '
              '(default to "cls"), recommended to easily differentiate them '
              'from regular instance methods.'),
    'C0203': ('Metaclass method %s should have %s as first argument',
              'bad-mcs-method-argument',
              'Used when a metaclass method has a first agument named '
              'differently than the value specified in valid-classmethod-first'
              '-arg option (default to "cls"), recommended to easily '
              'differentiate them from regular instance methods.'),
    'C0204': ('Metaclass class method %s should have %s as first argument',
              'bad-mcs-classmethod-argument',
              'Used when a metaclass class method has a first argument named '
              'differently than the value specified in valid-metaclass-'
              'classmethod-first-arg option (default to "mcs"), recommended to '
              'easily differentiate them from regular instance methods.'),

    'W0211': ('Static method with %r as first argument',
              'bad-staticmethod-argument',
              'Used when a static method has "self" or a value specified in '
              'valid-classmethod-first-arg option or '
              'valid-metaclass-classmethod-first-arg option as first argument.'
             ),
    'R0201': ('Method could be a function',
              'no-self-use',
              'Used when a method doesn\'t use its bound instance, and so could '
              'be written as a function.'
             ),

    'E0221': ('Interface resolved to %s is not a class',
              'interface-is-not-class',
              'Used when a class claims to implement an interface which is not '
              'a class.'),
    'E0222': ('Missing method %r from %s interface',
              'missing-interface-method',
              'Used when a method declared in an interface is missing from a '
              'class implementing this interface'),
    'W0221': ('Arguments number differs from %s %r method',
              'arguments-differ',
              'Used when a method has a different number of arguments than in '
              'the implemented interface or in an overridden method.'),
    'W0222': ('Signature differs from %s %r method',
              'signature-differs',
              'Used when a method signature is different than in the '
              'implemented interface or in an overridden method.'),
    'W0223': ('Method %r is abstract in class %r but is not overridden',
              'abstract-method',
              'Used when an abstract method (i.e. raise NotImplementedError) is '
              'not overridden in concrete class.'
             ),
    'F0220': ('failed to resolve interfaces implemented by %s (%s)',
              'unresolved-interface',
              'Used when a Pylint as failed to find interfaces implemented by '
              ' a class'),


    'W0231': ('__init__ method from base class %r is not called',
              'super-init-not-called',
              'Used when an ancestor class method has an __init__ method '
              'which is not called by a derived class.'),
    'W0232': ('Class has no __init__ method',
              'no-init',
              'Used when a class has no __init__ method, neither its parent '
              'classes.'),
    'W0233': ('__init__ method from a non direct base class %r is called',
              'non-parent-init-called',
              'Used when an __init__ method is called on a class which is not '
              'in the direct ancestors for the analysed class.'),
    'W0234': ('__iter__ returns non-iterator',
              'non-iterator-returned',
              'Used when an __iter__ method returns something which is not an '
               'iterable (i.e. has no `%s` method)' % NEXT_METHOD),
    'E0235': ('__exit__ must accept 3 arguments: type, value, traceback',
              'bad-context-manager',
              'Used when the __exit__ special method, belonging to a '
              'context manager, does not accept 3 arguments '
              '(type, value, traceback).'),
    'E0236': ('Invalid object %r in __slots__, must contain '
              'only non empty strings',
              'invalid-slots-object',
              'Used when an invalid (non-string) object occurs in __slots__.'),
    'E0237': ('Assigning to attribute %r not defined in class slots',
              'assigning-non-slot',
              'Used when assigning to an attribute not defined '
              'in the class slots.'),
    'E0238': ('Invalid __slots__ object',
              'invalid-slots',
              'Used when an invalid __slots__ is found in class. '
              'Only a string, an iterable or a sequence is permitted.'),
    'E0239': ('Inheriting %r, which is not a class.',
              'inherit-non-class',
              'Used when a class inherits from something which is not a '
              'class.'),


    }


class ClassChecker(BaseChecker):
    """checks for :
    * methods without self as first argument
    * overridden methods signature
    * access only to existent members via self
    * attributes not defined in the __init__ method
    * supported interfaces implementation
    * unreachable code
    """

    __implements__ = (IAstroidChecker,)

    # configuration section name
    name = 'classes'
    # messages
    msgs = MSGS
    priority = -2
    # configuration options
    options = (('ignore-iface-methods',
                {'default' : (#zope interface
                    'isImplementedBy', 'deferred', 'extends', 'names',
                    'namesAndDescriptions', 'queryDescriptionFor', 'getBases',
                    'getDescriptionFor', 'getDoc', 'getName', 'getTaggedValue',
                    'getTaggedValueTags', 'isEqualOrExtendedBy', 'setTaggedValue',
                    'isImplementedByInstancesOf',
                    # twisted
                    'adaptWith',
                    # logilab.common interface
                    'is_implemented_by'),
                 'type' : 'csv',
                 'metavar' : '<method names>',
                 'help' : 'List of interface methods to ignore, \
separated by a comma. This is used for instance to not check methods defines \
in Zope\'s Interface base class.'}
               ),
               ('defining-attr-methods',
                {'default' : ('__init__', '__new__', 'setUp'),
                 'type' : 'csv',
                 'metavar' : '<method names>',
                 'help' : 'List of method names used to declare (i.e. assign) \
instance attributes.'}
               ),
               ('valid-classmethod-first-arg',
                {'default' : ('cls',),
                 'type' : 'csv',
                 'metavar' : '<argument names>',
                 'help' : 'List of valid names for the first argument in \
a class method.'}
               ),
               ('valid-metaclass-classmethod-first-arg',
                {'default' : ('mcs',),
                 'type' : 'csv',
                 'metavar' : '<argument names>',
                 'help' : 'List of valid names for the first argument in \
a metaclass class method.'}
               ),
               ('exclude-protected',
                {
                    'default': (
                        # namedtuple public API.
                        '_asdict', '_fields', '_replace', '_source', '_make'),
                    'type': 'csv',
                    'metavar': '<protected access exclusions>',
                    'help': ('List of member names, which should be excluded '
                             'from the protected access warning.')}
               ))

    def __init__(self, linter=None):
        BaseChecker.__init__(self, linter)
        self._accessed = []
        self._first_attrs = []
        self._meth_could_be_func = None

    def visit_class(self, node):
        """init visit variable _accessed and check interfaces
        """
        self._accessed.append(defaultdict(list))
        self._check_bases_classes(node)
        self._check_interfaces(node)
        # if not an interface, exception, metaclass
        if node.type == 'class':
            try:
                node.local_attr('__init__')
            except astroid.NotFoundError:
                self.add_message('no-init', args=node, node=node)
        self._check_slots(node)
        self._check_proper_bases(node)

    @check_messages('inherit-non-class')
    def _check_proper_bases(self, node):
        """
        Detect that a class inherits something which is not
        a class or a type.
        """
        for base in node.bases:
            ancestor = safe_infer(base)
            if ancestor in (YES, None):
                continue
            if (isinstance(ancestor, astroid.Instance) and
                    ancestor.is_subtype_of('%s.type' % (BUILTINS,))):
                continue
            if not isinstance(ancestor, astroid.Class):
                self.add_message('inherit-non-class',
                                 args=base.as_string(), node=node)

    @check_messages('access-member-before-definition',
                    'attribute-defined-outside-init')
    def leave_class(self, cnode):
        """close a class node:
        check that instance attributes are defined in __init__ and check
        access to existent members
        """
        # check access to existent members on non metaclass classes
        accessed = self._accessed.pop()
        if cnode.type != 'metaclass':
            self._check_accessed_members(cnode, accessed)
        # checks attributes are defined in an allowed method such as __init__
        if not self.linter.is_message_enabled('attribute-defined-outside-init'):
            return
        defining_methods = self.config.defining_attr_methods
        current_module = cnode.root()
        for attr, nodes in six.iteritems(cnode.instance_attrs):
            # skip nodes which are not in the current module and it may screw up
            # the output, while it's not worth it
            nodes = [n for n in nodes if not
                     isinstance(n.statement(), (astroid.Delete, astroid.AugAssign))
                     and n.root() is current_module]
            if not nodes:
                continue # error detected by typechecking
            # check if any method attr is defined in is a defining method
            if any(node.frame().name in defining_methods
                   for node in nodes):
                continue

            # check attribute is defined in a parent's __init__
            for parent in cnode.instance_attr_ancestors(attr):
                attr_defined = False
                # check if any parent method attr is defined in is a defining method
                for node in parent.instance_attrs[attr]:
                    if node.frame().name in defining_methods:
                        attr_defined = True
                if attr_defined:
                    # we're done :)
                    break
            else:
                # check attribute is defined as a class attribute
                try:
                    cnode.local_attr(attr)
                except astroid.NotFoundError:
                    for node in nodes:
                        if node.frame().name not in defining_methods:
                            # If the attribute was set by a callfunc in any
                            # of the defining methods, then don't emit
                            # the warning.
                            if _called_in_methods(node.frame(), cnode,
                                                  defining_methods):
                                continue
                            self.add_message('attribute-defined-outside-init',
                                             args=attr, node=node)

    def visit_function(self, node):
        """check method arguments, overriding"""
        # ignore actual functions
        if not node.is_method():
            return
        klass = node.parent.frame()
        self._meth_could_be_func = True
        # check first argument is self if this is actually a method
        self._check_first_arg_for_type(node, klass.type == 'metaclass')
        if node.name == '__init__':
            self._check_init(node)
            return
        # check signature if the method overloads inherited method
        for overridden in klass.local_attr_ancestors(node.name):
            # get astroid for the searched method
            try:
                meth_node = overridden[node.name]
            except KeyError:
                # we have found the method but it's not in the local
                # dictionary.
                # This may happen with astroid build from living objects
                continue
            if not isinstance(meth_node, astroid.Function):
                continue
            self._check_signature(node, meth_node, 'overridden')
            break
        if node.decorators:
            for decorator in node.decorators.nodes:
                if isinstance(decorator, astroid.Getattr) and \
                        decorator.attrname in ('getter', 'setter', 'deleter'):
                    # attribute affectation will call this method, not hiding it
                    return
                if isinstance(decorator, astroid.Name) and decorator.name == 'property':
                    # attribute affectation will either call a setter or raise
                    # an attribute error, anyway not hiding the function
                    return
        # check if the method is hidden by an attribute
        try:
            overridden = klass.instance_attr(node.name)[0] # XXX
            overridden_frame = overridden.frame()
            if (isinstance(overridden_frame, astroid.Function)
                    and overridden_frame.type == 'method'):
                overridden_frame = overridden_frame.parent.frame()
            if (isinstance(overridden_frame, Class)
                    and klass.is_subtype_of(overridden_frame.qname())):
                args = (overridden.root().name, overridden.fromlineno)
                self.add_message('method-hidden', args=args, node=node)
        except astroid.NotFoundError:
            pass

        # check non-iterators in __iter__
        if node.name == '__iter__':
            self._check_iter(node)
        elif node.name == '__exit__':
            self._check_exit(node)

    def _check_slots(self, node):
        if '__slots__' not in node.locals:
            return
        for slots in node.igetattr('__slots__'):
            # check if __slots__ is a valid type
            for meth in ITER_METHODS:
                try:
                    slots.getattr(meth)
                    break
                except astroid.NotFoundError:
                    continue
            else:
                self.add_message('invalid-slots', node=node)
                continue

            if isinstance(slots, astroid.Const):
                # a string, ignore the following checks
                continue
            if not hasattr(slots, 'itered'):
                # we can't obtain the values, maybe a .deque?
                continue

            if isinstance(slots, astroid.Dict):
                values = [item[0] for item in slots.items]
            else:
                values = slots.itered()
            if values is YES:
                return

            for elt in values:
                try:
                    self._check_slots_elt(elt)
                except astroid.InferenceError:
                    continue

    def _check_slots_elt(self, elt):
        for infered in elt.infer():
            if infered is YES:
                continue
            if (not isinstance(infered, astroid.Const) or
                    not isinstance(infered.value, six.string_types)):
                self.add_message('invalid-slots-object',
                                 args=infered.as_string(),
                                 node=elt)
                continue
            if not infered.value:
                self.add_message('invalid-slots-object',
                                 args=infered.as_string(),
                                 node=elt)

    def _check_iter(self, node):
        try:
            infered = node.infer_call_result(node)
        except astroid.InferenceError:
            return

        for infered_node in infered:
            if (infered_node is YES
                    or isinstance(infered_node, Generator)):
                continue
            if isinstance(infered_node, astroid.Instance):
                try:
                    infered_node.local_attr(NEXT_METHOD)
                except astroid.NotFoundError:
                    self.add_message('non-iterator-returned',
                                     node=node)
                    break

    def _check_exit(self, node):
        positional = sum(1 for arg in node.args.args if arg.name != 'self')
        if positional < 3 and not node.args.vararg:
            self.add_message('bad-context-manager',
                             node=node)
        elif positional > 3:
            self.add_message('bad-context-manager',
                             node=node)

    def leave_function(self, node):
        """on method node, check if this method couldn't be a function

        ignore class, static and abstract methods, initializer,
        methods overridden from a parent class and any
        kind of method defined in an interface for this warning
        """
        if node.is_method():
            if node.args.args is not None:
                self._first_attrs.pop()
            if not self.linter.is_message_enabled('no-self-use'):
                return
            class_node = node.parent.frame()
            if (self._meth_could_be_func and node.type == 'method'
                    and not node.name in PYMETHODS
                    and not (node.is_abstract() or
                             overrides_a_method(class_node, node.name))
                    and class_node.type != 'interface'):
                self.add_message('no-self-use', node=node)

    def visit_getattr(self, node):
        """check if the getattr is an access to a class member
        if so, register it. Also check for access to protected
        class member from outside its class (but ignore __special__
        methods)
        """
        attrname = node.attrname
        # Check self
        if self.is_first_attr(node):
            self._accessed[-1][attrname].append(node)
            return
        if not self.linter.is_message_enabled('protected-access'):
            return

        self._check_protected_attribute_access(node)

    def visit_assattr(self, node):
        if isinstance(node.ass_type(), astroid.AugAssign) and self.is_first_attr(node):
            self._accessed[-1][node.attrname].append(node)
        self._check_in_slots(node)

    def _check_in_slots(self, node):
        """ Check that the given assattr node
        is defined in the class slots.
        """
        infered = safe_infer(node.expr)
        if infered and isinstance(infered, Instance):
            klass = infered._proxied
            if '__slots__' not in klass.locals or not klass.newstyle:
                return

            slots = klass.slots()
            if slots is None:
                return
            # If any ancestor doesn't use slots, the slots
            # defined for this class are superfluous.
            if any('__slots__' not in ancestor.locals and
                   ancestor.name != 'object'
                   for ancestor in klass.ancestors()):
                return

            if not any(slot.value == node.attrname for slot in slots):
                # If we have a '__dict__' in slots, then
                # assigning any name is valid.
                if not any(slot.value == '__dict__' for slot in slots):
                    if _is_attribute_property(node.attrname, klass):
                        # Properties circumvent the slots mechanism,
                        # so we should not emit a warning for them.
                        return
                    self.add_message('assigning-non-slot',
                                     args=(node.attrname, ), node=node)

    @check_messages('protected-access')
    def visit_assign(self, assign_node):
        node = assign_node.targets[0]
        if not isinstance(node, AssAttr):
            return

        if self.is_first_attr(node):
            return

        self._check_protected_attribute_access(node)

    def _check_protected_attribute_access(self, node):
        '''Given an attribute access node (set or get), check if attribute
        access is legitimate. Call _check_first_attr with node before calling
        this method. Valid cases are:
        * self._attr in a method or cls._attr in a classmethod. Checked by
        _check_first_attr.
        * Klass._attr inside "Klass" class.
        * Klass2._attr inside "Klass" class when Klass2 is a base class of
            Klass.
        '''
        attrname = node.attrname

        if (is_attr_protected(attrname) and
                attrname not in self.config.exclude_protected):

            klass = node_frame_class(node)

            # XXX infer to be more safe and less dirty ??
            # in classes, check we are not getting a parent method
            # through the class object or through super
            callee = node.expr.as_string()

            # We are not in a class, no remaining valid case
            if klass is None:
                self.add_message('protected-access', node=node, args=attrname)
                return

            # If the expression begins with a call to super, that's ok.
            if isinstance(node.expr, astroid.CallFunc) and \
               isinstance(node.expr.func, astroid.Name) and \
               node.expr.func.name == 'super':
                return

            # We are in a class, one remaining valid cases, Klass._attr inside
            # Klass
            if not (callee == klass.name or callee in klass.basenames):
                # Detect property assignments in the body of the class.
                # This is acceptable:
                #
                # class A:
                #     b = property(lambda: self._b)

                stmt = node.parent.statement()
                try:
                    if (isinstance(stmt, astroid.Assign) and
                            (stmt in klass.body or klass.parent_of(stmt)) and
                            isinstance(stmt.value, astroid.CallFunc) and
                            isinstance(stmt.value.func, astroid.Name) and
                            stmt.value.func.name == 'property' and
                            is_builtin_object(next(stmt.value.func.infer(), None))):
                        return
                except astroid.InferenceError:
                    pass
                self.add_message('protected-access', node=node, args=attrname)

    def visit_name(self, node):
        """check if the name handle an access to a class member
        if so, register it
        """
        if self._first_attrs and (node.name == self._first_attrs[-1] or
                                  not self._first_attrs[-1]):
            self._meth_could_be_func = False

    def _check_accessed_members(self, node, accessed):
        """check that accessed members are defined"""
        # XXX refactor, probably much simpler now that E0201 is in type checker
        for attr, nodes in six.iteritems(accessed):
            # deactivate "except doesn't do anything", that's expected
            # pylint: disable=W0704
            try:
                # is it a class attribute ?
                node.local_attr(attr)
                # yes, stop here
                continue
            except astroid.NotFoundError:
                pass
            # is it an instance attribute of a parent class ?
            try:
                next(node.instance_attr_ancestors(attr))
                # yes, stop here
                continue
            except StopIteration:
                pass
            # is it an instance attribute ?
            try:
                defstmts = node.instance_attr(attr)
            except astroid.NotFoundError:
                pass
            else:
                # filter out augment assignment nodes
                defstmts = [stmt for stmt in defstmts if stmt not in nodes]
                if not defstmts:
                    # only augment assignment for this node, no-member should be
                    # triggered by the typecheck checker
                    continue
                # filter defstmts to only pick the first one when there are
                # several assignments in the same scope
                scope = defstmts[0].scope()
                defstmts = [stmt for i, stmt in enumerate(defstmts)
                            if i == 0 or stmt.scope() is not scope]
                # if there are still more than one, don't attempt to be smarter
                # than we can be
                if len(defstmts) == 1:
                    defstmt = defstmts[0]
                    # check that if the node is accessed in the same method as
                    # it's defined, it's accessed after the initial assignment
                    frame = defstmt.frame()
                    lno = defstmt.fromlineno
                    for _node in nodes:
                        if _node.frame() is frame and _node.fromlineno < lno \
                           and not are_exclusive(_node.statement(), defstmt,
                                                 ('AttributeError', 'Exception', 'BaseException')):
                            self.add_message('access-member-before-definition',
                                             node=_node, args=(attr, lno))

    def _check_first_arg_for_type(self, node, metaclass=0):
        """check the name of first argument, expect:

        * 'self' for a regular method
        * 'cls' for a class method or a metaclass regular method (actually
          valid-classmethod-first-arg value)
        * 'mcs' for a metaclass class method (actually
          valid-metaclass-classmethod-first-arg)
        * not one of the above for a static method
        """
        # don't care about functions with unknown argument (builtins)
        if node.args.args is None:
            return
        first_arg = node.args.args and node.argnames()[0]
        self._first_attrs.append(first_arg)
        first = self._first_attrs[-1]
        # static method
        if node.type == 'staticmethod':
            if (first_arg == 'self' or
                    first_arg in self.config.valid_classmethod_first_arg or
                    first_arg in self.config.valid_metaclass_classmethod_first_arg):
                self.add_message('bad-staticmethod-argument', args=first, node=node)
                return
            self._first_attrs[-1] = None
        # class / regular method with no args
        elif not node.args.args:
            self.add_message('no-method-argument', node=node)
        # metaclass
        elif metaclass:
            # metaclass __new__ or classmethod
            if node.type == 'classmethod':
                self._check_first_arg_config(
                    first,
                    self.config.valid_metaclass_classmethod_first_arg, node,
                    'bad-mcs-classmethod-argument', node.name)
            # metaclass regular method
            else:
                self._check_first_arg_config(
                    first,
                    self.config.valid_classmethod_first_arg, node,
                    'bad-mcs-method-argument',
                    node.name)
        # regular class
        else:
            # class method
            if node.type == 'classmethod':
                self._check_first_arg_config(
                    first,
                    self.config.valid_classmethod_first_arg, node,
                    'bad-classmethod-argument',
                    node.name)
            # regular method without self as argument
            elif first != 'self':
                self.add_message('no-self-argument', node=node)

    def _check_first_arg_config(self, first, config, node, message,
                                method_name):
        if first not in config:
            if len(config) == 1:
                valid = repr(config[0])
            else:
                valid = ', '.join(repr(v) for v in config[:-1])
                valid = '%s or %r' % (valid, config[-1])
            self.add_message(message, args=(method_name, valid), node=node)

    def _check_bases_classes(self, node):
        """check that the given class node implements abstract methods from
        base classes
        """
        def is_abstract(method):
            return method.is_abstract(pass_is_abstract=False)

        # check if this class abstract
        if class_is_abstract(node):
            return

        methods = sorted(
            unimplemented_abstract_methods(node, is_abstract).items(),
            key=lambda item: item[0],
        )
        for name, method in methods:
            owner = method.parent.frame()
            if owner is node:
                continue
            # owner is not this class, it must be a parent class
            # check that the ancestor's method is not abstract
            if name in node.locals:
                # it is redefined as an attribute or with a descriptor
                continue
            self.add_message('abstract-method', node=node,
                             args=(name, owner.name))

    def _check_interfaces(self, node):
        """check that the given class node really implements declared
        interfaces
        """
        e0221_hack = [False]
        def iface_handler(obj):
            """filter interface objects, it should be classes"""
            if not isinstance(obj, astroid.Class):
                e0221_hack[0] = True
                self.add_message('interface-is-not-class', node=node,
                                 args=(obj.as_string(),))
                return False
            return True
        ignore_iface_methods = self.config.ignore_iface_methods
        try:
            for iface in node.interfaces(handler_func=iface_handler):
                for imethod in iface.methods():
                    name = imethod.name
                    if name.startswith('_') or name in ignore_iface_methods:
                        # don't check method beginning with an underscore,
                        # usually belonging to the interface implementation
                        continue
                    # get class method astroid
                    try:
                        method = node_method(node, name)
                    except astroid.NotFoundError:
                        self.add_message('missing-interface-method',
                                         args=(name, iface.name),
                                         node=node)
                        continue
                    # ignore inherited methods
                    if method.parent.frame() is not node:
                        continue
                    # check signature
                    self._check_signature(method, imethod,
                                          '%s interface' % iface.name)
        except astroid.InferenceError:
            if e0221_hack[0]:
                return
            implements = Instance(node).getattr('__implements__')[0]
            assignment = implements.parent
            assert isinstance(assignment, astroid.Assign)
            # assignment.expr can be a Name or a Tuple or whatever.
            # Use as_string() for the message
            # FIXME: in case of multiple interfaces, find which one could not
            #        be resolved
            self.add_message('unresolved-interface', node=implements,
                             args=(node.name, assignment.value.as_string()))

    def _check_init(self, node):
        """check that the __init__ method call super or ancestors'__init__
        method
        """
        if (not self.linter.is_message_enabled('super-init-not-called') and
                not self.linter.is_message_enabled('non-parent-init-called')):
            return
        klass_node = node.parent.frame()
        to_call = _ancestors_to_call(klass_node)
        not_called_yet = dict(to_call)
        for stmt in node.nodes_of_class(astroid.CallFunc):
            expr = stmt.func
            if not isinstance(expr, astroid.Getattr) \
                   or expr.attrname != '__init__':
                continue
            # skip the test if using super
            if isinstance(expr.expr, astroid.CallFunc) and \
                   isinstance(expr.expr.func, astroid.Name) and \
               expr.expr.func.name == 'super':
                return
            try:
                for klass in expr.expr.infer():
                    if klass is YES:
                        continue
                    # The infered klass can be super(), which was
                    # assigned to a variable and the `__init__`
                    # was called later.
                    #
                    # base = super()
                    # base.__init__(...)

                    if (isinstance(klass, astroid.Instance) and
                            isinstance(klass._proxied, astroid.Class) and
                            is_builtin_object(klass._proxied) and
                            klass._proxied.name == 'super'):
                        return
                    try:
                        del not_called_yet[klass]
                    except KeyError:
                        if klass not in to_call:
                            self.add_message('non-parent-init-called',
                                             node=expr, args=klass.name)
            except astroid.InferenceError:
                continue
        for klass, method in six.iteritems(not_called_yet):
            if klass.name == 'object' or method.parent.name == 'object':
                continue
            self.add_message('super-init-not-called', args=klass.name, node=node)

    def _check_signature(self, method1, refmethod, class_type):
        """check that the signature of the two given methods match

        class_type is in 'class', 'interface'
        """
        if not (isinstance(method1, astroid.Function)
                and isinstance(refmethod, astroid.Function)):
            self.add_message('method-check-failed',
                             args=(method1, refmethod), node=method1)
            return
        # don't care about functions with unknown argument (builtins)
        if method1.args.args is None or refmethod.args.args is None:
            return
        # if we use *args, **kwargs, skip the below checks
        if method1.args.vararg or method1.args.kwarg:
            return
        if is_attr_private(method1.name):
            return
        if len(method1.args.args) != len(refmethod.args.args):
            self.add_message('arguments-differ',
                             args=(class_type, method1.name),
                             node=method1)
        elif len(method1.args.defaults) < len(refmethod.args.defaults):
            self.add_message('signature-differs',
                             args=(class_type, method1.name),
                             node=method1)

    def is_first_attr(self, node):
        """Check that attribute lookup name use first attribute variable name
        (self for method, cls for classmethod and mcs for metaclass).
        """
        return self._first_attrs and isinstance(node.expr, astroid.Name) and \
                   node.expr.name == self._first_attrs[-1]

def _ancestors_to_call(klass_node, method='__init__'):
    """return a dictionary where keys are the list of base classes providing
    the queried method, and so that should/may be called from the method node
    """
    to_call = {}
    for base_node in klass_node.ancestors(recurs=False):
        try:
            to_call[base_node] = next(base_node.igetattr(method))
        except astroid.InferenceError:
            continue
    return to_call


def node_method(node, method_name):
    """get astroid for <method_name> on the given class node, ensuring it
    is a Function node
    """
    for n in node.local_attr(method_name):
        if isinstance(n, astroid.Function):
            return n
    raise astroid.NotFoundError(method_name)

def register(linter):
    """required method to auto register this checker """
    linter.register_checker(ClassChecker(linter))
