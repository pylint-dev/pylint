# -*- coding: utf-8 -*-
# Copyright (c) 2016 Moisés López <moylop260@vauxoo.com>
# Copyright (c) 2016 Claudiu Popa <pcmanticore@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Looks for code which can be refactored."""

import collections

import astroid
from astroid import decorators
import six

from pylint import interfaces
from pylint import checkers
from pylint import utils as lint_utils
from pylint.checkers import utils


class RefactoringChecker(checkers.BaseTokenChecker):
    """Looks for code which can be refactored

    This checker also mixes the astroid and the token approaches
    in order to create knowledge about whether a "else if" node
    is a true "else if" node, or a "elif" node.
    """

    __implements__ = (interfaces.ITokenChecker, interfaces.IAstroidChecker)

    name = 'refactoring'

    msgs = {
        'R1701': ("Consider merging these isinstance calls to isinstance(%s, (%s))",
                  "consider-merging-isinstance",
                  "Usen when multiple consecutive isinstance calls can be merged into one."),
        'R1702': ('Too many nested blocks (%s/%s)',
                  'too-many-nested-blocks',
                  'Used when a function or a method has too many nested '
                  'blocks. This makes the code less understandable and '
                  'maintainable.',
                  {'old_names': [('R0101', 'too-many-nested-blocks')]}),
        'R1703': ('The if statement can be replaced with %s',
                  'simplifiable-if-statement',
                  'Used when an if statement can be replaced with '
                  '\'bool(test)\'. ',
                  {'old_names': [('R0102', 'simplifiable-if-statement')]}),
        'R1704': ('Redefining argument with the local name %r',
                  'redefined-argument-from-local',
                  'Used when a local name is redefining an argument, which might '
                  'suggest a potential error. This is taken in account only for '
                  'a handful of name binding operations, such as for iteration, '
                  'with statement assignment and exception handler assignment.'
                 )
    }
    options = (('max-nested-blocks',
                {'default': 5, 'type': 'int', 'metavar': '<int>',
                 'help': 'Maximum number of nested blocks for function / '
                         'method body'}
               ),)

    priority = 0

    def __init__(self, linter=None):
        checkers.BaseTokenChecker.__init__(self, linter)
        self._init()

    def _init(self):
        self._nested_blocks = []
        self._elifs = []
        self._if_counter = 0
        self._nested_blocks_msg = None

    @decorators.cachedproperty
    def _dummy_rgx(self):
        return lint_utils.get_global_option(
            self, 'dummy-variables-rgx', default=None)

    @staticmethod
    def _is_bool_const(node):
        return (isinstance(node.value, astroid.Const)
                and isinstance(node.value.value, bool))

    def _is_actual_elif(self, node):
        """Check if the given node is an actual elif

        This is a problem we're having with the builtin ast module,
        which splits `elif` branches into a separate if statement.
        Unfortunately we need to know the exact type in certain
        cases.
        """

        if isinstance(node.parent, astroid.If):
            orelse = node.parent.orelse
            # current if node must directly follow a "else"
            if orelse and orelse == [node]:
                if self._elifs[self._if_counter]:
                    return True
        return False

    def _check_simplifiable_if(self, node):
        """Check if the given if node can be simplified.

        The if statement can be reduced to a boolean expression
        in some cases. For instance, if there are two branches
        and both of them return a boolean value that depends on
        the result of the statement's test, then this can be reduced
        to `bool(test)` without losing any functionality.
        """

        if self._is_actual_elif(node):
            # Not interested in if statements with multiple branches.
            return
        if len(node.orelse) != 1 or len(node.body) != 1:
            return

        # Check if both branches can be reduced.
        first_branch = node.body[0]
        else_branch = node.orelse[0]
        if isinstance(first_branch, astroid.Return):
            if not isinstance(else_branch, astroid.Return):
                return
            first_branch_is_bool = self._is_bool_const(first_branch)
            else_branch_is_bool = self._is_bool_const(else_branch)
            reduced_to = "'return bool(test)'"
        elif isinstance(first_branch, astroid.Assign):
            if not isinstance(else_branch, astroid.Assign):
                return
            first_branch_is_bool = self._is_bool_const(first_branch)
            else_branch_is_bool = self._is_bool_const(else_branch)
            reduced_to = "'var = bool(test)'"
        else:
            return

        if not first_branch_is_bool or not else_branch_is_bool:
            return
        if not first_branch.value.value:
            # This is a case that can't be easily simplified and
            # if it can be simplified, it will usually result in a
            # code that's harder to understand and comprehend.
            # Let's take for instance `arg and arg <= 3`. This could theoretically be
            # reduced to `not arg or arg > 3`, but the net result is that now the
            # condition is harder to understand, because it requires understanding of
            # an extra clause:
            #   * first, there is the negation of truthness with `not arg`
            #   * the second clause is `arg > 3`, which occurs when arg has a
            #     a truth value, but it implies that `arg > 3` is equivalent
            #     with `arg and arg > 3`, which means that the user must
            #     think about this assumption when evaluating `arg > 3`.
            #     The original form is easier to grasp.
            return

        self.add_message('simplifiable-if-statement', node=node,
                         args=(reduced_to,))

    def process_tokens(self, tokens):
        # Process tokens and look for 'if' or 'elif'
        for _, token, _, _, _ in tokens:
            if token == 'elif':
                self._elifs.append(True)
            elif token == 'if':
                self._elifs.append(False)

    def leave_module(self, _):
        self._init()

    @utils.check_messages('too-many-nested-blocks')
    def visit_tryexcept(self, node):
        self._check_nested_blocks(node)

    visit_tryfinally = visit_tryexcept
    visit_while = visit_tryexcept

    def _check_redefined_argument_from_local(self, name_node):
        if self._dummy_rgx and self._dummy_rgx.match(name_node.name):
            return
        if not name_node.lineno:
            # Unknown position, maybe it is a manually built AST?
            return

        scope = name_node.scope()
        if not isinstance(scope, astroid.FunctionDef):
            return

        for defined_argument in scope.args.nodes_of_class(astroid.AssignName):
            if defined_argument.name == name_node.name:
                self.add_message('redefined-argument-from-local',
                                 node=name_node,
                                 args=(name_node.name, ))

    @utils.check_messages('redefined-argument-from-local',
                          'too-many-nested-blocks')
    def visit_for(self, node):
        self._check_nested_blocks(node)

        for name in node.target.nodes_of_class(astroid.AssignName):
            self._check_redefined_argument_from_local(name)

    @utils.check_messages('redefined-argument-from-local')
    def visit_excepthandler(self, node):
        if node.name and isinstance(node.name, astroid.AssignName):
            self._check_redefined_argument_from_local(node.name)

    @utils.check_messages('redefined-argument-from-local')
    def visit_with(self, node):
        for _, names in node.items:
            if not names:
                continue
            for name in names.nodes_of_class(astroid.AssignName):
                self._check_redefined_argument_from_local(name)

    def visit_ifexp(self, _):
        self._if_counter += 1

    def visit_comprehension(self, node):
        self._if_counter += len(node.ifs)

    @utils.check_messages('too-many-nested-blocks', 'simplifiable-if-statement')
    def visit_if(self, node):
        self._check_simplifiable_if(node)
        self._check_nested_blocks(node)
        self._if_counter += 1

    @utils.check_messages('too-many-nested-blocks')
    def leave_functiondef(self, _):
        # new scope = reinitialize the stack of nested blocks
        self._nested_blocks = []
        # if there is a waiting message left, send it
        if self._nested_blocks_msg:
            self.add_message('too-many-nested-blocks',
                             node=self._nested_blocks_msg[0],
                             args=self._nested_blocks_msg[1])
            self._nested_blocks_msg = None

    def _check_nested_blocks(self, node):
        """Update and check the number of nested blocks
        """
        # only check block levels inside functions or methods
        if not isinstance(node.scope(), astroid.FunctionDef):
            return
        # messages are triggered on leaving the nested block. Here we save the
        # stack in case the current node isn't nested in the previous one
        nested_blocks = self._nested_blocks[:]
        if node.parent == node.scope():
            self._nested_blocks = [node]
        else:
            # go through ancestors from the most nested to the less
            for ancestor_node in reversed(self._nested_blocks):
                if ancestor_node == node.parent:
                    break
                self._nested_blocks.pop()
            # if the node is a elif, this should not be another nesting level
            if isinstance(node, astroid.If) and self._elifs[self._if_counter]:
                if self._nested_blocks:
                    self._nested_blocks.pop()
            self._nested_blocks.append(node)
        # send message only once per group of nested blocks
        if len(nested_blocks) > self.config.max_nested_blocks:
            if len(nested_blocks) > len(self._nested_blocks):
                self.add_message('too-many-nested-blocks', node=nested_blocks[0],
                                 args=(len(nested_blocks),
                                       self.config.max_nested_blocks))
                self._nested_blocks_msg = None
            else:
                # if time has not come yet to send the message (ie the stack of
                # nested nodes is still increasing), save it in case the
                # current node is the last one of the function
                self._nested_blocks_msg = (self._nested_blocks[0],
                                           (len(self._nested_blocks),
                                            self.config.max_nested_blocks))

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
    __implements__ = (interfaces.IAstroidChecker,)
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
    skipped_nodes = (astroid.Set,)
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
