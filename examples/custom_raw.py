from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pylint.checkers import BaseRawFileChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class MyRawChecker(BaseRawFileChecker):
    r"""Check for line continuations with '\' instead of using triple
    quoted string or parenthesis.
    """

    name = "custom_raw"
    msgs = {
        "W9901": (
            "use \\ for line continuation",
            "backslash-line-continuation",
            (
                "Used when a \\ is used for a line continuation instead"
                " of using triple quoted string or parenthesis."
            ),
        )
    }
    options = ()

    def process_module(self, node: nodes.Module) -> None:
        """Process a module.

        the module's content is accessible via node.stream() function
        """
        with node.stream() as stream:
            for lineno, line in enumerate(stream):
                if line.rstrip().endswith("\\"):
                    self.add_message("backslash-line-continuation", line=lineno)


def register(linter: PyLinter) -> None:
    """This required method auto registers the checker during initialization.

    :param linter: The linter to register the checker to.
    """
    linter.register_checker(MyRawChecker(linter))
