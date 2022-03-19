from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class ManualMagicMethodChecker(BaseChecker):
    """Check for manual __magic__ method calls."""

    __implements__ = IAstroidChecker

    EXCLUSIONS = (
        "__init__",
        "__new__",
        "__subclasses__",
        "__init_subclass__",
    )
    name = "manual-magic-methods"
    priority = -1
    msgs = {
        "C2801": (
            "Manually invokes %s magic method.",
            "manual-magic-methods",
            "Used when a __magic__ method is manually invoked instead "
            "of using the corresponding function/method/operator.",
        ),
    }
    options = ()

    def visit_call(self, node: nodes.Call) -> None:
        """Check if method being called uses __magic__ method naming convention."""
        if (
            isinstance(node.func, nodes.Attribute)
            and node.func.attrname.startswith("__")
            and node.func.attrname.endswith("__")
            and node.func.attrname not in self.EXCLUSIONS
        ):
            self.add_message(
                "manual-magic-methods",
                node=node,
                args=(node.func.attrname,),
            )


def register(linter: "PyLinter") -> None:
    linter.register_checker(ManualMagicMethodChecker(linter))
