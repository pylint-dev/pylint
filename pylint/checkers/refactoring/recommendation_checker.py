# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import astroid

from pylint import checkers, interfaces
from pylint.checkers import utils


class RecommendationChecker(checkers.BaseChecker):

    __implements__ = (interfaces.IAstroidChecker,)
    name = "refactoring"
    msgs = {
        "C0200": (
            "Consider using enumerate instead of iterating with range and len",
            "consider-using-enumerate",
            "Emitted when code that iterates with range and len is "
            "encountered. Such code can be simplified by using the "
            "enumerate builtin.",
        ),
        "C0201": (
            "Consider iterating the dictionary directly instead of calling .keys()",
            "consider-iterating-dictionary",
            "Emitted when the keys of a dictionary are iterated through the .keys() "
            "method. It is enough to just iterate through the dictionary itself, as "
            'in "for key in dictionary".',
        ),
    }

    @staticmethod
    def _is_builtin(node, function):
        inferred = utils.safe_infer(node)
        if not inferred:
            return False
        return utils.is_builtin_object(inferred) and inferred.name == function

    @utils.check_messages("consider-iterating-dictionary")
    def visit_call(self, node):
        if not isinstance(node.func, astroid.Attribute):
            return
        if node.func.attrname != "keys":
            return
        if not isinstance(node.parent, (astroid.For, astroid.Comprehension)):
            return

        inferred = utils.safe_infer(node.func)
        if not isinstance(inferred, astroid.BoundMethod) or not isinstance(
            inferred.bound, astroid.Dict
        ):
            return

        if isinstance(node.parent, (astroid.For, astroid.Comprehension)):
            self.add_message("consider-iterating-dictionary", node=node)

    @utils.check_messages("consider-using-enumerate")
    def visit_for(self, node):
        """Emit a convention whenever range and len are used for indexing."""
        # Verify that we have a `range([start], len(...), [stop])` call and
        # that the object which is iterated is used as a subscript in the
        # body of the for.

        # Is it a proper range call?
        if not isinstance(node.iter, astroid.Call):
            return
        if not self._is_builtin(node.iter.func, "range"):
            return
        if not node.iter.args:
            return
        is_constant_zero = (
            isinstance(node.iter.args[0], astroid.Const)
            and node.iter.args[0].value == 0
        )
        if len(node.iter.args) == 2 and not is_constant_zero:
            return
        if len(node.iter.args) > 2:
            return

        # Is it a proper len call?
        if not isinstance(node.iter.args[-1], astroid.Call):
            return
        second_func = node.iter.args[-1].func
        if not self._is_builtin(second_func, "len"):
            return
        len_args = node.iter.args[-1].args
        if not len_args or len(len_args) != 1:
            return
        iterating_object = len_args[0]
        if not isinstance(iterating_object, astroid.Name):
            return
        # If we're defining __iter__ on self, enumerate won't work
        scope = node.scope()
        if iterating_object.name == "self" and scope.name == "__iter__":
            return

        # Verify that the body of the for loop uses a subscript
        # with the object that was iterated. This uses some heuristics
        # in order to make sure that the same object is used in the
        # for body.
        for child in node.body:
            for subscript in child.nodes_of_class(astroid.Subscript):
                if not isinstance(subscript.value, astroid.Name):
                    continue

                value = subscript.slice
                if isinstance(value, astroid.Index):
                    value = value.value
                if not isinstance(value, astroid.Name):
                    continue
                if value.name != node.target.name:
                    continue
                if iterating_object.name != subscript.value.name:
                    continue
                if subscript.value.scope() != node.scope():
                    # Ignore this subscript if it's not in the same
                    # scope. This means that in the body of the for
                    # loop, another scope was created, where the same
                    # name for the iterating object was used.
                    continue
                self.add_message("consider-using-enumerate", node=node)
                return
