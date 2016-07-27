# -*- coding: utf-8 -*-
# Copyright (c) 2016 Moisés López <moylop260@vauxoo.com>
# Copyright (c) 2016 Claudiu Popa <pcmanticore@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Looks for code which can be refactored."""

import collections

import astroid
import six

from pylint import interfaces
from pylint import checkers
from pylint.checkers import utils



class RefactoringChecker(checkers.BaseChecker):
    """Looks for code which can be refactored."""

    __implements__ = (interfaces.IAstroidChecker,)

    name = 'refactoring'

    msgs = {
        'R1701': (
            "Consider merging these isinstance calls to isinstance(%s, (%s))",
            "consider-merging-isinstance",
            "Usen when multiple consecutive isinstance calls can be merged into one."),
    }
    priority = 0

    @staticmethod
    def _duplicated_isinstance_types(node):
        """Get the duplicated types from the underlying isinstance calls.

        :param astroid.BoolOp node: Node which should contain a bunch of isinstance calls.
        :returns: Dictionary of the comparison objects from the isinstance calls,
                  to duplicate values from consecutive calls.
        :rtype: dict
        """
        duplicated_objects = set()
        all_types = collections.defaultdict(set)

        for call in node.values:
            if not isinstance(call, astroid.Call) or len(call.args) != 2:
                continue

            inferred = utils.safe_infer(call.func)
            if not inferred or not utils.is_builtin_object(inferred):
                continue

            if inferred.name != 'isinstance':
                continue

            isinstance_object = call.args[0].as_string()
            isinstance_types = call.args[1]

            if isinstance_object in all_types:
                duplicated_objects.add(isinstance_object)

            if isinstance(isinstance_types, astroid.Tuple):
                elems = [class_type.as_string() for class_type in isinstance_types.itered()]
            else:
                elems = [isinstance_types.as_string()]
            all_types[isinstance_object].update(elems)

        # Remove all keys which not duplicated
        return {key: value for key, value in all_types.items()
                if key in duplicated_objects}

    @utils.check_messages('consider-merging-isinstance')
    def visit_boolop(self, node):
        '''Check isinstance calls which can be merged together.'''
        if node.op != 'or':
            return

        first_args = self._duplicated_isinstance_types(node)
        for duplicated_name, class_names in first_args.items():
            names = sorted(name for name in class_names)
            self.add_message('consider-merging-isinstance',
                             node=node,
                             args=(duplicated_name, ', '.join(names)))


class RecommandationChecker(checkers.BaseChecker):
    __implements__ = (interfaces.IAstroidChecker, )
    name = 'refactoring'
    msgs = {'C0200': ('Consider using enumerate instead of iterating with range and len',
                      'consider-using-enumerate',
                      'Emitted when code that iterates with range and len is '
                      'encountered. Such code can be simplified by using the '
                      'enumerate builtin.'),
            'C0201': ('Consider iterating the dictionary directly instead of calling .keys()',
                      'consider-iterating-dictionary',
                      'Emitted when the keys of a dictionary are iterated through the .keys() '
                      'method. It is enough to just iterate through the dictionary itself, as '
                      'in "for key in dictionary".'),
           }

    @staticmethod
    def _is_builtin(node, function):
        inferred = utils.safe_infer(node)
        if not inferred:
            return False
        return utils.is_builtin_object(inferred) and inferred.name == function

    @utils.check_messages('consider-iterating-dictionary')
    def visit_call(self, node):
        inferred = utils.safe_infer(node.func)
        if not inferred:
            return

        if not isinstance(inferred, astroid.BoundMethod):
            return
        if not isinstance(inferred.bound, astroid.Dict) or inferred.name != 'keys':
            return

        # Check if the statement is what we're expecting to have.
        statement = node.statement()
        if isinstance(statement, astroid.Expr):
            statement = statement.value

        if isinstance(statement, astroid.For) or utils.is_comprehension(statement):
            self.add_message('consider-iterating-dictionary', node=node)

    @utils.check_messages('consider-using-enumerate')
    def visit_for(self, node):
        """Emit a convention whenever range and len are used for indexing."""
        # Verify that we have a `range(len(...))` call and that the object
        # which is iterated is used as a subscript in the body of the for.

        # Is it a proper range call?
        if not isinstance(node.iter, astroid.Call):
            return
        if not self._is_builtin(node.iter.func, 'range'):
            return
        if len(node.iter.args) != 1:
            return

        # Is it a proper len call?
        if not isinstance(node.iter.args[0], astroid.Call):
            return
        second_func = node.iter.args[0].func
        if not self._is_builtin(second_func, 'len'):
            return
        len_args = node.iter.args[0].args
        if not len_args or len(len_args) != 1:
            return
        iterating_object = len_args[0]
        if not isinstance(iterating_object, astroid.Name):
            return

        # Verify that the body of the for loop uses a subscript
        # with the object that was iterated. This uses some heuristics
        # in order to make sure that the same object is used in the
        # for body.
        for child in node.body:
            for subscript in child.nodes_of_class(astroid.Subscript):
                if not isinstance(subscript.value, astroid.Name):
                    continue
                if not isinstance(subscript.slice, astroid.Index):
                    continue
                if not isinstance(subscript.slice.value, astroid.Name):
                    continue
                if subscript.slice.value.name != node.target.name:
                    continue
                if iterating_object.name != subscript.value.name:
                    continue
                if subscript.value.scope() != node.scope():
                    # Ignore this subscript if it's not in the same
                    # scope. This means that in the body of the for
                    # loop, another scope was created, where the same
                    # name for the iterating object was used.
                    continue
                self.add_message('consider-using-enumerate', node=node)
                return


