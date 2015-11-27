import astroid
from pylint.checkers import BaseTokenChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import ITokenChecker, IAstroidChecker


class ElseifUsedChecker(BaseTokenChecker):
    """Checks for use of "else if" when a "elif" could be used
    """

    __implements__ = (ITokenChecker, IAstroidChecker)
    name = 'elseifused'
    msgs = {'R5501': ('Consider using "elif" instead of "else if"',
                      'else-if-used',
                      'Used when an else statement is immediately followed by '
                      'an if statement and does not contain statements that '
                      'would be unrelated to it.'),
           }

    def __init__(self, linter=None):
        BaseTokenChecker.__init__(self, linter)
        self._init()

    def _init(self):
        self._elifs = []
        self._if_counter = 0

    def _is_actual_elif(self, node):
        """Check if the given node is an actual elif

        This is a problem we're having with the builtin ast module,
        which splits `elif` branches into a separate if statement.
        Unfortunately we need to know the exact type in certain
        cases.
        """

        if isinstance(node.parent, astroid.If):
            orelse = node.parent.orelse
            # current if node must directly follow a "else"
            if orelse and orelse == [node]:
                if self._elifs[self._if_counter]:
                    return True
        return False

    def process_tokens(self, tokens):
        # Process tokens and look for 'if' or 'elif'
        for _, token, _, _, _ in tokens:
            self._elifs.append(True if token == 'elif' else False)

    def leave_module(self, _):
        self._init()

    def visit_ifexp(self, _):
        self._if_counter += 1

    def visit_comprehension(self, node):
        self._if_counter += len(node.ifs)

    @check_messages('else-if-used')
    def visit_if(self, node):
        if isinstance(node.parent, astroid.If):
            orelse = node.parent.orelse
            # current if node must directly follow a "else"
            if orelse and orelse == [node]:
                if not self._elifs[self._if_counter]:
                    self.add_message('else-if-used', node=node)
        self._if_counter += 1


def register(linter):
    """Required method to auto register this checker.

    :param linter: Main interface object for Pylint plugins
    :type linter: Pylint object
    """
    linter.register_checker(ElseifUsedChecker(linter))
