# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE
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
            "Consider using %s instead",
            "consider-using-str-partition",
            "Emitted when accessing only the first or last element of a str.split(sep). "
            "Or when a str.split(sep,maxsplit=1) is used. "
            "The first and last element can be accessed by using str.partition(sep)[0] "
            "or str.rpartition(sep)[-1] instead, which is less computationally "
            "expensive and works the same as str.split() or str.rsplit() with a maxsplit "
            "of 1",
        ),
    }

    @staticmethod
    def _is_builtin(node, function):
        inferred = utils.safe_infer(node)
        if not inferred:
            return False
        return utils.is_builtin_object(inferred) and inferred.name == function

    @utils.check_messages(
        "consider-iterating-dictionary", "consider-using-str-partition"
    )
    def visit_call(self, node: astroid.Call) -> None:
        self._check_consider_iterating_dictionary(node)
        self._check_consider_using_str_partition(node)

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

    def _check_consider_using_str_partition(self, node: astroid.Call) -> None:
        """Add message when accessing first or last elements of a str.split() or str.rsplit(),
        or when split/rsplit with max_split=1 is used"""

        # Check if call is split() or rsplit()
        if isinstance(node.func, astroid.Attribute) and node.func.attrname in (
            "split",
            "rsplit",
        ):
            inferred_func = utils.safe_infer(node.func)
            fn_name = node.func.attrname
            node_name = node.as_string()

            if not isinstance(inferred_func, astroid.BoundMethod):
                return

            try:
                seperator = utils.get_argument_from_call(node, 0, "sep").value
            except utils.NoSuchArgumentError:
                return
            # Check if maxsplit is set, and if it's == 1 (this can be replaced by partition)
            try:
                maxsplit = utils.get_argument_from_call(node, 1, "maxsplit").value
                if maxsplit == 1:
                    self.add_message(
                        "consider-using-str-partition",
                        node=node,
                        args=(
                            f"{node.func.expr.as_string()}.{node.func.attrname.replace('split','partition')}('{seperator}')"
                        ),
                    )
                return

            except utils.NoSuchArgumentError:
                pass

            # Check if it's immediately subscripted
            if isinstance(node.parent, astroid.Subscript):
                subscript_node = node.parent
                # Check if subscripted with -1/0
                if not isinstance(
                    subscript_node.slice, (astroid.Const, astroid.UnaryOp)
                ):
                    return
                subscript_value = utils.safe_infer(subscript_node.slice)
                subscript_value = cast(astroid.Const, subscript_value)
                subscript_value = subscript_value.value
                if subscript_value in (-1, 0):
                    new_fn = "rpartition" if subscript_value == -1 else "partition"
                    new_fn = new_fn[::-1]
                    node_name = node_name[::-1]
                    fn_name = fn_name[::-1]
                    new_name = node_name.replace(fn_name, new_fn, 1)[::-1]
                    self.add_message(
                        "consider-using-str-partition", node=node, args=(new_name,)
                    )
                    return
            # Check where name it's assigned to, then check all usage of name
            assign_target = None
            if isinstance(node.parent, astroid.Tuple):
                assign_node = node.parent.parent
                if not isinstance(assign_node, astroid.Assign):
                    return
                idx = node.parent.elts.index(node)
                if not isinstance(assign_node.targets[0], astroid.Tuple):
                    return
                assign_target = assign_node.targets[0].elts[idx]
            elif isinstance(node.parent, astroid.Assign):
                assign_target = node.parent.targets[0]

            if assign_target is None or not isinstance(
                assign_target, astroid.AssignName
            ):
                return

            # Go to outer-most scope (module), then search the child for usage
            module_node = node
            while not isinstance(module_node, astroid.Module):
                module_node = module_node.parent

            subscript_usage = set()
            for child in module_node.body:
                for search_node in child.nodes_of_class(astroid.Name):
                    search_node = cast(astroid.Name, search_node)

                    last_definition = search_node.lookup(search_node.name)[1][-1]
                    if last_definition is not assign_target:
                        continue
                    if not isinstance(search_node.parent, astroid.Subscript):
                        continue
                    subscript_node = search_node.parent
                    if not isinstance(
                        subscript_node.slice, (astroid.Const, astroid.UnaryOp)
                    ):
                        return
                    subscript_value = utils.safe_infer(subscript_node.slice)
                    subscript_value = cast(astroid.Const, subscript_value)
                    subscript_value = subscript_value.value
                    if subscript_value not in (-1, 0):
                        return
                    subscript_usage.add(subscript_value)
            if not subscript_usage:  # Not used
                return
            # Construct help text
            help_text = ""
            node_name = node_name[::-1]
            fn_name = fn_name[::-1]
            if 0 in subscript_usage:
                new_fn = "partition"[::-1]
                new_name = node_name.replace(fn_name, new_fn, 1)[::-1]
                help_text += f"{new_name} to extract the first element of a .split()"

            if -1 in subscript_usage:
                new_fn = "rpartition"[::-1]
                new_name = node_name.replace(fn_name, new_fn, 1)[::-1]
                help_text += " and " if help_text != "" else ""
                help_text += f"{new_name} to extract the last element of a .split()"
            self.add_message(
                "consider-using-str-partition", node=node, args=(help_text,)
            )

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
