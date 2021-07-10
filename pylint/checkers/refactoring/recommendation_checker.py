# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
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
            "value by index lookup. "
            "Both the key and value can be accessed by iterating using the .items() "
            "method of the dictionary instead.",
        ),
        "C0207": (
            "Use %s instead",
            "use-maxsplit-arg",
            "Emitted when accessing only the first or last element of str.split(). "
            "The first and last element can be accessed by using "
            "str.split(sep, maxsplit=1)[0] or str.rsplit(sep, maxsplit=1)[-1] "
            "instead.",
        ),
    }

    @staticmethod
    def _is_builtin(node, function):
        inferred = utils.safe_infer(node)
        if not inferred:
            return False
        return utils.is_builtin_object(inferred) and inferred.name == function

    @utils.check_messages("consider-iterating-dictionary", "use-maxsplit-arg")
    def visit_call(self, node: astroid.Call) -> None:
        self._check_consider_iterating_dictionary(node)
        self._check_use_maxsplit_arg(node)

    def _check_consider_iterating_dictionary(self, node: astroid.Call) -> None:
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

    def _check_use_maxsplit_arg(self, node: astroid.Call) -> None:
        """Add message when accessing first or last elements of a str.split() or str.rsplit()."""

        # Check if call is split() or rsplit()
        if not (
            isinstance(node.func, astroid.Attribute)
            and node.func.attrname in ("split", "rsplit")
            and isinstance(utils.safe_infer(node.func), astroid.BoundMethod)
        ):
            return

        try:
            utils.get_argument_from_call(node, 0, "sep")
        except utils.NoSuchArgumentError:
            return

        try:
            # Ignore if maxsplit arg has been set
            utils.get_argument_from_call(node, 1, "maxsplit")
            return
        except utils.NoSuchArgumentError:
            pass

        if isinstance(node.parent, astroid.Subscript):
            try:
                subscript_value = utils.get_subscript_const_value(node.parent).value
            except utils.InferredTypeError:
                return

            # Check for cases where variable (Name) subscripts may be mutated within a loop
            if isinstance(node.parent.slice, astroid.Name):
                # Check if loop present within the scope of the node
                scope = node.scope()
                for loop_node in scope.nodes_of_class((astroid.For, astroid.While)):
                    loop_node = cast(astroid.node_classes.NodeNG, loop_node)
                    if not loop_node.parent_of(node):
                        continue

                    # Check if var is mutated within loop (Assign/AugAssign)
                    for assignment_node in loop_node.nodes_of_class(astroid.AugAssign):
                        assignment_node = cast(astroid.AugAssign, assignment_node)
                        if node.parent.slice.name == assignment_node.target.name:
                            return
                    for assignment_node in loop_node.nodes_of_class(astroid.Assign):
                        assignment_node = cast(astroid.Assign, assignment_node)
                        if node.parent.slice.name in [
                            n.name for n in assignment_node.targets
                        ]:
                            return

            if subscript_value in (-1, 0):
                fn_name = node.func.attrname
                new_fn = "rsplit" if subscript_value == -1 else "split"
                new_name = (
                    node.func.as_string().rsplit(fn_name, maxsplit=1)[0]
                    + new_fn
                    + f"({node.args[0].as_string()}, maxsplit=1)[{subscript_value}]"
                )
                self.add_message("use-maxsplit-arg", node=node, args=(new_name,))

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
        if isinstance(iterating_object, astroid.Name):
            expected_subscript_val_type = astroid.Name
        elif isinstance(iterating_object, astroid.Attribute):
            expected_subscript_val_type = astroid.Attribute
        else:
            return
        # If we're defining __iter__ on self, enumerate won't work
        scope = node.scope()
        if (
            isinstance(iterating_object, astroid.Name)
            and iterating_object.name == "self"
            and scope.name == "__iter__"
        ):
            return

        # Verify that the body of the for loop uses a subscript
        # with the object that was iterated. This uses some heuristics
        # in order to make sure that the same object is used in the
        # for body.
        for child in node.body:
            for subscript in child.nodes_of_class(astroid.Subscript):
                subscript = cast(astroid.Subscript, subscript)
                if not isinstance(subscript.value, expected_subscript_val_type):
                    continue

                value = subscript.slice
                if not isinstance(value, astroid.Name):
                    continue
                if subscript.value.scope() != node.scope():
                    # Ignore this subscript if it's not in the same
                    # scope. This means that in the body of the for
                    # loop, another scope was created, where the same
                    # name for the iterating object was used.
                    continue
                if value.name == node.target.name and (
                    isinstance(subscript.value, astroid.Name)
                    and iterating_object.name == subscript.value.name
                    or isinstance(subscript.value, astroid.Attribute)
                    and iterating_object.attrname == subscript.value.attrname
                ):
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
                    # Early termination as dict index lookup is necessary
                    return

                self.add_message("consider-using-dict-items", node=node)
                return

    @utils.check_messages("consider-using-dict-items")
    def visit_comprehension(self, node: astroid.Comprehension) -> None:
        iterating_object_name = utils.get_iterating_dictionary_name(node)
        if iterating_object_name is None:
            return

        for child in node.parent.get_children():
            for subscript in child.nodes_of_class(astroid.Subscript):
                subscript = cast(astroid.Subscript, subscript)

                if not isinstance(subscript.value, (astroid.Name, astroid.Attribute)):
                    continue

                value = subscript.slice
                if (
                    not isinstance(value, astroid.Name)
                    or value.name != node.target.name
                    or iterating_object_name != subscript.value.as_string()
                ):
                    continue

                self.add_message("consider-using-dict-items", node=node)
                return
