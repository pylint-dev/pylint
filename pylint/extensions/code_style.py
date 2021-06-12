from typing import List, Set, Tuple, Type, Union

import astroid
from astroid.node_classes import NodeNG

from pylint.checkers import BaseChecker, utils
from pylint.checkers.utils import check_messages, safe_infer
from pylint.interfaces import IAstroidChecker
from pylint.lint import PyLinter


class CodeStyleChecker(BaseChecker):
    """Checkers that can improve code consistency.

    As such they don't necessarily provide a performance benefit and
    are often times opinionated.

    Before adding another checker here, consider this:
    1. Does the checker provide a clear benefit,
       i.e. detect a common issue or improve performance
       => it should probably be part of the core checker classes
    2. Is it something that would improve code consistency,
       maybe because it's slightly better with regards to performance
       and therefore preferred => this is the right place
    3. Everything else should go into another extension
    """

    __implements__ = (IAstroidChecker,)

    name = "code_style"
    priority = -1
    msgs = {
        "R6101": (
            "Consider using namedtuple or dataclass for dictionary values",
            "consider-using-namedtuple-or-dataclass",
            "Emitted when dictionary values can be replaced by namedtuples or dataclass instances.",
        ),
        "R6102": (
            "Consider using an in-place tuple%s",
            "consider-using-tuple",
            "Emitted when an in-place defined list or set can be "
            "replaced by a slightly faster tuple.",
        ),
    }

    def __init__(self, linter: PyLinter) -> None:
        """Initialize checker instance."""
        super().__init__(linter=linter)

    @check_messages("consider-using-namedtuple-or-dataclass")
    def visit_dict(self, node: astroid.Dict) -> None:
        self._check_dict_consider_namedtuple_dataclass(node)

    @check_messages("consider-using-tuple")
    def visit_for(self, node: astroid.For) -> None:
        self._check_inplace_defined_list_set(node)

    @check_messages("consider-using-tuple")
    def visit_comprehension(self, node: astroid.Comprehension) -> None:
        self._check_inplace_defined_list_set(node)

    def _check_dict_consider_namedtuple_dataclass(self, node: astroid.Dict) -> None:
        """Check if dictionary values can be replaced by Namedtuple or Dataclass."""
        if not (
            isinstance(node.parent, (astroid.Assign, astroid.AnnAssign))
            and isinstance(node.parent.parent, astroid.Module)
            or isinstance(node.parent, astroid.AnnAssign)
            and utils.is_assign_name_annotated_with(node.parent.target, "Final")
        ):
            # If dict is not part of an 'Assign' or 'AnnAssign' node in
            # a module context OR 'AnnAssign' with 'Final' annotation, skip check.
            return

        # All dict_values are itself dict nodes
        if len(node.items) > 1 and all(
            isinstance(dict_value, astroid.Dict) for _, dict_value in node.items
        ):
            KeyTupleT = Tuple[Type[NodeNG], str]

            # Makes sure all keys are 'Const' string nodes
            keys_checked: Set[KeyTupleT] = set()
            for _, dict_value in node.items:
                for key, _ in dict_value.items:
                    key_tuple = (type(key), key.as_string())
                    if key_tuple in keys_checked:
                        continue
                    inferred = safe_infer(key)
                    if not (
                        isinstance(inferred, astroid.Const)
                        and inferred.pytype() == "builtins.str"
                    ):
                        return
                    keys_checked.add(key_tuple)

            # Makes sure all subdicts have at least 1 common key
            key_tuples: List[Tuple[KeyTupleT, ...]] = []
            for _, dict_value in node.items:
                key_tuples.append(
                    tuple((type(key), key.as_string()) for key, _ in dict_value.items)
                )
            keys_intersection: Set[KeyTupleT] = set(key_tuples[0])
            for sub_key_tuples in key_tuples[1:]:
                keys_intersection.intersection_update(sub_key_tuples)
            if not keys_intersection:
                return

            self.add_message("consider-using-namedtuple-or-dataclass", node=node)
            return

        # All dict_values are itself either list or tuple nodes
        if len(node.items) > 1 and all(
            isinstance(dict_value, (astroid.List, astroid.Tuple))
            for _, dict_value in node.items
        ):
            # Make sure all sublists have the same length > 0
            list_length = len(node.items[0][1].elts)
            if list_length == 0:
                return
            for _, dict_value in node.items[1:]:
                if len(dict_value.elts) != list_length:
                    return

            # Make sure at least one list entry isn't a dict
            for _, dict_value in node.items:
                if all(isinstance(entry, astroid.Dict) for entry in dict_value.elts):
                    return

            self.add_message("consider-using-namedtuple-or-dataclass", node=node)
            return

    def _check_inplace_defined_list_set(
        self, node: Union[astroid.For, astroid.Comprehension]
    ) -> None:
        """Check if inplace defined list / set can be replaced by a tuple."""
        if isinstance(node.iter, (astroid.List, astroid.Set)) and not any(
            isinstance(item, astroid.Starred) for item in node.iter.elts
        ):
            self.add_message(
                "consider-using-tuple",
                node=node.iter,
                args=(f" instead of {node.iter.__class__.__qualname__.lower()}"),
            )


def register(linter: PyLinter) -> None:
    linter.register_checker(CodeStyleChecker(linter))
