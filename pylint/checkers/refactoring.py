# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Looks for code which can be refactored."""

import collections

import astroid

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages, is_builtin_object, safe_infer


def duplicated(items):
    items_counter = collections.Counter(items)
    return [item for item, counter in items_counter.items() if counter > 1]


class RefactoringChecker(BaseChecker):
    """Looks for code which can be refactored.
    """

    __implements__ = (IAstroidChecker,)

    # configuration section name
    name = 'refactoring'

    msgs = {
        'R1701': (
            "Consider merging these isinstance calls to %s.",
            "consider-merging-isinstance",
            "Usen when multiple isinstance calls can be grouped into one."),
    }
    priority = -2

    @staticmethod
    def first_args(node):
        # TODO: Remove after fix https://github.com/PyCQA/pylint/issues/984
        # pylint: disable=redundant-returns-doc
        """Get the objects, as strings, from the *isinstance* calls,
        found in the BoolOp node.
        :param astroid.BoolOp node: Node to get first argument of values
        :returns: First arguments as string of all `node.values`
        :rtype: generator
        """
        for value in node.values:
            if not isinstance(value, astroid.Call) or not value.args:
                continue
            inferred = safe_infer(value.func)
            if not inferred or not is_builtin_object(inferred):
                continue
            if inferred.name == 'isinstance':
                yield value.args[0].as_string()

    @check_messages('consider-merging-isinstance')
    def visit_boolop(self, node):
        "Check isinstance calls which can be merged together."
        if node.op != 'or':
            return
        for duplicated_name in duplicated(self.first_args(node)):
            self.add_message('consider-merging-isinstance', node=node,
                             args=(duplicated_name,))


def register(linter):
    """required method to auto register this checker """
    linter.register_checker(RefactoringChecker(linter))
