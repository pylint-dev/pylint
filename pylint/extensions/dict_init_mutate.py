# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Check for use of dictionary mutation after initialization."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages, truncated_dict_suggestion
from pylint.interfaces import HIGH

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter


class DictInitMutateChecker(BaseChecker):
    name = "dict-init-mutate"
    msgs = {
        "C3401": (
            "Declare all known key/values when initializing the dictionary: %s",
            "dict-init-mutate",
            "Dictionaries can be initialized with a single statement "
            "using dictionary literal syntax.",
        )
    }

    @only_required_for_messages("dict-init-mutate")
    def visit_assign(self, node: nodes.Assign) -> None:
        """
        Detect dictionary mutation immediately after initialization.

        At this time, detecting nested mutation is not supported.
        """
        match node:
            case nodes.Assign(
                targets=[nodes.AssignName(name=dict_name)],
                value=nodes.Dict() as dict_node,
            ):
                pass
            case _:
                return

        match node.next_sibling():
            case nodes.Assign(
                targets=[nodes.Subscript(value=nodes.Name(name=name))]
            ) if (name == dict_name):
                suggestion = self._build_suggestion(
                    dict_name, dict_node, node.next_sibling()
                )
                self.add_message(
                    "dict-init-mutate",
                    node=node,
                    args=(suggestion,),
                    confidence=HIGH,
                )

    @staticmethod
    def _build_suggestion(
        dict_name: str,
        dict_node: nodes.Dict,
        first_mutation: nodes.Assign,
    ) -> str:
        """Build a suggested dictionary literal from the init and subsequent
        mutations.
        """

        def _items() -> Iterator[str]:
            # Existing items from the dict literal
            for key, value in dict_node.items:
                if key is not None:
                    yield f"{key.as_string()}: {value.as_string()}"

            # Items from consecutive subscript assignments
            sibling: nodes.NodeNG | None = first_mutation
            while sibling is not None:
                match sibling:
                    case nodes.Assign(
                        targets=[
                            nodes.Subscript(value=nodes.Name(name=name), slice=key_node)
                        ],
                        value=val_node,
                    ) if (
                        name == dict_name
                    ):
                        yield f"{key_node.as_string()}: {val_node.as_string()}"
                    case _:
                        break
                sibling = sibling.next_sibling()

        return f"{dict_name} = {truncated_dict_suggestion(_items())}"


def register(linter: PyLinter) -> None:
    linter.register_checker(DictInitMutateChecker(linter))
