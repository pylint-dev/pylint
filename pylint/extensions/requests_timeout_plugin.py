import astroid

from pylint.checkers import BaseChecker


class RequestsSessionTimeoutChecker(BaseChecker):
    name = "requests-session-timeout-checker"
    msgs = {
        "W3102": (
            "No timeout set for requests.Session() object.",
            "missing-timeout-session",
            "You should set a timeout for requests.Session() object creation.",
        ),
    }

    def visit_call(self, node):
        if isinstance(node.func, astroid.Attribute):
            if (
                isinstance(node.func.expr, astroid.Name)
                and node.func.expr.name == "requests"
                and node.func.attrname == "Session"
            ):
                for keyword_arg in node.keywords:
                    if keyword_arg.arg == "timeout":
                        return
                self.add_message("missing-timeout-session", node=node)


def register(linter):
    linter.register_checker(RequestsSessionTimeoutChecker(linter))
