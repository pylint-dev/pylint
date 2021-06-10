from typing import Union

import astroid

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages
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

    @check_messages("consider-using-tuple")
    def visit_for(self, node: astroid.For) -> None:
        self._check_inplace_defined_list_set(node)

    @check_messages("consider-using-tuple")
    def visit_comprehension(self, node: astroid.Comprehension) -> None:
        self._check_inplace_defined_list_set(node)

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
