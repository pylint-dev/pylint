# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""This is the remnant of the python3 checker. It was removed because
the transition from python 2 to python3 is behind us, but some checks
are still useful in python3 after all.
See https://github.com/PyCQA/pylint/issues/5025
"""


from pylint import checkers, interfaces
from pylint.checkers import utils


class Python3Checker(checkers.BaseChecker):

    __implements__ = interfaces.IAstroidChecker
    enabled = True
    name = "python3"

    msgs = {
        "W1641": (
            "Implementing __eq__ without also implementing __hash__",
            "eq-without-hash",
            "Used when a class implements __eq__ but not __hash__.  In Python 2, objects "
            "get object.__hash__ as the default implementation, in Python 3 objects get "
            "None as their default __hash__ implementation if they also implement __eq__.",
        ),
    }

    @utils.check_messages("eq-without-hash")
    def visit_classdef(self, node):
        locals_and_methods = set(node.locals).union(x.name for x in node.mymethods())
        if "__eq__" in locals_and_methods and "__hash__" not in locals_and_methods:
            self.add_message("eq-without-hash", node=node)


def register(linter):
    linter.register_checker(Python3Checker(linter))
