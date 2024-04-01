import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class RequestsSessionTimeoutChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = "requests-session-timeout-checker"
    msgs = {
        "W3102": (
            "No timeout set for requests.Session() object.",
            "missing-timeout-session",
            "You should set a timeout for requests.Session() object creation.",
        ),
    }

    @staticmethod
    def visit_call(node):
        if isinstance(node.func, astroid.Attribute):
            if (
                isinstance(node.func.expr, astroid.Name)
                and node.func.expr.name == "requests"
                and node.func.attrname == "Session"
            ):
                for arg in node.args:
                    if isinstance(arg, astroid.Keyword) and arg.arg == "timeout":
                        return
                RequestsSessionTimeoutChecker.add_message(
                    "missing-timeout-session", node=node
                )


def register(linter):
    linter.register_checker(RequestsSessionTimeoutChecker(linter))
