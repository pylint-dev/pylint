# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE
import re
from typing import cast

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
        "C0206": (
            "Consider iterating with .items()",
            "consider-using-dict-items",
            "Emitted when iterating over the keys of a dictionary and accessing the "
            "value by index lookup."
            "Both the key and value can be accessed by iterating using the .items() "
            "method of the dictionary instead.",
        ),
        "C0207": (
            "Consider using %s[%d] instead",
            "consider-using-str-partition",
            "Emitted when accessing only the first or last element of a str.split(sep). "
            "The first and last element can be accessed by using str.partition(sep)[0] "
            "or str.rpartition(sep)[-1] instead, which is less computationally "
            "expensive.",
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

    @utils.check_messages("consider-using-enumerate", "consider-using-dict-items")
    def visit_for(self, node: astroid.For) -> None:
        self._check_consider_using_enumerate(node)
        self._check_consider_using_dict_items(node)

    def _check_consider_using_enumerate(self, node: astroid.For) -> None:
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

    def _check_consider_using_dict_items(self, node: astroid.For) -> None:
        """Add message when accessing dict values by index lookup."""
        # Verify that we have a .keys() call and
        # that the object which is iterated is used as a subscript in the
        # body of the for.

        iterating_object_name = utils.get_iterating_dictionary_name(node)
        if iterating_object_name is None:
            return

        # Verify that the body of the for loop uses a subscript
        # with the object that was iterated. This uses some heuristics
        # in order to make sure that the same object is used in the
        # for body.
        for child in node.body:
            for subscript in child.nodes_of_class(astroid.Subscript):
                subscript = cast(astroid.Subscript, subscript)

                if not isinstance(subscript.value, (astroid.Name, astroid.Attribute)):
                    continue

                value = subscript.slice
                if isinstance(value, astroid.Index):
                    value = value.value
                if (
                    not isinstance(value, astroid.Name)
                    or value.name != node.target.name
                    or iterating_object_name != subscript.value.as_string()
                ):
                    continue
                last_definition_lineno = value.lookup(value.name)[1][-1].lineno
                if last_definition_lineno > node.lineno:
                    # Ignore this subscript if it has been redefined after
                    # the for loop. This checks for the line number using .lookup()
                    # to get the line number where the iterating object was last
                    # defined and compare that to the for loop's line number
                    continue
                if (
                    isinstance(subscript.parent, astroid.Assign)
                    and subscript in subscript.parent.targets
                    or isinstance(subscript.parent, astroid.AugAssign)
                    and subscript == subscript.parent.target
                ):
                    # Ignore this subscript if it is the target of an assignment
                    continue

                self.add_message("consider-using-dict-items", node=node)
                return

    @utils.check_messages("consider-using-dict-items")
    def visit_comprehension(self, node: astroid.Comprehension) -> None:
        iterating_object_name = utils.get_iterating_dictionary_name(node)
        if iterating_object_name is None:
            return

        children = list(node.parent.get_children())
        if node.ifs:
            children.extend(node.ifs)
        for child in children:
            for subscript in child.nodes_of_class(astroid.Subscript):
                subscript = cast(astroid.Subscript, subscript)

                if not isinstance(subscript.value, (astroid.Name, astroid.Attribute)):
                    continue

                value = subscript.slice
                if isinstance(value, astroid.Index):
                    value = value.value
                if (
                    not isinstance(value, astroid.Name)
                    or value.name != node.target.name
                    or iterating_object_name != subscript.value.as_string()
                ):
                    continue

                self.add_message("consider-using-dict-items", node=node)
                return

    @utils.check_messages("consider-using-str-partition")
    def visit_subscript(self, node: astroid.Subscript) -> None:
        """Add message when accessing first or last elements of a str.split()."""
        assignment = None
        subscripted_object = node.value
        if isinstance(subscripted_object, astroid.Name):
            # Check assignment of this subscripted object
            assignment_lookup_results = node.value.lookup(node.value.name)
            if (
                len(assignment_lookup_results) == 0
                or len(assignment_lookup_results[-1]) == 0
            ):
                return
            assign_name = assignment_lookup_results[-1][-1]
            if not isinstance(assign_name, astroid.AssignName):
                return
            assignment = assign_name.parent
            if not isinstance(assignment, astroid.Assign):
                return
            # Set subscripted_object to the assignment RHS
            subscripted_object = assignment.value

        if isinstance(subscripted_object, astroid.Call):
            # Check if call is .split() or .rsplit()
            if isinstance(
                subscripted_object.func, astroid.Attribute
            ) and subscripted_object.func.attrname in ["split", "rsplit"]:
                inferred = utils.safe_infer(subscripted_object.func)
                if not isinstance(inferred, astroid.BoundMethod):
                    return

                # Check if subscript is 1 or -1
                value = node.slice
                if isinstance(value, astroid.Index):
                    value = value.value

                if isinstance(value, (astroid.UnaryOp, astroid.Const)):
                    const = utils.safe_infer(value)
                    const = cast(astroid.Const, const)
                    p = re.compile(
                        r"tilpsr*\."
                    )  # Match and replace in reverse to ensure last occurance replaced
                    if const.value == -1:
                        help_text = p.sub(
                            ".rpartition"[::-1],
                            subscripted_object.as_string()[::-1],
                            count=1,
                        )[::-1]
                        self.add_message(
                            "consider-using-str-partition",
                            node=node,
                            args=(help_text, -1),
                        )
                    elif const.value == 0:
                        help_text = p.sub(
                            ".partition"[::-1],
                            subscripted_object.as_string()[::-1],
                            count=1,
                        )[::-1]
                        self.add_message(
                            "consider-using-str-partition",
                            node=node,
                            args=(help_text, 0),
                        )
                # Check if subscript is len(split) - 1
                if (
                    isinstance(value, astroid.BinOp)
                    and value.left.func.name == "len"
                    and value.op == "-"
                    and value.right.value == 1
                    and assignment is not None
                ):
                    # Ensure that the len() is from builtins, not user re-defined
                    inferred_fn = utils.safe_infer(value.left.func)
                    if not (
                        isinstance(inferred_fn, astroid.FunctionDef)
                        and isinstance(inferred_fn.parent, astroid.Module)
                        and inferred_fn.parent.name == "builtins"
                    ):
                        return

                    # Further check for argument within len(), and compare that to object being split
                    arg_within_len = value.left.args[0].name
                    if arg_within_len == node.value.name:
                        p = re.compile(
                            r"tilpsr*\."
                        )  # Match and replace in reverse to ensure last occurance replaced
                        help_text = p.sub(
                            ".rpartition"[::-1],
                            subscripted_object.as_string()[::-1],
                            count=1,
                        )[::-1]
                        self.add_message(
                            "consider-using-str-partition",
                            node=node,
                            args=(help_text, -1),
                        )