class NotChecker(checkers.BaseChecker):
    """checks for too many not in comparison expressions

    - "not not" should trigger a warning
    - "not" followed by a comparison should trigger a warning
    """
    __implements__ = (interfaces.IAstroidChecker,)
    msgs = {'C0113': ('Consider changing "%s" to "%s"',
                      'unneeded-not',
                      'Used when a boolean expression contains an unneeded '
                      'negation.'),
           }
    name = 'basic'
    reverse_op = {'<': '>=', '<=': '>', '>': '<=', '>=': '<', '==': '!=',
                  '!=': '==', 'in': 'not in', 'is': 'is not'}
    # sets are not ordered, so for example "not set(LEFT_VALS) <= set(RIGHT_VALS)" is
    # not equivalent to "set(LEFT_VALS) > set(RIGHT_VALS)"
    skipped_nodes = (astroid.Set, )
    # 'builtins' py3, '__builtin__' py2
    skipped_classnames = ['%s.%s' % (six.moves.builtins.__name__, qname)
                          for qname in ('set', 'frozenset')]

    @utils.check_messages('unneeded-not')
    def visit_unaryop(self, node):
        if node.op != 'not':
            return
        operand = node.operand

        if isinstance(operand, astroid.UnaryOp) and operand.op == 'not':
            self.add_message('unneeded-not', node=node,
                             args=(node.as_string(),
                                   operand.operand.as_string()))
        elif isinstance(operand, astroid.Compare):
            left = operand.left
            # ignore multiple comparisons
            if len(operand.ops) > 1:
                return
            operator, right = operand.ops[0]
            if operator not in self.reverse_op:
                return
            # Ignore __ne__ as function of __eq__
            frame = node.frame()
            if frame.name == '__ne__' and operator == '==':
                return
            for _type in (utils.node_type(left), utils.node_type(right)):
                if not _type:
                    return
                if isinstance(_type, self.skipped_nodes):
                    return
                if (isinstance(_type, astroid.Instance) and
                        _type.qname() in self.skipped_classnames):
                    return
            suggestion = '%s %s %s' % (left.as_string(),
                                       self.reverse_op[operator],
                                       right.as_string())
            self.add_message('unneeded-not', node=node,
                             args=(node.as_string(), suggestion))



def register(linter):
    """Required method to auto register this checker."""
    linter.register_checker(RefactoringChecker(linter))
    linter.register_checker(NotChecker(linter))
    linter.register_checker(RecommandationChecker(linter))
