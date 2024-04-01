import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

class RequestsSessionTimeoutChecker(BaseChecker):
    __implements__ = (IAstroidChecker,)

    name = 'requests-session-timeout-checker'
    msgs = {
        'W3102': {
            'msg': 'No timeout set for requests.Session() object.',
            'symbol': 'missing-timeout-session',
            'desc': 'You should set a timeout for requests.Session() object creation.'
        }
    }

    def visit_call(self, node):
        if isinstance(node.func, astroid.Attribute):
            if isinstance(node.func.expr, astroid.Name) and node.func.expr.name == 'requests' \
                    and node.func.attrname == 'Session':
                for keyword_arg in node.keywords:
                    if keyword_arg.arg == 'timeout':
                        return
                self.add_message('missing-timeout-session', node=node)

def register(linter):
    linter.register_checker(RequestsSessionTimeoutChecker(linter))

