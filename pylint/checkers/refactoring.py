# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Looks for code which can be refactored."""

import astroid

from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages, is_builtin_object, safe_infer



class RefactoringChecker(BaseChecker):
    """Looks for code which can be refactored.
    """

    __implements__ = (IAstroidChecker,)

    # configuration section name
    name = 'refactoring'

    msgs = {
        'R1701': (
            "Consider merging these isinstance calls to isinstance(%s, (%s))",
            "consider-merging-isinstance",
            "Usen when multiple isinstance calls can be grouped into one."),
    }
    priority = -2

    @staticmethod
    def _first_args_duplicated(node):
        """Get the objects, as strings, from the *isinstance* calls,
        found in the BoolOp node.
        :param astroid.BoolOp node: Node to get first argument of values
        :returns: First arguments duplicated as string of all `node.values` and
            parameters as string. E.g. {'var1': ['objx', 'objy'], 'var2': ['objz']}
        :rtype: dict
        """
        first_args = {}
        duplicated = []
        for value in node.values:
            if not isinstance(value, astroid.Call) or len(value.args) != 2:
                continue
            inferred = safe_infer(value.func)
            if not inferred or not is_builtin_object(inferred):
                continue
            if inferred.name == 'isinstance':
                first_arg = value.args[0].as_string()
                if first_arg in first_args:
                    duplicated.append(first_arg)
                else:
                    first_args[first_arg] = set()
                if isinstance(value.args[1], astroid.Tuple):
                    first_args[first_arg].update([
                        class_type.as_string() for class_type in value.args[1].itered()])
                else:
                    first_args[first_arg].add(value.args[1].as_string())
        # Remove all keys not duplicated
        for key in list(first_args):
            if key not in duplicated:
                first_args.pop(key)
            else:
                first_args[key] = list(first_args[key])
                first_args[key].sort()
        return first_args

    @check_messages('consider-merging-isinstance')
    def visit_boolop(self, node):
        "Check isinstance calls which can be merged together."
        if node.op != 'or':
            return
        first_args = self._first_args_duplicated(node)
        for duplicated_name, class_names in first_args.items():
            self.add_message(
                'consider-merging-isinstance', node=node,
                args=(duplicated_name, ', '.join([name for name in class_names])))


def register(linter):
    """required method to auto register this checker """
    linter.register_checker(RefactoringChecker(linter))
