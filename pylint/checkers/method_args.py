# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Variables checkers for Python code."""

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import arguments, nodes

from pylint.checkers import BaseChecker, utils
from pylint.interfaces import INFERENCE

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class MethodArgsChecker(BaseChecker):
    """BaseChecker for method_args.

    Checks for
    * missing-timeout
    """

    name = "method_args"
    msgs = {
        "W3101": (
            "Missing timeout argument for method '%s' can cause your program to hang indefinitely",
            "missing-timeout",
            "Used when a method needs a 'timeout' parameter in order to avoid waiting "
            "for a long time. If no timeout is specified explicitly the default value "
            "is used. For example for 'requests' the program will never time out "
            "(i.e. hang indefinitely).",
        ),
    }
    options = (
        (
            "timeout-methods",
            {
                "default": (
                    "requests.api.delete",
                    "requests.api.get",
                    "requests.api.head",
                    "requests.api.options",
                    "requests.api.patch",
                    "requests.api.post",
                    "requests.api.put",
                    "requests.api.request",
                ),
                "type": "csv",
                "metavar": "<comma separated list>",
                "help": "List of qualified names (i.e., library.method) which require a timeout parameter "
                "e.g. 'requests.api.get,requests.api.post'",
            },
        ),
    )

    @utils.only_required_for_messages("missing-timeout")
    def visit_call(self, node: nodes.Call) -> None:
        """Check if the call needs a timeout parameter based on package.func_name
        configured in config.timeout_methods.

        Package uses inferred node in order to know the package imported.
        """
        inferred = utils.safe_infer(node.func)
        call_site = arguments.CallSite.from_call(node)
        if (
            inferred
            and not call_site.has_invalid_keywords()
            and inferred.qname() in self.linter.config.timeout_methods
        ):
            keyword_arguments = [keyword.arg for keyword in node.keywords]
            keyword_arguments.extend(call_site.keyword_arguments)
            if "timeout" not in keyword_arguments:
                self.add_message(
                    "missing-timeout",
                    node=node,
                    args=(node.func.as_string(),),
                    confidence=INFERENCE,
                )


def register(linter: PyLinter) -> None:
    linter.register_checker(MethodArgsChecker(linter))
